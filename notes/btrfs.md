# BTRFS

## Table of Contents

- [BTRFS](#btrfs)
  - [Table of Contents](#table-of-contents)
  - [Placeholders](#placeholders)
  - [BTRFS Command Shorthands](#btrfs-command-shorthands)
  - [Information on Filesystem](#information-on-filesystem)
  - [Drive Manipulation](#drive-manipulation)
    - [Replace Drives](#replace-drives)
    - [Degraded Mount and Missing Device Removal](#degraded-mount-and-missing-device-removal)
  - [Filesystem Manipulation](#filesystem-manipulation)
    - [Upgrading Btrfs Block Group Cache to V2](#upgrading-btrfs-block-group-cache-to-v2)
    - [Defrag](#defrag)
  - [Balances](#balances)
  - [Scrub](#scrub)
  - [Snapshots](#snapshots)
    - [Create Snapshots](#create-snapshots)
    - [Delete Snapshots](#delete-snapshots)
  - [Backup Procedures](#backup-procedures)
  - [Recovery](#recovery)
    - [Filesystem Check](#filesystem-check)
    - [Diagnosis](#diagnosis)

## Placeholders

Replace the placeholders below with the appropriate values for your setup:

- **Devices**
  - Block device: `<device>` (e.g., /dev/sda)
  - Source device to replace: `<source-device>` (e.g., /dev/sdb)
  - Target device: `<target-device>` (e.g., /dev/sdc)
  - UUID: `<uuid>` (e.g., a1b2c3d4-e5f6-7890-abcd-ef1234567890)

- **Paths**
  - Mount point: `<mountpoint>` (e.g., /mnt/media)
  - Subvolume name: `<subvolume>` (e.g., root, home, backups, snapshots)
  - Subvolume ID: `<subvolume-id>` (e.g., 257)
  - Snapshot label: `<snapshot-label>` (e.g., 2024-09-15)

## BTRFS Command Shorthands

Most `btrfs` subcommands accept shortened aliases. The table below lists the common ones used throughout this document.

| Long form                     | Short form              |
| ----------------------------- | ----------------------- |
| `btrfs filesystem`            | `btrfs fi`              |
| `btrfs filesystem show`       | `btrfs fi show`         |
| `btrfs filesystem usage`      | `btrfs fi usage`        |
| `btrfs filesystem df`         | `btrfs fi df`           |
| `btrfs filesystem resize`     | `btrfs fi resize`       |
| `btrfs filesystem defragment` | `btrfs fi defrag`       |
| `btrfs subvolume`             | `btrfs sub`             |
| `btrfs subvolume list`        | `btrfs sub list`        |
| `btrfs subvolume snapshot`    | `btrfs sub snap`        |
| `btrfs subvolume delete`      | `btrfs sub del`         |
| `btrfs subvolume get-default` | `btrfs sub get-default` |
| `btrfs subvolume set-default` | `btrfs sub set-default` |
| `btrfs device`                | `btrfs dev`             |
| `btrfs device add`            | `btrfs dev add`         |
| `btrfs device usage`          | `btrfs dev usage`       |
| `btrfs device stats`          | `btrfs dev stats`       |
| `btrfs balance start`         | `btrfs bal start`       |
| `btrfs balance status`        | `btrfs bal status`      |
| `btrfs balance cancel`        | `btrfs bal cancel`      |
| `btrfs inspect-internal`      | `btrfs insp`            |

## Information on Filesystem

**Show Basic Filesystem Information**

Display basic information (size, IDs, paths, etc.) for the specified mountpoint:

```bash
btrfs fi show <mountpoint>
```

**Display detailed usage information**

To show detailed usage information (allocated, unallocated, free, used, etc.) for the specified mountpoint:

```bash
btrfs fi usage <mountpoint>
```

**Display detailed usage information as a table**

```bash
btrfs fi usage -T <mountpoint>
```

- `-T` The tabular flag gives you a nice grid that shows exactly how much Data, Metadata, and System space is allocated per device.

**Display Detailed Allocation Information**

View block groups and used space:

```bash
btrfs fi df <mountpoint>
```

**Get Detailed Device Usage Statistics**

Physical size, unallocated space, RAID levels, etc.:

```bash
btrfs device usage <mountpoint>
```

**Scan and Display BTRFS Information**

Scan all devices or a specific drive:

```bash
btrfs device scan
btrfs device scan <device>
```

**Retrieve Statistics and Error Information**

Read errors, write errors, flush errors, etc.:

```bash
btrfs device stats <mountpoint>
```

**Reset Device Error Counters**

Reset all per-device error counters to zero after acknowledging them:

```bash
btrfs device stats --reset <mountpoint>
btrfs device stats -z <mountpoint>
```

- `-z` / `--reset`: Zeroes the counters after printing. Useful after a known event you've already investigated.

**List BTRFS Subvolumes**

```bash
btrfs subvolume list <mountpoint>
```

**Default Subvolume**

Check if a non-standard subvolume is set as the default:

```bash
btrfs subvol get-default <mountpoint>
btrfs subvol list <mountpoint>
```

Change the default subvolume:

```bash
btrfs subvol set-default <subvolume-id> <mountpoint>
```

**Verify Current Cache Version**

Check if your filesystem is using cache V1 by device:

```bash
btrfs inspect-internal dump-super -f <device> | grep cache_generation
```

By UUID:

```bash
btrfs inspect-internal dump-super -f $(blkid -U <uuid>) | grep cache_generation
```

- If `cache_generation` is present, cache V1 is in use. If absent, the filesystem is already using V2.

## Drive Manipulation

**Mount Whole Drive**

```bash
mount UUID=<uuid> <mountpoint>
```

**Mount Subvolume by Name**

```bash
mount UUID=<uuid> -o subvol=<subvolume> <mountpoint>
```

**Mount Subvolume by ID**

```bash
btrfs subvol list /
mount -o subvolid=<subvolume-id> /dev/disk/by-uuid/<uuid> <mountpoint>
```

**Mount Read-Only**

Mount a partition in read-only mode, useful for forensics or recovery without risking further writes:

```bash
mount -r <device> <mountpoint>
```

**Remount with Performance Options**

Apply common performance mount options to a live filesystem without unmounting:

```bash
mount -o remount,noatime,compress=zstd:3,autodefrag,space_cache=v2 <mountpoint>
```

**Remount with Default Options**

```bash
mount -o remount,defaults,noatime,compress=zstd:3 <mountpoint>
```

**Add a New Drive**

```bash
btrfs device add <device> <mountpoint>
```

**Resize Filesystem**

Grow the filesystem on a specific device to its maximum:

```bash
btrfs filesystem resize 1:max <mountpoint>
```

**Create Subvolumes**

```bash
btrfs subvol create <mountpoint>/<subvolume>
```

### Replace Drives

**Start the replacement process:**

Copies data from the old drive to the new drive while the filesystem remains mounted:

```bash
btrfs replace start <source-device> <target-device> <mountpoint>
```

- `<source-device>`: Drive to be replaced.
- `<target-device>`: Drive to replace it with.
- `<mountpoint>`: Mount point of the BTRFS filesystem.

**Monitor the progress:**

```bash
btrfs replace status <mountpoint>
```

**Monitor progress interactively:**

```bash
btrfs replace status -i <mountpoint>
```

- `-i`: Updates progress in real time.

**Notes:**

- `btrfs replace` works on a live mounted filesystem — no unmounting required.
- Useful for both failing drive replacement and capacity upgrades.
- Ensure the target drive has enough space to accommodate the source data.

### Degraded Mount and Missing Device Removal

Use when a drive has failed and you need to access the filesystem with the remaining devices.

**Mount in degraded mode:**

```bash
mount -o ro,degraded <device> <mountpoint>
```

**Mount a specific subvolume in degraded mode:**

```bash
mount -t btrfs -o degraded,subvol=<subvolume>,noatime,compress=zstd:3 UUID=<uuid> <mountpoint>
```

**Remove the missing device from the filesystem:**

Once mounted degraded, remove the placeholder for the missing drive:

```bash
btrfs device remove missing <mountpoint>
```

- This cleans up the missing device slot so the filesystem no longer expects it.
- Only safe to run if data is intact on the remaining devices (e.g., RAID1 with one drive).

## Filesystem Manipulation

### Upgrading Btrfs Block Group Cache to V2

**Non-root filesystems (running system):**

```bash
mount -o remount,clear_cache,space_cache=v2 <mountpoint>
```

**Root filesystem (running system):**

1. Check if using cache V1:

   ```bash
   btrfs inspect-internal dump-super -f <device> | grep cache_generation
   ```

2. Enable cache V2 via GRUB:

   ```bash
   nano /etc/default/grub
   # Add to GRUB_CMDLINE_LINUX_DEFAULT or GRUB_CMDLINE_LINUX:
   # rootflags=clear_cache,space_cache=v2
   ```

   Example:

   ```bash
   GRUB_CMDLINE_LINUX_DEFAULT="quiet splash rootflags=clear_cache,space_cache=v2"
   ```

   ```bash
   update-grub
   reboot
   ```

3. Verify the change:

   ```bash
   btrfs inspect-internal dump-super -f <device> | grep cache_generation
   ```

4. Remove `clear_cache` from GRUB after confirming:

   ```bash
   nano /etc/default/grub
   # Remove clear_cache from rootflags, then:
   update-grub
   ```

**From a live system:**

```bash
apt update
apt install btrfs-progs
lsblk -o NAME,UUID
blkid
mount -o clear_cache,space_cache=v2 /dev/disk/by-uuid/<uuid> <mountpoint>
btrfs inspect-internal dump-super -f /dev/disk/by-uuid/<uuid> | grep cache_generation
umount <mountpoint>
```

### Defrag

**Standard recursive defrag with LZO compression:**

```bash
btrfs filesystem defrag -r -v -clzo <mountpoint>
```

- `-r`: Recursive.
- `-v`: Verbose.
- `-clzo`: Optional LZO compression to save space.

**Recursive defrag with Zstd compression, logged to file:**

Runs in the background with unbuffered output so the log file updates in real time:

```bash
stdbuf -oL btrfs filesystem defrag -r -v -czstd <mountpoint> > /root/<date>-defrag.log 2>&1 &
```

- `stdbuf -oL`: Forces line-buffered stdout so log entries appear immediately.
- `-czstd`: Zstd compression (better ratio than LZO, available since kernel 5.1).
- `&`: Runs in the background; use `tail -f /root/<date>-defrag.log` to monitor.

## Balances

**Full balance on nearly empty block groups:**

```bash
btrfs balance start --full-balance -dusage=0 -musage=0 <mountpoint>
```

- `--full-balance`: Default but with a warning if not specified.
- `-dusage=0`: Only balance data block groups that are ~0% full.
- `-musage=0`: Only balance metadata block groups that are ~0% full.

**Full balance on partially used block groups:**

```bash
btrfs balance start --full-balance -dusage=50 -musage=50 <mountpoint>
```

- `-dusage=50`: Include data block groups less than 50% full.
- `-musage=50`: Include metadata block groups less than 50% full.

**Balance data in the background:**

```bash
btrfs balance start --bg -d <mountpoint>
```

**Balance metadata in the background:**

```bash
btrfs balance start --bg -m <mountpoint>
```

**Balance data and metadata in the background:**

```bash
btrfs balance start --bg --full-balance -dusage=0 -musage=0 <mountpoint>
```

**Balance a limited number of chunks:**

```bash
btrfs balance start --bg -dlimit=100 <mountpoint>
```

**Convert to RAID1:**

Rebalances data and metadata to RAID1 profile. Use after adding a second drive or to switch from single to mirrored:

```bash
btrfs balance start -mconvert=raid1 -dconvert=raid1 <mountpoint>
```

**Cancel a balance:**

```bash
btrfs balance cancel <mountpoint>
```

**Monitor balance status:**

```bash
btrfs balance status <mountpoint>
```

## Scrub

**Start a scrub**

The scrub operation verifies data integrity against checksums:

```bash
btrfs scrub start <mountpoint>
```

**Check scrub status:**

```bash
btrfs scrub status <mountpoint>
```

**Cancel a scrub:**

```bash
btrfs scrub cancel <mountpoint>
```

**Lower scrub I/O priority:**

Reduce the impact of a running scrub on system I/O by setting it to idle class:

```bash
ionice -c 3 -p $(pgrep btrfs-scrub)
```

- `-c 3`: Idle class — only uses I/O when no other process needs it.

**Watch scrub status and device stats:**

Continuously display scrub progress and per-device error counters:

```bash
watch -n 10 "btrfs scrub status <mountpoint>; echo ''; btrfs device stats <mountpoint>"
```

**Watch scrub status and all drive temperatures:**

```bash
watch -n 5 "btrfs scrub status <mountpoint> && echo '' && \
smartctl --scan | awk '{print \$1}' | while read dev; do \
  echo -n \"\$dev: \"; \
  smartctl -A \$dev | grep -iE 'Temperature|Airflow_Temp' | awk '\
    /Temperature_Celsius/ {print \$10 \"°C\"} \
    /Airflow_Temperature_Cel/ {print \$10 \"°C\"} \
    /Temperature:/ {print \$2 \"°C\"}' | head -n 1; \
done && echo '' && btrfs device stats <mountpoint>"
```

## Snapshots

### Create Snapshots

1. **Mount the snapshots subvolume:**

   ```bash
   mount UUID=<uuid> -o subvol=snapshots <mountpoint>
   ```

2. **Create a snapshot:**

   ```bash
   btrfs subvolume snapshot <source-subvolume> "<mountpoint>/<snapshot-label>"
   ```

3. **Unmount after creating:**

   ```bash
   umount <mountpoint>
   ```

### Delete Snapshots

1. **Mount the snapshots subvolume:**

   ```bash
   mount -o subvol=snapshots /dev/disk/by-uuid/<uuid> <mountpoint>
   ```

2. **List available snapshots:**

   ```bash
   btrfs subvol list <mountpoint>
   ```

3. **Delete the desired snapshot:**

   ```bash
   btrfs subvolume delete <mountpoint>/<snapshot-label>
   ```

4. **Unmount after deleting:**

   ```bash
   umount <mountpoint>
   ```

## Backup Procedures

**Snapshot backup procedure:**

1. Mount snapshot location:

   ```bash
   mount UUID=<uuid> -o subvol=snapshots <mountpoint>
   ```

2. Create snapshots for the desired subvolumes:

   ```bash
   btrfs subvolume snapshot / "<mountpoint>/root/<snapshot-label>"
   btrfs subvolume snapshot /home "<mountpoint>/home/<snapshot-label>"
   btrfs subvolume snapshot <source-subvolume> "<mountpoint>/<subvolume>/<snapshot-label>"
   ```

3. Unmount after creating snapshots:

   ```bash
   umount <mountpoint>
   ```

## Recovery

1. **Mount a Subvolume with Recovery Options:**

   ```bash
   mount -o recovery,subvol=<subvolume> UUID=<uuid> <mountpoint>
   ```

2. **Clear Cache During Mount:**

   ```bash
   mount -o clear_cache,subvol=<subvolume> UUID=<uuid> <mountpoint>
   ```

3. **Data Restoration with btrfs restore:**

   ```bash
   btrfs restore -D <device>
   ```

### Filesystem Check

Run offline consistency checks on an unmounted BTRFS filesystem.

**Check an unmounted filesystem:**

```bash
btrfs check <device>
```

- Must be run on an **unmounted** device. Running on a mounted filesystem risks corruption.
- Use the UUID path if needed: `/dev/disk/by-uuid/<uuid>`

**Force check (use with caution):**

```bash
btrfs check --force <device>
```

- `--force`: Bypasses the mount check. Only use this if you are certain the filesystem is not mounted and understand the risks.

### Diagnosis

Filter system logs and kernel messages to diagnose BTRFS-related events.

**Search journal logs by date range:**

```bash
journalctl --since "<date>" --until "<date>" | grep -i btrfs
```

Example:

```bash
journalctl --since "2026-01-01" --until "2026-01-02" | grep -i btrfs
```

**Search kernel ring buffer for BTRFS events:**

```bash
dmesg | grep -i btrfs
```
