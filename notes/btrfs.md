# BTRFS

## Table of Contents

- [BTRFS](#btrfs)
  - [Table of Contents](#table-of-contents)
  - [Information on Drives](#information-on-drives)
  - [Information on Filesystem](#information-on-filesystem)
  - [Backup Procedures](#backup-procedures)
  - [Recovery](#recovery)
  - [Drive Manipulation](#drive-manipulation)
    - [Replace Drives](#replace-drives)
  - [Filesystem Manipulation](#filesystem-manipulation)
    - [Upgrading Btrfs block group cache to V2](#upgrading-btrfs-block-group-cache-to-v2)
  - [Balances](#balances)
  - [Scrub](#scrub)
  - [Snapshots](#snapshots)

## Information on Drives

**List of Drives and Mountpoints**

To check all attached drives:

```bash
ls /dev/sd*
ls /dev/nv*
```

To view mountpoints and drive details such as names, sizes, and mountpoints:

```bash
lsblk
df -h
cat /etc/fstab
```

**Drive Information**

To get detailed information and serial number of a specific drive:

```bash
smartctl -i /dev/sdc
```

**Find the Device Path from UUID**

Using lsblk:

```bash
lsblk -o NAME,UUID,MOUNTPOINT
```

Using blkid:

```bash
blkid | grep <UUID>
```

## Information on Filesystem

**Show Basic Filesystem Information**

To display basic information (size, IDs, paths, etc.) for the specified mountpoint:

```bash
btrfs fi show /mnt/media/
```

**Display Detailed Usage Information**

To show detailed usage information (allocated, unallocated, etc.) for the specified mountpoint:

```bash
btrfs fi usage /mnt/media
```

**Display Detailed Allocation Information**

To view detailed allocation information (block groups, used space) for the specified mountpoint:

```bash
btrfs fi df /mnt/media
```

**Get Detailed Device Usage Statistics**

To get detailed device usage statistics (physical size, unallocated space, RAID levels, etc.) for a BTRFS filesystem:

```bash
btrfs device usage /mnt/media
```

**Scan and Display BTRFS Information**

To scan and display BTRFS information for all devices or a specific drive:

```bash
btrfs device scan /dev/sda/
```

**Retrieve Statistics and Error Information**

To get statistics and error information (read errors, write errors, flush errors, etc.) for the specified mountpoint:

```bash
btrfs device stats /mnt/media
```

**List BTRFS Subvolumes**

To list BTRFS subvolumes:

```bash
btrfs subvolume list /
btrfs subvolume list /home/fabrice
btrfs subvolume list /mnt/workbench
```

**Default Subvolume**

To check if a non-standard subvolume is set as the default:

```bash
btrfs subvol get-default /mnt/tmp/
btrfs subvol list /mnt/tmp/
```

To change the default subvolume if a non-standard one is set:

```bash
btrfs subvol set-default 257 /mnt/tmp/
```

**Verify Current Cache Version**

To check if your filesystem is using cache V1 by device:

```bash
btrfs inspect-internal dump-super -f /dev/<device> | grep cache_generation
```

To check if your filesystem is using cache V1 by UUID:

```bash
btrfs inspect-internal dump-super -f $(blkid -U <UUID>) | grep cache_generation
```

- If cache_generation is present, it indicates cache V1 is in use. If it's absent, the filesystem is already using V2.

## Backup Procedures

**Desktop Backup: Root and Home**

1. Mount snapshot location:

   ```bash
   mount UUID=394decca-4780-47c9-9ae3-e4d03681a791 -o subvol=snapshots /mnt/snapshots
   ```

2. Create snapshots for root and home:

   ```bash
   btrfs subvolume snapshot / "/mnt/snapshots/root/2021-05-23 - Fedora 34 upgrade"
   btrfs subvolume snapshot /home "/mnt/snapshots/home/2021-05-23 - Fedora 34 upgrade"
   ```

3. Unmount after creating snapshots:

   ```bash
   umount /mnt/snapshots
   ```

**Data Backup: Workbench, Documents, Education**

1. Mount snapshot location:

   ```bash
   mount UUID=72e1770a-9fc0-461e-88d3-db640ff53dd9 -o subvol=snapshots /mnt/snapshots
   ```

2. Create snapshots for multiple directories:

   ```bash
   btrfs subvolume snapshot /mnt/workbench "/mnt/snapshots/workbench/2021-05-23 - Fedora 34 upgrade"
   btrfs subvolume snapshot /home/fabrice/Documents "/mnt/snapshots/Documents/2021-05-23 - Fedora 34 upgrade"
   btrfs subvolume snapshot /home/fabrice/Education "/mnt/snapshots/Education/2021-05-23 - Fedora 34 upgrade"
   ```

3. Unmount after creating snapshots:

   ```bash
   umount /mnt/snapshots
   ```

**STOR1 Fedora Backup**

1. Mount snapshot location:

   ```bash
   mount UUID=e4fd608e-cfe8-4c10-b6d0-03b05bae8aa6 -o subvol=snapshots /mnt/snapshots
   ```

2. Create snapshot:

   ```bash
   btrfs subvolume snapshot / "/mnt/snapshots/root/2021-06-06"
   ```

3. Unmount after creating snapshot:

   ```bash
   umount /mnt/snapshots
   ```

**STOR1 Debian Backup**

1. Mount snapshot location:

   ```bash
   mount UUID=c9a77f3c-626f-47bd-b4e3-9a094bea287f -o subvol=snapshots /mnt/snapshots
   ```

2. Create snapshot:

   ```bash
   btrfs subvolume snapshot / "/mnt/snapshots/root/2021-07-12 - post mostly setup"
   ```

3. Unmount after creating snapshot:

   ```bash
   umount /mnt/snapshots
   ```

**STOR2 Backup**

1. Mount snapshot location:

   ```bash
   mount UUID=30bd5e0e-e781-4e87-8fb8-ea5606403b15 -o subvol=snapshots /mnt/snapshots
   ```

2. Create snapshot:

   ```bash
   btrfs subvolume snapshot / "/mnt/snapshots/root/2021-06-06 - Fedora 34"
   ```

3. Unmount after creating snapshot:

   ```bash
   umount /mnt/snapshots
   ```

## Recovery

**Mount a Subvolume with Recovery Options**

```bash
mount -o recovery,subvol=backups UUID=aa5c1d34-ecba-42a9-9339-8f7879d47536 /mnt/tmp
```

**Clear Cache During Mount**

```bash
mount -o clear_cache,subvol=backups UUID=aa5c1d34-ecba-42a9-9339-8f7879d47536 /mnt/tmp
```

**Data Restoration**

To restore data using `btrfs restore`:

```bash
btrfs restore -D /dev/sdb
```

## Drive Manipulation

**Mount Whole Drive**

```bash
mount UUID=c9a77f3c-626f-47bd-b4e3-9a094bea287f /mnt/tmp
```

**Mount Subvolume by ID**

```bash
btrfs subvol list /
mount -o subvolid=5 /dev/disk/by-uuid/7a22514b-594a-43a3-8fdd-4df1530b5465 /mnt
```

**Add a New Drive**

To add a new drive to an existing BTRFS setup:

```bash
btrfs device add /dev/sdf /mnt/media/
```

**Resize Filesystem**

```bash
btrfs filesystem resize 1:max /mnt/media/
```

**Create Subvolumes**

```bash
btrfs subvol create /mnt/tmp/root
btrfs subvol create /mnt/tmp/snapshots
```

### Replace Drives

**Replace the source drive with the target drive:**

This command will start the replacement process where the data from the old drive (`/dev/sdb`) is copied over to the new drive (`/dev/sdj`).

```bash
btrfs replace start /dev/sdb /dev/sdj /mnt/media
```

- `/dev/sdb`: Source drive to be replaced.
- `/dev/sdj`: Target drive to replace the source drive.
- `/mnt/media`: Mount point of the BTRFS filesystem.

**Monitor the progress of the replacement:**

Once the replacement process has started, you can monitor its progress with the following command:

```bash
btrfs replace status /mnt/media
```

- This will print the current status of the drive replacement operation, showing how much data has been migrated.

**Monitor progress interactively:**

For a more detailed, interactive status view of the replacement process, use the `-i` option:

```bash
btrfs replace status -i /mnt/media
```

- `-i`: This flag provides an interactive mode where the progress is updated in real time.

**Notes:**

- The `btrfs replace` command allows you to replace a faulty or underperforming drive without unmounting the filesystem, making it ideal for live systems.
- It can be used for upgrading storage by replacing smaller drives with larger ones, or for replacing failing drives.
- Ensure that the target drive has enough space to accommodate the data from the source drive.

## Filesystem Manipulation

### Upgrading Btrfs block group cache to V2

**From a running system non-root filesystems**

```bash
mount -o remount,clear_cache,space_cache=v2 /mnt/<mount-point>
```

**From a running system on root**

Check if your filesystem is using cache V1:

```bash
btrfs inspect-internal dump-super -f /dev/<device> | grep cache_generation
```

Enable Cache V2

```bash
nano /etc/default/grub
# Locate the line starting with GRUB_CMDLINE_LINUX_DEFAULT or GRUB_CMDLINE_LINUX and add the following options:
rootflags=clear_cache,space_cache=v2
```

Example:

```bash
GRUB_CMDLINE_LINUX_DEFAULT="quiet splash rootflags=clear_cache,space_cache=v2"
```

```bash
update-grub
reboot
```

Verify the Change

```bash
btrfs inspect-internal dump-super -f /dev/<device> | grep cache_generation
```

Remove `clear_cache` Option

```bash
nano /etc/default/grub
# Remove clear_cache from the rootflags.
update-grub
```

**From a live system**

```bash
apt update
apt install btrfs-progs
lsblk -o NAME,UUID
blkid
mount -o clear_cache,space_cache=v2 /dev/disk/by-uuid/<UUID> /mnt
btrfs inspect-internal dump-super -f /dev/disk/by-uuid/<UUID> | grep cache_generation
umount /mnt

```

## Balances

**Perform a Full Balance with Minimal Usage**

```bash
btrfs balance start --full-balance -dusage=0 -musage=0 /mnt/media/
```

- `--full-balance` is default but with a warning if not specified.
- `-dusage=0` means only data block groups that are nearly empty (0% full) will be balanced.
- `-musage=0` means only metadata block groups that are nearly empty (0% full) will be balanced.

**Perform a Full Balance on Partially Used Blocks**

```bash
btrfs balance start --full-balance -dusage=50 -musage=50 /mnt/media/
```

- `-dusage=50` means data block groups that are less than 50% full will be included in the balance process.
- `-musage=50` means metadata block groups that are less than 50% full will also be balanced.

**Balance data in the background**

```bash
btrfs balance start --bg -d /mnt/media
```

**Balance metadata in the background**

```bash
btrfs balance start --bg -m /mnt/media
```

**Balance data and metadata in the background**

```bash
btrfs balance start --bg --full-balance -dusage=0 -musage=0 /mnt/media/
```

**To balance 100 chunks of data**

```bash
btrfs balance start --bg -dlimit=100 /mnt/media/
```

**Cancel Balance Operation**

```bash
btrfs balance cancel /mnt/media/
```

**Monitor Balance Status**

```bash
btrfs balance status /mnt/media/
```

## Scrub

**Start a Scrub Operation**

To start a scrub operation to verify data integrity:

```bash
btrfs scrub start /mnt/media/
```

**Check Scrub Status**

To check the progress and status of the ongoing scrub:

```bash
btrfs scrub status /mnt/media/
```

**Cancel a Scrub Operation**

```bash
btrfs scrub cancel /mnt/media/
```

## Snapshots

**Create Snapshots**

1. **Mount snapshot subvolume**

```bash
mount UUID=c9a77f3c-626f-47bd-b4e3-9a094bea287f -o subvol=snapshots /mnt/snapshots
```

2. **Create a new snapshot**

```bash
btrfs subvolume snapshot / "/mnt/snapshots/root/2021-06-26 - Debian install"
```

3. **Unmount after creating snapshots**

```bash
umount /mnt/snapshots
```

**Delete Snapshots**

1. **Mount subvolume containing snapshots**

   ```bash
   mount -o subvol=snapshots /dev/disk/by-uuid/7a22514b-594a-43a3-8fdd-4df1530b5465 /mnt/snapshots/
   ```

2. **List available snapshots**

   ```bash
   btrfs subvol list /mnt/snapshots/
   ```

3. **Delete the desired snapshot**

   ```bash
   btrfs subvolume delete /mnt/snapshots/@rootfs/2024-09-15
   ```

4. **Unmount after deleting snapshots**

   ```bash
   umount /mnt/snapshots/
   ```
