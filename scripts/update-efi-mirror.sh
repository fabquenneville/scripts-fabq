#!/bin/bash

# Identify the currently mounted EFI partition and its device
SOURCE_MOUNT="/boot/efi"
SOURCE_PART=$(findmnt -no SOURCE "$SOURCE_MOUNT")
SOURCE_UUID=$(findmnt -no UUID "$SOURCE_MOUNT")
SOURCE_DISK=$(lsblk -no PKNAME "$SOURCE_PART")
SOURCE_DISK_PATH="/dev/$SOURCE_DISK"

# Extract the backup UUID from fstab
BACKUP_UUID=$(grep "^#UUID=" /etc/fstab | grep "/boot/efi" | awk -F'[= ]' '{print $2}')

if [ -z "$BACKUP_UUID" ]; then
    echo "Error: Backup EFI UUID not found in /etc/fstab"
    exit 1
fi

if [ "$SOURCE_UUID" == "$BACKUP_UUID" ]; then
    echo "Error: Source and Backup UUIDs are identical. Check /etc/fstab."
    exit 1
fi

# Identify the physical disk for the backup UUID
BACKUP_PART=$(blkid -U "$BACKUP_UUID")
BACKUP_DISK=$(lsblk -no PKNAME "$BACKUP_PART")
BACKUP_DISK_PATH="/dev/$BACKUP_DISK"

# Define temporary mount point
TARGET_MOUNT=$(mktemp -d -t efi-sync.XXXXXXXXXX)

# Trap to ensure the directory is removed even if the script fails
trap 'rm -rf "$TARGET_MOUNT"' EXIT

# Mount, Sync, and Cleanup
if mount -U "$BACKUP_UUID" "$TARGET_MOUNT"; then
    echo "Syncing EFI files: $SOURCE_UUID -> $BACKUP_UUID"
    rsync -aqAX --delete "$SOURCE_MOUNT/" "$TARGET_MOUNT/"
    umount "$TARGET_MOUNT"
    echo "EFI Files Sync Complete."
else
    echo "Error: Could not mount backup EFI ($BACKUP_UUID)"
    exit 1
fi

# Ensure GRUB binary is installed on BOTH physical disks
echo "Updating GRUB bootloader on both physical disks..."
grub-install "$SOURCE_DISK_PATH" --recheck > /dev/null 2>&1
grub-install "$BACKUP_DISK_PATH" --recheck > /dev/null 2>&1

echo "Redundancy Complete: Files synced and GRUB updated on $SOURCE_DISK_PATH and $BACKUP_DISK_PATH."
