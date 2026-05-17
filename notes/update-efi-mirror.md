# Redundant Root with EFI Mirror

## Table of Contents

- [Redundant Root with EFI Mirror](#redundant-root-with-efi-mirror)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Placeholders](#placeholders)
  - [How It Works](#how-it-works)
  - [Paths](#paths)
  - [Setup Procedure](#setup-procedure)
    - [1. Format the Disks](#1-format-the-disks)
    - [2. Convert the Root Filesystem to BTRFS RAID1](#2-convert-the-root-filesystem-to-btrfs-raid1)
    - [3. Configure fstab](#3-configure-fstab)
    - [4. Install the Sync Script](#4-install-the-sync-script)
    - [5. Configure apt to Run the Script Post-Install](#5-configure-apt-to-run-the-script-post-install)
    - [6. Test](#6-test)
  - [Moving to a New Disk](#moving-to-a-new-disk)

## Overview

This setup provides a redundant Debian root drive using BTRFS RAID1 across two disks, with a synced EFI partition on both so the machine can boot from either. The script `update-efi-mirror` keeps the backup EFI in sync and re-installs GRUB on both physical disks. It is triggered automatically after every `apt` operation.

## Placeholders

Replace the placeholders below with the appropriate values for your setup:

- **Devices**
  - Primary disk: `<primary-disk>` (e.g., /dev/sda, /dev/nvme0n1)
  - Backup disk: `<backup-disk>` (e.g., /dev/sdb, /dev/nvme1n1)
  - Primary EFI partition: `<primary-efi-part>` (e.g., /dev/sda1, /dev/nvme0n1p1)
  - Backup EFI partition: `<backup-efi-part>` (e.g., /dev/sdb1, /dev/nvme1n1p1)
  - Primary root partition: `<primary-root-part>` (e.g., /dev/sda2, /dev/nvme0n1p2)
  - Backup root partition: `<backup-root-part>` (e.g., /dev/sdb2, /dev/nvme1n1p2)
  - Primary swap partition: `<primary-swap-part>` (e.g., /dev/sda3, /dev/nvme0n1p3)
  - Backup swap partition: `<backup-swap-part>` (e.g., /dev/sdb3, /dev/nvme1n1p3)

- **UUIDs**
  - Primary EFI UUID: `<primary-efi-uuid>` (e.g., D167-0F46)
  - Backup EFI UUID: `<backup-efi-uuid>` (e.g., 08E8-A87C)
  - Root BTRFS UUID: `<root-uuid>` (e.g., 387526ec-f3bd-4fa8-a17e-e985121ada0b)
  - Primary swap UUID: `<primary-swap-uuid>`
  - Backup swap UUID: `<backup-swap-uuid>`

## How It Works

- The root filesystem is BTRFS RAID1 across two partitions. Either disk alone can serve reads and writes.
- Each disk has its own EFI partition. GRUB is installed on both physical disks.
- After every `apt` install or upgrade, an apt hook calls `update-efi-mirror`, which:
  1. Rsyncs the live `/boot/efi` to the backup EFI partition.
  2. Runs `grub-install` on both physical disks.
- Either disk can be removed and the system will still boot and run.

## Paths

- **Sync script**: `/usr/local/sbin/update-efi-mirror`
- **Apt hook**: `/etc/apt/apt.conf.d/99-update-efi-mirror`
- **fstab**: `/etc/fstab`

## Setup Procedure

### 1. Format the Disks

**Verify which disks are present before touching anything**

```bash
lsblk
lsblk -f
```

**Open `fdisk` on the backup disk**

If the disk was previously used at a smaller capacity, the GPT backup table may be misaligned — `fdisk` will correct it on write.

```bash
fdisk <backup-disk>
```

Create a GPT partition table if not already present:

```
g
```

**Check the primary disk partition layout and note the exact sector boundaries**

```bash
fdisk -l <primary-disk>
```

This shows the `Start` and `End` sectors for each partition. Use these values when partitioning the backup disk so the layouts match exactly.

**Create the three partitions to match the layout of the primary disk**

| #   | Size      | Type       |
| --- | --------- | ---------- |
| 1   | 830M      | EFI System |
| 2   | ~12G      | Linux fs   |
| 3   | Remainder | Linux swap |

Inside `fdisk`, the sequence is:

```
n          # new partition
            # enter the exact End sector from the primary disk to match partition sizes
t          # change type
1          # select partition 1
EFI System # set type to EFI
t          # change type
3          # select partition 3
Linux swap # set type to swap
w          # write and exit
```

**Partition sizes must be at least as large as the corresponding primary partition** — the BTRFS replace will fail if the target partition is smaller than the source.

**Format the new EFI partition**

```bash
apt install dosfstools   # if not installed
mkfs.fat -F32 <backup-efi-part>
```

**Format the new swap partition**

```bash
mkswap <backup-swap-part>
```

**Check UUIDs of the new partitions**

```bash
lsblk -f <backup-disk>
```

### 2. Convert the Root Filesystem to BTRFS RAID1

**Add the backup partition to the BTRFS volume**

```bash
btrfs device add <backup-root-part> /
```

**Convert to RAID1**

```bash
btrfs balance start -mconvert=raid1 -dconvert=raid1 /
```

Monitor the balance:

```bash
btrfs balance status /
```

**Verify the final layout**

```bash
btrfs filesystem show /
btrfs fi usage /
```

### 3. Configure fstab

Edit `/etc/fstab` to mount the primary EFI partition normally and document the backup EFI UUID in a commented-out entry. The script reads the backup UUID from this comment.

**Edit fstab**

```bash
nano /etc/fstab
```

The fstab should contain:

```
# Primary EFI — mounted at boot
UUID=<primary-efi-uuid>  /boot/efi  vfat  umask=0077  0  1

# Backup EFI — not auto-mounted, used by update-efi-mirror
#UUID=<backup-efi-uuid> /boot/efi vfat umask=0077 0 1

# Root — BTRFS RAID1 (both partitions share the same UUID)
UUID=<root-uuid>  /  btrfs  defaults,noatime  0  1

# Swap — both disks
UUID=<primary-swap-uuid>  none  swap  sw  0  0
UUID=<backup-swap-uuid>   none  swap  sw  0  0
```

The backup EFI line must start with `#UUID=` — this is the format the script greps for:

```bash
grep "^#UUID=" /etc/fstab | grep "/boot/efi"
```

**Reload systemd after editing fstab**

```bash
systemctl daemon-reload
```

### 4. Install the Sync Script

**Create the script**

```bash
nano /usr/local/sbin/update-efi-mirror
```

Paste the contents of `update-efi-mirror.sh`.

**Set ownership and permissions**

```bash
chown root:root /usr/local/sbin/update-efi-mirror
chmod 755 /usr/local/sbin/update-efi-mirror
```

The script will:

1. Detect the currently mounted EFI partition and its disk.
2. Read the backup EFI UUID from the `#UUID=` comment in `/etc/fstab`.
3. Mount the backup EFI to a temp directory, rsync all files from the live EFI, then unmount.
4. Run `grub-install --recheck` on both physical disks.

### 5. Configure apt to Run the Script Post-Install

**Create the apt hook**

```bash
nano /etc/apt/apt.conf.d/99-update-efi-mirror
```

Add:

```
DPkg::Post-Invoke {"if [ -x /usr/local/sbin/update-efi-mirror ]; then /usr/local/sbin/update-efi-mirror; fi";};
```

This runs the sync script after every `apt` operation that invokes `dpkg` — including kernel upgrades, which update `/boot/efi` with new initramfs and GRUB config.

### 6. Test

**Run the script manually**

```bash
/usr/local/sbin/update-efi-mirror
```

Expected output:

```
Syncing EFI files: <primary-efi-uuid> -> <backup-efi-uuid>
EFI Files Sync Complete.
Updating GRUB bootloader on both physical disks...
Redundancy Complete: Files synced and GRUB updated on <primary-disk> and <backup-disk>.
```

**Test the apt hook**

```bash
apt update
apt upgrade -y
```

The sync output should appear at the end of the upgrade, after GRUB regenerates its config.

**Verify the backup EFI contents match**

```bash
TMPMNT=$(mktemp -d)
mount -U <backup-efi-uuid> "$TMPMNT"
diff -r /boot/efi/ "$TMPMNT/"
umount "$TMPMNT"
rmdir "$TMPMNT"
```

**Verify GRUB is installed on both disks**

```bash
fdisk -l <primary-disk> | grep -i efi
fdisk -l <backup-disk>  | grep -i efi
```

**`Optional` Boot from the backup disk**

Swap the boot order in BIOS/UEFI to confirm the machine boots cleanly from `<backup-disk>`.

## Moving to a New Disk

Use this procedure when replacing one of the two disks in the BTRFS RAID1 — for example when upgrading to a larger drive.

**1. Partition the new disk** following [Step 1](#1-format-the-disks).

**2. Find the device ID of the partition to be replaced:**

```bash
btrfs filesystem show /
```

**3. Shrink the filesystem on the disk being replaced to fit the new partition:**

```bash
btrfs filesystem resize <device-id>:<size> /
```

**4. Replace the old partition with the new one:**

```bash
btrfs replace start <device-id> <new-root-part> /
btrfs replace status /
```

**5. Grow the new partition to max:**

```bash
btrfs filesystem resize <device-id>:max /
```

**6. Update fstab** if the backup EFI UUID has changed (new disk = new EFI UUID):

```bash
lsblk -f <new-disk>
nano /etc/fstab
systemctl daemon-reload
```

**7. Run the sync script** to install GRUB on the new disk and populate its EFI partition:

```bash
/usr/local/sbin/update-efi-mirror
```

**8. Verify** following [Step 6](#6-test).
