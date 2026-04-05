# Storage

## Table of Contents

- [Storage](#storage)
  - [Table of Contents](#table-of-contents)
  - [Placeholders](#placeholders)
  - [Drive Information](#drive-information)
    - [List Block Devices](#list-block-devices)
    - [List Mountpoints and Usage](#list-mountpoints-and-usage)
    - [Inspect fstab](#inspect-fstab)
    - [Find Device Path from UUID](#find-device-path-from-uuid)
    - [Power On Hours](#power-on-hours)
  - [Partitions and Filesystems](#partitions-and-filesystems)
  - [Mounting](#mounting)
  - [SMART Diagnostics](#smart-diagnostics)
  - [Badblocks](#badblocks)
  - [Cloning drives and images with dd](#cloning-drives-and-images-with-dd)
  - [Benchmarking](#benchmarking)
  - [USB Devices](#usb-devices)
    - [Device Recognition](#device-recognition)
    - [Test Device Integrity](#test-device-integrity)
    - [Switching Two USB Keys](#switching-two-usb-keys)

## Placeholders

Replace the placeholders below with the appropriate values for your setup:

- **Devices**
  - Block device: `<device>` (e.g., /dev/sda)
  - Partition: `<partition>` (e.g., /dev/sda1)
  - UUID: `<uuid>` (e.g., a1b2c3d4-e5f6-7890-abcd-ef1234567890)

- **Paths**
  - Mount point: `<mountpoint>` (e.g., /mnt/media)
  - Directory path: `<dirpath>` (e.g., /mnt/data)

## Drive Information

### List Block Devices

Check all attached block devices by type:

```bash
ls /dev/sd*
ls /dev/nv*
```

### List Mountpoints and Usage

**Tree view of all block devices with sizes and mountpoints**

```bash
lsblk
lsblk -f
```

- `-f`: Add filesystem type, label, and UUID to the tree.

**Disk space usage for all mounted filesystems**

```bash
df -h
```

- `-h`: Human-readable.

**Disk space usage for a specific device**

```bash
df -h | grep <device>
```

### Inspect fstab

**View all configured mount entries**

```bash
cat /etc/fstab
```

### Find Device Path from UUID

Using `lsblk`:

```bash
lsblk -o NAME,UUID,MOUNTPOINT
```

Using `blkid`:

```bash
blkid | grep <uuid>
blkid -U <uuid>
```

### Power On Hours

Check power-on hours across multiple drives at once:

```bash
for dev in /dev/sd{a,b,c,d}; do echo -n "$dev: "; smartctl -a $dev | grep "Power_On_Hours"; done
```

## Partitions and Filesystems

**View partition table and disk details:**

```bash
fdisk -l <device>
```

**Check and repair a filesystem:**

```bash
fsck <partition>
```

## Mounting

**Validate all `fstab` entries**

```bash
findmnt --verify --verbose
```

**Dry-run mount of all fstab entries, reports what would succeed or fail**

```bash
mount -fav
```

- `-f`: Fake mount — goes through the motions without making the actual syscall.
- `-a`: Process all entries in `/etc/fstab` (excluding `noauto`).
- `-v`: Verbose output.

**Find mount point details:**

```bash
findmnt <device>
mount | grep <device>
```

**Apply fstab changes without rebooting**

```bash
mount -o remount -a
```

**Unmount and Safely Remove**

```bash
umount <device>
eject <device>
```

## SMART Diagnostics

**Get full SMART information for a drive:**

```bash
smartctl -a <device>
```

**Get drive identity and model info only:**

```bash
smartctl -i <device>
```

**Run a short SMART test:**

```bash
smartctl -t short <device>
```

**Run a long SMART test:**

```bash
smartctl -t long <device>
```

**View test results:**

```bash
smartctl -a <device>
```

**Check SMART device statistics (error counters, etc.):**

```bash
smartctl -A <device>
```

## Badblocks

**Read-only test:**

```bash
badblocks -v <device>
```

**Non-destructive read-write test:**

`Save to RAM -> Write Pattern -> Verify -> Restore`

```bash
badblocks -nsv <device>
```

- `-n`: Non-destructive read-write test.
- `-s`: Show progress.
- `-v`: Verbose output.
- Warning: If the computer loses power or the kernel panics after Step 2 but before Step 4, that specific block of data will be lost

**Destructive write test**

Overwrites all data — use only on blank drives or drives to be deleted.

```bash
badblocks -wsv <device>
```

## Cloning drives and images with dd

**Clone a drive or create an image:**

```bash
dd if=<source-device> of=<destination-device> bs=4M status=progress
dd if=<source-device> of=<image-file>.img bs=4M status=progress
```

**Restore from image:**

```bash
dd if=<image-file>.img of=<destination-device> bs=4M status=progress
sync
```

## Benchmarking

**Measure read speed with `hdparm`:**

```bash
hdparm -t <device>
```

## USB Devices

### Device Recognition

Check if the system recognizes the device and show recent USB-related kernel messages:

```bash
lsusb
dmesg | tail -n 20
```

### Test Device Integrity

Warning: The write test is destructive. All data on <device> will be permanently overwritten. Verify the target device with lsblk before running.

1. **Unmount the device** (if mounted):

   ```bash
   umount <mountpoint>
   ```

2. **Write test:**

   ```bash
   dd if=/dev/zero of=<device> bs=4M count=256 status=progress
   ```

3. **Read test:**

   ```bash
   dd if=<device> of=/dev/null bs=4M count=256 status=progress
   ```

4. **Check for bad blocks:**

   ```bash
   badblocks -wsv <device>
   ```

5. **Run a SMART test:**

   ```bash
   smartctl -t short <device>
   smartctl -a <device>
   ```

### Switching Two USB Keys

Copy data off, reformat, and restore:

```bash
cp -r /media/<username>/<volume-label> /tmp/<backup-folder>
umount <device-partition>
mkfs.vfat <device-partition>

cp -r /tmp/<backup-folder> /media/<username>/<new-volume-label>
umount <device-partition>
```

Or clone with `dd`:

```bash
dd if=<source-device> of=/tmp/usb_image.img bs=4M status=progress
mkfs.vfat <device-partition>
dd if=/tmp/usb_image.img of=<destination-device> bs=4M status=progress
sync
```
