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
    - [Swap](#swap)
  - [Partitions and Filesystems](#partitions-and-filesystems)
  - [TRIM](#trim)
  - [Mounting](#mounting)
  - [SMART Diagnostics](#smart-diagnostics)
  - [Hardware Monitoring](#hardware-monitoring)
  - [Kernel Messages](#kernel-messages)
  - [Badblocks](#badblocks)
  - [Hex Dump](#hex-dump)
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

**Exclude loop devices from the listing**

```bash
lsblk -e 7
```

- `-e 7`: Excludes device major number 7 (loop devices), keeping the output clean on systems with many snaps or loop mounts.

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
blkid <partition>
```

### Power On Hours

Check power-on hours across multiple drives at once:

```bash
for dev in /dev/sd{a,b,c,d}; do echo -n "$dev: "; smartctl -a $dev | grep "Power_On_Hours"; done
for dev in /dev/sd{a..d}; do echo -n "$dev: "; smartctl -a $dev | grep "Power_On_Hours"; done
```

### Swap

Check Swap currently used by the system:

```bash
swapon --show
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

## TRIM

TRIM allows the OS to inform the drive which blocks are no longer in use, maintaining performance on SSDs and NVMe drives over time.

**Run TRIM once manually across all mounted filesystems:**

```bash
fstrim -av
```

- `-a`: Run on all mounted filesystems that support TRIM.
- `-v`: Verbose — reports how much space was freed per filesystem.

**Enable the weekly TRIM timer:**

```bash
systemctl enable --now fstrim.timer
```

- Debian/Ubuntu run this weekly by default once enabled.
- Check timer status with `systemctl status fstrim.timer`.

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

**Check active mounts for a specific mountpoint:**

```bash
cat /proc/mounts | grep <mountpoint>
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

```bash
for dev in /dev/sd[a-z] /dev/nvme[0-9]n[0-9]; do
   echo "--- $dev ---"
   smartctl -i $dev | grep -Ei "Model|Serial Number|Capacity"
done
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

**Filter for key health attributes:**

Check the most important failure indicators in a single line:

```bash
smartctl -A <device> | grep -E "Reallocated|Pending|UDMA_CRC"
```

**Check multiple health attributes at once:**

```bash
smartctl -a <device> | grep -E "Power_On_Hours|Load_Cycle_Count|Reallocated_Sector_Ct"
```

**Check temperatures across all drives:**

Scans all SMART-capable devices and prints their temperature:

```bash
smartctl --scan | awk '{print $1}' | while read dev; do \
  echo -n "$dev: "; \
  smartctl -A $dev | grep -iE 'Temperature|Airflow_Temp' | awk '
    /Temperature_Celsius/ {print $10 "°C"}
    /Airflow_Temperature_Cel/ {print $10 "°C"}
    /Temperature:/ {print $2 "°C"}
  ' | head -n 1; \
done
```

**Watch drive temperatures continuously:**

```bash
watch -n 5 "smartctl --scan | awk '{print \$1}' | while read dev; do \
  echo -n \"\$dev: \"; \
  smartctl -A \$dev | grep -iE 'Temperature|Airflow_Temp' | awk '\
    /Temperature_Celsius/ {print \$10 \"°C\"} \
    /Airflow_Temperature_Cel/ {print \$10 \"°C\"} \
    /Temperature:/ {print \$2 \"°C\"}' | head -n 1; \
done"
```

## Hardware Monitoring

**Install lm-sensors:**

```bash
apt install lm-sensors
```

**Detect available sensor chips:**

Run once after installation to probe for hardware sensors:

```bash
sensors-detect
```

**Display current sensor readings:**

Shows CPU, GPU, and motherboard temperatures, fan speeds, and voltages:

```bash
sensors
```

## Kernel Messages

**Tail the most recent kernel messages:**

```bash
dmesg | tail -n 25
```

**Show only errors and warnings:**

```bash
dmesg --level=err,warn
```

**Show kernel messages with human-readable timestamps:**

```bash
dmesg -T
```

**Filter for NVMe events:**

```bash
dmesg | grep -i nvme
dmesg -w | grep -i nvme
```

- `-w`: Follow — print new messages as they arrive (like `tail -f`).

**Filter for ATA/SCSI/SATA/NVMe device events:**

```bash
dmesg | grep -i -E 'scsi|ata|nvme|sata'
```

**Filter for I/O errors:**

```bash
dmesg | grep -i "I/O error"
```

**Filter for ATA/SCSI/SATA/NVMe device errors:**

```bash
dmesg | grep -i -E 'scsi|ata|nvme|sata'
```

**Map ATA port number to block device name:**

When `dmesg` reports an error on e.g. `ata7` and you need to identify which physical drive that is:

```bash
ls -l /sys/class/block/ | grep ata<port-number>
dmesg -T | grep -iE "ata"
```

**Filter for BTRFS events:**

```bash
dmesg | grep -i btrfs
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

## Hex Dump

Inspect raw bytes on a device directly, useful for verifying partition tables, boot sectors, or investigating corruption.

**View the first 512 bytes (MBR / partition table):**

```bash
hexdump -C -n 512 <device>
```

**View 1 MB of data starting at a specific offset:**

```bash
hexdump -C -s 1G -n 1M <device>
```

- `-C`: Canonical format — hex on the left, ASCII on the right.
- `-n <length>`: Number of bytes to read.
- `-s <offset>`: Skip to this offset before reading.

**Extract readable strings from a raw device:**

Useful for locating file paths, filenames, or metadata remnants directly on a block device:

```bash
strings <device> | grep -C 200 "<search-term>" > <output-file>.txt
```

- `-C 200`: Show 200 lines of context around each match.
- Redirect to a file — output can be very large on multi-TB drives.

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
