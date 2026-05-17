# EFI Partition Repair

## Table of Contents

- [EFI Partition Repair](#efi-partition-repair)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Placeholders](#placeholders)
  - [Repair Procedure](#repair-procedure)
    - [1. Verify What You're Working With](#1-verify-what-youre-working-with)
    - [2. Mount Everything for Chroot](#2-mount-everything-for-chroot)
    - [3. Chroot In](#3-chroot-in)
    - [4. Reinstall GRUB](#4-reinstall-grub)
    - [5. Regenerate GRUB Config](#5-regenerate-grub-config)
    - [6. Verify fstab](#6-verify-fstab)
    - [7. Exit and Reboot](#7-exit-and-reboot)

## Overview

Use this procedure when a Debian machine fails to boot but the root filesystem appears intact — for example after a failed kernel upgrade, a corrupted EFI partition, or GRUB being wiped by another OS. Boot from a live environment, chroot into the installed system, and reinstall GRUB.

## Placeholders

Replace the placeholders below with the appropriate values for your setup:

- **Devices**
  - Disk: `<disk>` (e.g., /dev/sda, /dev/nvme0n1)
  - EFI partition: `<efi-part>` (e.g., /dev/sda1, /dev/nvme0n1p1)
  - Root partition: `<root-part>` (e.g., /dev/sda2, /dev/nvme0n1p2)

- **Filesystem**
  - Root subvolume name: `<root-subvol>` (e.g., @rootfs)

## Repair Procedure

### 1. Verify What You're Working With

Identify the disk layout, partition types, UUIDs, and current mount points:

```bash
lsblk -o NAME,SIZE,FSTYPE,PARTTYPE,UUID,MOUNTPOINT
```

Confirm which partition is EFI and which is root before proceeding.

### 2. Mount Everything for Chroot

**Mount the root filesystem**

```bash
mkdir -p /mnt
mount -o subvol=<root-subvol> <root-part> /mnt
```

**Mount the EFI partition**

```bash
mkdir -p /mnt/boot/efi
mount <efi-part> /mnt/boot/efi
```

**Bind mount the pseudo-filesystems**

```bash
mkdir -p /mnt/{dev,proc,sys,run}
mount --bind /dev  /mnt/dev
mount --bind /proc /mnt/proc
mount --bind /sys  /mnt/sys
mount --bind /run  /mnt/run
```

**Bind mount EFI vars**

Required for `grub-install` to write boot entries to the firmware:

```bash
mount --bind /sys/firmware/efi/efivars /mnt/sys/firmware/efi/efivars
```

### 3. Chroot In

```bash
chroot /mnt /bin/bash
source /etc/profile
export PS1="(chroot) $PS1"
```

### 4. Reinstall GRUB

**Run grub-install on the disk**

```bash
grub-install --target=x86_64-efi --efi-directory=/boot/efi --bootloader-id=debian --recheck <disk>
```

If you get an error about EFI vars not being writable:

```bash
mount -o remount,rw /sys/firmware/efi/efivars
```

Then re-run `grub-install`.

### 5. Regenerate GRUB Config

```bash
update-grub
```

Check the output — it should find your kernel on the btrfs volume. If it complains about not finding a kernel, you may need to also reinstall it:

**Check what kernel is installed**

```bash
dpkg -l | grep linux-image
```

**Reinstall the kernel if missing or broken**

```bash
apt-get install --reinstall linux-image-amd64
```

Then re-run `update-grub`.

### 6. Verify fstab

Confirm the EFI and root entries look correct before rebooting:

```bash
cat /etc/fstab
```

### 7. Exit and Reboot

**Exit the chroot**

```bash
exit
```

**Unmount everything**

```bash
umount -R /mnt
```

**Reboot**

```bash
reboot
```
