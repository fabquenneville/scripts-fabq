# Linux

## Table of Contents

- [Linux](#linux)
  - [Table of Contents](#table-of-contents)
  - [Basic Commands](#basic-commands)
  - [USB Devices](#usb-devices)
    - [Test USB Key](#test-usb-key)

## System information

## Basic Commands

## USB Devices

### Test USB Key

**Device Information**
Check if the system recognizes the device and show the latest system messages related to USB devices being connected.

```bash
lsusb
dmesg | tail -n 20
```

**Find Mount Points and Device Information**
Identify mount points, partitions, and other relevant details of mounted devices.

```bash
lsblk -f
df -h | grep /dev/sdc
findmnt /dev/sdc1
mount | grep /dev/sd
```

**Print Detailed Information About the USB Key**
View detailed partition and disk information.

```bash
fdisk -l /dev/sdc
```

**Test the File System**
Check and repair the filesystem on the USB key.

```bash
fsck /dev/sdc1
```

**Test Data Integrity**
Perform read/write tests to ensure the integrity of the USB key.

1. **Unmount the USB Key** (if mounted):
   ```bash
   umount /media/fabrice/BD48-F8BB
   ```
2. **Write Test**:
   ```bash
   dd if=/dev/zero of=/dev/sdc bs=4M count=256 status=progress
   ```
3. **Read Test**:
   ```bash
   dd if=/dev/sdc of=/dev/null bs=4M count=256 status=progress
   ```

**Check for Bad Blocks**
Identify any bad sectors on the USB key.

- **Read-only test**:
  ```bash
  badblocks -v /dev/sdc
  ```
- **Non-destructive read-write test**:

  ```bash
  badblocks -nsv /dev/sdc
  ```

- The -n option performs a non-destructive read-write test.
- The -s option shows progress.
- The -v option is for verbose output.

**Perform a SMART Test**
Run SMART diagnostics to test the health of the USB key.

1. **Start a short SMART test**:
   ```bash
   smartctl -t short /dev/sdc
   ```
2. **View test results**:
   ```bash
   smartctl -a /dev/sdc
   ```

**Benchmark the Speed**
Measure the read speed of the USB key.

```bash
hdparm -t /dev/sdc
```

**Unmount and Safely Remove**
Unmount the USB key and safely remove it from the system.

```bash
umount /mnt/usb
eject /dev/sdc
```
