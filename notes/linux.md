# Linux

## Table of Contents

- [Linux](#linux)
  - [Table of Contents](#table-of-contents)
  - [System Information](#system-information)
    - [Hardware Information](#hardware-information)
    - [Software Information](#software-information)
- [Commands to Get Information About Linux Version, Kernel Version, and Release](#commands-to-get-information-about-linux-version-kernel-version-and-release)
  - [User Management](#user-management)
    - [User Information](#user-information)
    - [Super User Management](#super-user-management)
    - [Switch User](#switch-user)
  - [System Management](#system-management)
    - [Change password of a tar/openssl archive](#change-password-of-a-taropenssl-archive)
    - [Verify two possibly identical folders recursively](#verify-two-possibly-identical-folders-recursively)
  - [USB Devices](#usb-devices)
    - [Test USB Key](#test-usb-key)
  - [Diagnosis](#diagnosis)
    - [Debian Upgrade Issues](#debian-upgrade-issues)
    - [Wayland Issues](#wayland-issues)
  - [Fonts](#fonts)

## System Information

### Hardware Information

To gather detailed information about your hardware, use the following commands:

- **`lscpu`**: Displays information about the CPU architecture, including details about cores, threads, and CPU family.
- **`lshw`**: Provides a comprehensive listing of hardware components. Use `lshw -short` for a more concise view.
- **`hwinfo`**: Offers detailed information about hardware components and can be more verbose than `lshw`.
- **`lsscsi`**: Lists SCSI devices, including disks and other SCSI-attached hardware.
- **`lsusb`**: Shows information about USB devices connected to your system.
- **`lsblk`**: Lists block devices such as hard drives and their partitions.
- **`df -H`**: Displays disk space usage in a human-readable format.
- **`fdisk -l`**: Lists all partitions on the system.
- **`dmidecode`**: Retrieves hardware information from the BIOS. Use:
  - `dmidecode -t processor` for CPU details
  - `dmidecode -t memory` for RAM details
  - `dmidecode -t bios` for BIOS information

### Software Information

**Finding information on the Linux distribution**

# Commands to Get Information About Linux Version, Kernel Version, and Release

- **`lsb_release -a`**: Displays detailed information about the Linux distribution, including the distributor ID, description, release number, and codename.
- **`cat /etc/debian_version`**: Displays the version of the Debian distribution if you're running a Debian-based system (like Ubuntu).
- **`cat /etc/os-release`**: Displays information about the operating system, such as the name, version, and ID of the distribution.
- **`cat /etc/*release`**: Searches for any files in the `/etc/` directory that contain the word `release` and displays their contents. This typically includes more detailed distribution information.
- **`cat /etc/*version`**: Similar to `cat /etc/*release`, but it looks for files containing the word `version`. It can provide additional version-related details.
- **`hostnamectl`**: Displays system information related to the hostname and other metadata about the system. This may include the operating system, kernel version, and architecture.

**Finding Path to Binary**

To find the location of an executable binary, use:

```bash
type composer
```

This command will show the path to the `composer` executable if it's available in your `PATH`.

**Number of Words in a File**

To count the number of words in a file, use:

```bash
wc filepath
```

This command will show the number of words along with other details like lines and characters.

**Number of Lines in a File**

To count the number of lines in a file, use:

```bash
wc -l filepath
```

This command will display the number of lines in the specified file.

## User Management

### User Information

**Add users**

This variation of the adduser command uses the --gecos option to pre-fill the user's information (Full name, Room number, Work Phone, Home Phone, and Email) non-interactively, allowing you to automate user creation with predefined details.

```bash
adduser --gecos "Fabrice Quenneville,,,fabrice@fabq.ca" fabrice
```

This variation of the adduser command creates a system user named "aptly" with a Bash shell, no password login (--disabled-password), a specified home directory (/home/aptly), and adds the user to a new group, while using the --gecos option to set the full name as "Aptly repository".

```bash
adduser --system --shell /bin/bash --gecos 'Aptly repository' --group --disabled-password --home /home/aptly aptly
```

**List Users**

To list all users from the `/etc/passwd` file, use:

```bash
awk -F':' '{ print $1}' /etc/passwd | sort
```

This command extracts the usernames from the `/etc/passwd` file and sorts them in alphabetical order.

### Super User Management

**Disable Root Login**

To disable root login via SSH, perform the following steps:

1. **Edit the SSH Configuration File:**

   ```bash
   nano /etc/ssh/sshd_config
   ```

   Comment out the line containing `PermitRootLogin` by adding a `#` at the beginning of the line.

2. **Change Shell for Root User:**

   ```bash
   nano /etc/passwd
   ```

   Find the line starting with `root` and change `/bin/bash` to `/sbin/nologin` to disable login for the root user.

   Save and close the file. Restart the SSH service for changes to take effect:

   ```bash
   systemctl restart ssh
   ```

**Sudo Management**

**Add User to Sudo Group**

```bash
adduser fabrice sudo
```

**Update Sudoers File to Remove Password Requirement**

Edit the sudoers file:

```bash
visudo
```

Add the following line to allow the user to execute commands without a password:

```bash
fabrice     ALL=(ALL) NOPASSWD:ALL
```

### Switch User

**Switch to Another User as Sudoer**

```bash
sudo -i -u postgres
```

This command switches to the `postgres` user with sudo privileges.

**Switch to Another User as Root**

```bash
su - postgres
```

This command switches to the `postgres` user with root privileges.

**Run command as specific user**

```bash
sudo -u www-data somecommand and arguments
```

**Change shell of a user**

```bash
chsh -s /bin/bash www-data
chsh -s /usr/sbin/nologin www-data
```

**Change user with specific shell**

```bash
sudo -u www-data bash
```

## System Management

**Ensure hostname or add alias**

Set or update the hostname for your server.

```bash
nano /etc/hosts
# Add the hostname alias:
# 127.0.1.1 local.servername.domain.com

nano /etc/hostname
# Set the main hostname:
# 127.0.1.1 servername.domain.com servername

hostnamectl set-hostname servername.domain.com
```

**Tar backup for a large number of small files**

These commands create backups using `tar` and transfer them securely over SSH.

Create a tar archive and transfer it to a remote server:

```bash
tar -c /path/to/dir | ssh fabrice@servername.domain.com 'tar -xvf - -C /absolute/path/to/remotedir'
```

Compress and transfer a folder, then store it as a .tar.gz file:

```bash
tar zcvf - /folder | ssh fabrice@servername.domain.com "cat > /backup/folder.tar.gz"
```

Transfer a compressed .tar.gz file and extract it on the remote server:

```bash
cat folder.tar.gz | ssh fabrice@servername.domain.com "tar zxvf -"
```

Alternative method: change directory on the remote server before extracting:

```bash
cat folder.tar.gz | ssh fabrice@servername.domain.com "cd /path/to/dest/; tar zxvf -"
```

**List time zones**

Use `timedatectl` to list available time zones or check the current settings.

```bash
timedatectl
timedatectl list-timezones
```

**Configure time zone**

Configure the time zone using `timedatectl` or by manually setting a symbolic link to `/etc/localtime`.

```bash
timedatectl set-timezone "America/Toronto"
```

Alternatively, manually set the time zone by linking the correct file:

```bash
mv /etc/localtime /etc/localtime-old
ln -s /usr/share/zoneinfo/America/Toronto /etc/localtime
```

**Find a specific service**

Search for a specific service running on your system.

```bash
systemctl list-units --type=service | grep php
```

### Change password of a tar/openssl archive

**Decrypt the archive**

To decrypt an `openssl`-encrypted archive using a password stored in a file:

1. **Store your password in this file.**
   ```bash
   nano $HOME/xyz001.txt
   ```
2. **Decrypt the archive**  
   Decrypt the archive using the password stored in xyz001.txt.

   ```bash
   openssl aes-256-cbc -d -pbkdf2 -in servername-backup.tar.gz -out servername-backup.tar -pass file:$HOME/xyz001.txt
   ```

3. **Re-encrypt the archive with a new password**

   ```bash
   nano $HOME/xyz001.txt
   openssl aes-256-cbc -e -pbkdf2 -in servername-backup.tar -out servername-backup-new.tar.gz -pass file:$HOME/xyz001.txt
   rm $HOME/xyz001.txt
   ```

**Decode / Extract**

To decrypt and extract the contents of an encrypted archive directly into a directory:

```bash
nano $HOME/xyz001.txt
openssl aes-256-cbc -d -pbkdf2 -in servername-backup.tar.gz -pass file:xyz001.txt | tar xz -C .
rm $HOME/xyz001.txt
```

### Verify two possibly identical folders recursively

**With `diff`**

Check for differences between two directories, comparing all files recursively:

```bash
diff -r servername-files/data/servername-repositories/ servername-repositories/
```

Outputs any differences found between the two directories.

**With `rsync`**

Use `rsync` to show differences without copying any data:

```bash
rsync -avn servername-files/data/servername-repositories/ servername-repositories/
```

- The `-n` flag means this is a dry run, which won’t make any changes.

**With `cmp`**

This script compares files in two directories and identifies any differences between matching file names.

```bash
#!/bin/bash

dir1="servername-files/data/servername-repositories/"
dir2="servername-repositories/"

# Check if both directories exist before proceeding.
if [ ! -d "$dir1" ] || [ ! -d "$dir2" ]; then
    echo "One or both directories do not exist."
    exit 1
fi

# Iterate through all files in dir1 and compare with corresponding files in dir2.
for file1 in $(find "$dir1" -type f); do
    file2="${file1/$dir1/$dir2}"
    if [ ! -f "$file2" ]; then
        echo "File $file2 not found."
    else
        cmp --silent "$file1" "$file2" || echo "Files $file1 and $file2 differ."
    fi
done
```

## USB Devices

### Test USB Key

**Device Information**

Check if the system recognizes the device and show the latest system messages related to USB devices being connected:

```bash
lsusb
dmesg | tail -n 20
```

**Find Mount Points and Device Information**

Identify mount points, partitions, and other relevant details of mounted devices:

```bash
lsblk -f
df -h | grep /dev/sdc
findmnt /dev/sdc1
mount | grep /dev/sd
```

**Print Detailed Information About the USB Key**

View detailed partition and disk information:

```bash
fdisk -l /dev/sdc
```

**Test the File System**

Check and repair the filesystem on the USB key:

```bash
fsck /dev/sdc1
```

**Test Data Integrity**

Perform read/write tests to ensure the integrity of the USB key:

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

Identify any bad sectors on the USB key:

- **Read-only test**:

  ```bash
  badblocks -v /dev/sdc
  ```

- **Non-destructive read-write test**:

  ```bash
  badblocks -nsv /dev/sdc
  ```

  - The `-n` option performs a non-destructive read-write test.
  - The `-s` option shows progress.
  - The `-v` option is for verbose output.

**Perform a SMART Test**

Run SMART diagnostics to test the health of the USB key:

1. **Start a short SMART test**:

   ```bash
   smartctl -t short /dev/sdc
   ```

2. **View test results**:

   ```bash
   smartctl -a /dev/sdc
   ```

**Benchmark the Speed**

Measure the read speed of the USB key:

```bash
hdparm -t /dev/sdc
```

**Unmount and Safely Remove**

Unmount the USB key and safely remove it from the system:

```bash
umount /mnt/usb
eject /dev/sdc
```

**Switching two USB keys**

The following commands copy data between two USB drives, format one of them, and restore the data.

```bash
cp -r /media/fabrice/465A-759B "/tmp/Michael Allison"
umount /dev/sdc1
mkfs.vfat /dev/sdc1

umount /dev/sdc1
dd if=/dev/sdc of=/tmp/usb_image.img bs=4M status=progress
mkfs.vfat /dev/sdc1

cp -r "/tmp/Michael Allison" /media/fabrice/D67D-ADF8
umount /dev/sdc1

dd if=/tmp/usb_image.img of=/dev/sdc bs=4M status=progress
sync
```

## Diagnosis

### Debian Upgrade Issues

**Apt Logs**

View the APT logs to check for package installation and updates history:

```bash
less /var/log/apt/history.log
```

### Wayland Issues

**System Logs**

Examine system logs and hardware information for troubleshooting Wayland issues:

```bash
lspci -k | grep -A 3 -E "(VGA|3D)"
lsmod | grep -i "drm\|gpu\|nouveau\|amdgpu\|i915"
glxinfo | grep "OpenGL version"
```

**GPU Information**

Search the system logs for any errors or warnings related to GPU and Wayland:

```bash
journalctl -b | grep -i "drm\|gpu\|display\|wayland\|monitor"
journalctl -b | grep -i "gnome-shell"
```

## Fonts

**Download and Install Fonts**

1. **Download the Font Archive**:

   ```bash
   wget https://path/to/font/archive.tar.gz
   ```

2. **Extract the Font Files**:

   ```bash
   tar -xzvf font-archive.tar.gz
   ```

3. **Copy the Font Files to the Local Fonts Directory**:

   **Local font directory**

   ```bash
   cp -v *.ttf ~/.local/share/fonts/
   ```

   **Global font directory - Package manager managed**

   ```bash
   cp -v *.ttf /usr/share/fonts
   ```

   **Global font directory - User managed**

   ```bash
   cp -v *.ttf /usr/local/share/fonts
   ```

**Update the Font Cache**

**Force a Reload of the Installed Font Cache**:

```bash
sudo su -
fc-cache -fv
fc-cache -frv
```

- **`-f`**: Force re-generation of apparently up-to-date cache files, overriding the timestamp checking.
- **`-r`**: Erase all existing cache files and rescan.
- **`-v`**: Display status information while busy.
