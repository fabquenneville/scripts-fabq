# Linux

## Table of Contents

- [Linux](#linux)
  - [Table of Contents](#table-of-contents)
  - [System Information](#system-information)
    - [Hardware Information](#hardware-information)
    - [Software Information](#software-information)
  - [User Management](#user-management)
    - [User Information](#user-information)
    - [Super User Management](#super-user-management)
    - [Switch User](#switch-user)
  - [USB Devices](#usb-devices)
    - [Test USB Key](#test-usb-key)
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
   ```bash
   cp -v *.ttf ~/.local/share/fonts/
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
