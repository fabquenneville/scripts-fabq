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
  - [System Management](#system-management)
    - [Change password of a tar/openssl archive](#change-password-of-a-taropenssl-archive)
    - [Verify two possibly identical folders recursively](#verify-two-possibly-identical-folders-recursively)
  - [NFS](#nfs)
  - [Network Diagnostics](#network-diagnostics)
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
- **`dmidecode`**: Retrieves hardware information from the BIOS. Use:
  - `dmidecode -t processor` for CPU details
  - `dmidecode -t memory` for RAM details
  - `dmidecode -t bios` for BIOS information

**CPU information**

```bash
lscpu
cat /proc/cpuinfo
grep -c 'model name' /proc/cpuinfo
```

- `lscpu`: Structured summary of CPU architecture, cores, threads, and NUMA topology.
- `cat /proc/cpuinfo`: Raw per-core details including model name, flags, and frequencies.
- `grep -c 'model name'`: Quick count of logical CPU cores.

**GPU information**

```bash
lspci | grep -i vga
```

**CPU frequency scaling driver**

Check which driver is managing CPU frequency scaling (e.g., `intel_pstate`, `acpi-cpufreq`):

```bash
cat /sys/devices/system/cpu/cpu0/cpufreq/scaling_driver
```

### Software Information

**Finding information on the Linux distribution**

- **`lsb_release -a`**: Displays detailed information about the Linux distribution, including the distributor ID, description, release number, and codename.
- **`cat /etc/debian_version`**: Displays the version of the Debian distribution if you're running a Debian-based system (like Ubuntu).
- **`cat /etc/os-release`**: Displays information about the operating system, such as the name, version, and ID of the distribution.
- **`cat /etc/*release`**: Searches for any files in the `/etc/` directory that contain the word `release` and displays their contents. This typically includes more detailed distribution information.
- **`cat /etc/*version`**: Similar to `cat /etc/*release`, but looks for files containing the word `version`. It can provide additional version-related details.
- **`hostnamectl`**: Displays system information related to the hostname and other metadata about the system. This may include the operating system, kernel version, and architecture.

**Finding Path to Binary**

To find the location of an executable binary, use:

```bash
type <binary-name>
```

This command will show the path to a binary executable, ex `composer`, if it's available in your `PATH`.

**Number of Words in a File**

To count the number of words in a file, use:

```bash
wc <filepath>
```

This command will show the number of words along with other details like lines and characters.

**Number of Lines in a File**

To count the number of lines in a file, use:

```bash
wc -l <filepath>
```

## User Management

### User Information

**Add users**

This variation of the adduser command uses the --gecos option to pre-fill the user's information (Full name, Room number, Work Phone, Home Phone, and Email) non-interactively, allowing you to automate user creation with predefined details.

```bash
adduser --gecos "<full-name>,,,<email>" <username>
```

This variation creates a system user with a Bash shell, no password login (--disabled-password), a specified home directory (`/home/<username>`), and adds the user to a new group, while using the --gecos option to set the full name as `<service-description>`.

```bash
adduser --system --shell /bin/bash --gecos '<service-description>' --group --disabled-password --home /home/<username> <username>
```

**List Users**

To list all users from the `/etc/passwd` file in alphabetical order, use:

```bash
awk -F':' '{ print $1}' /etc/passwd | sort
```

### Super User Management

**Disable Root Login**

To disable root login via SSH, perform the following steps:

1. **Edit the SSH Configuration File:**

   ```bash
   nano /etc/ssh/sshd_config
   ```

   Comment out the line containing `PermitRootLogin`.

2. **Change Shell for Root User:**

   ```bash
   nano /etc/passwd
   ```

   Find the line starting with `root` and change `/bin/bash` to `/sbin/nologin`.

   ```bash
   systemctl restart ssh
   ```

**Add User to Sudo Group**

```bash
adduser <username> sudo
```

**Update Sudoers File to Remove Password Requirement**

Edit the sudoers file with the default editor:

```bash
visudo
```

Edit the sudoers file with `nano`:

```bash
EDITOR=nano visudo
```

Add the following line to allow the user to execute commands without a password:

```bash
<username>     ALL=(ALL) NOPASSWD:ALL
```

### Switch User

**Switch to Another User as Sudoer**

```bash
sudo -i -u <username>
```

**Switch to Another User as Root**

```bash
su - <username>
```

**Run command as specific user**

```bash
sudo -u <username> <command>
```

**Change shell of a user**

```bash
chsh -s /bin/bash <username>
chsh -s /usr/sbin/nologin <username>
```

**Change user with specific shell**

```bash
sudo -u <username> bash
```

## System Management

**Ensure hostname or add alias**

```bash
nano /etc/hosts
# Add the hostname alias:
# 127.0.1.1 <hostname-intranet>

nano /etc/hostname
# Set the main hostname:
# 127.0.1.1 <hostname-intranet> <hostname-short>

hostnamectl set-hostname <hostname-intranet>
```

**Tar backup for a large number of small files**

Create a tar archive and transfer it to a remote server:

```bash
tar -c /path/to/dir | ssh <username>@<hostname-intranet> 'tar -xvf - -C /absolute/path/to/remotedir'
```

Compress and transfer a folder, then store it as a `.tar.gz` file:

```bash
tar zcvf - /folder | ssh <username>@<hostname-intranet> "cat > /backup/folder.tar.gz"
```

Transfer a compressed `.tar.gz` file and extract it on the remote server:

```bash
cat folder.tar.gz | ssh <username>@<hostname-intranet> "tar zxvf -"
```

Alternative: change directory on the remote server before extracting:

```bash
cat folder.tar.gz | ssh <username>@<hostname-intranet> "cd /path/to/dest/; tar zxvf -"
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
ln -s /usr/share/zoneinfo/<timezone> /etc/localtime
```

**Find a specific service**

```bash
systemctl list-units --type=service | grep <service-name>
```

**Bind mount a directory**

Make a directory available at another path, useful during chroot recovery or container setup:

```bash
mount --bind /dev /mnt/<newroot>/dev
```

**Chroot into another system**

Enter a mounted system's root as if it were the running OS. Useful for recovery, initramfs rebuilds, or bootloader fixes:

```bash
chroot /mnt/<newroot>
```

Typically preceded by binding the required pseudo-filesystems:

```bash
mount --bind /dev  /mnt/<newroot>/dev
mount --bind /proc /mnt/<newroot>/proc
mount --bind /sys  /mnt/<newroot>/sys
chroot /mnt/<newroot>
```

**Rebuild initramfs**

After kernel or driver changes, rebuild the initramfs and refresh the GRUB configuration:

```bash
update-initramfs -u
update-initramfs -u -k all
```

- `update-initramfs -u`: Rebuilds the initramfs for the currently running kernel.
- `-k all`: Rebuilds for all installed kernels.

**Rebuild initramfs for a specific kernel version:**

```bash
update-initramfs -c -k $(uname -r)
```

- `-c`: Create a new initramfs (instead of updating).
- `-k $(uname -r)`: Targets the currently running kernel version.

**Update GRUB:**

```bash
update-grub
```

- Scans for kernels and regenerates `/boot/grub/grub.cfg`.

### Change password of a tar/openssl archive

**Decrypt the archive**

To decrypt an `openssl`-encrypted archive using a password stored in a file:

1. **Store your password in a temporary file:**

   ```bash
   nano $HOME/<filename>
   ```

2. **Decrypt the archive:**

   ```bash
   openssl aes-256-cbc -d -pbkdf2 -in <archive>.tar.gz -out <archive>.tar -pass file:$HOME/<filename>
   ```

3. **Re-encrypt the archive with a new password:**

   ```bash
   nano $HOME/<filename>
   openssl aes-256-cbc -e -pbkdf2 -in <archive>.tar -out <archive>-new.tar.gz -pass file:$HOME/<filename>
   rm $HOME/<filename>
   ```

**Decode / Extract**

Decrypt and extract the contents directly into a directory:

```bash
nano $HOME/<filename>
openssl aes-256-cbc -d -pbkdf2 -in <archive>.tar.gz -pass file:<filename> | tar xz -C .
rm $HOME/<filename>
```

### Verify two possibly identical folders recursively

**With `diff`**

```bash
diff -r <dir1>/ <dir2>/
```

**With `rsync`**

Dry run — shows differences without copying any data:

```bash
rsync -avn <dir1>/ <dir2>/
```

- `-n`: dry run, no changes made.

**With `cmp`**

```bash
#!/bin/bash

dir1="<dir1>/"
dir2="<dir2>/"

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

## NFS

**Show NFS exports from a server:**

```bash
showmount -e <hostname>
showmount -e localhost
```

**List active exports and their options on the server:**

```bash
exportfs -v
```

## Network Diagnostics

**Measure HTTP response timing:**

Breaks down the full request lifecycle — useful for diagnosing DNS, TLS, or TTFB issues:

```bash
curl -o /dev/null -s -w \
  'Lookup: %{time_namelookup}s\nConnect: %{time_connect}s\nAppConnect: %{time_appconnect}s\nTTFB: %{time_starttransfer}s\nTotal: %{time_total}s\n' \
  https://<hostname>
```

- `time_namelookup`: DNS resolution time.
- `time_connect`: TCP connection time.
- `time_appconnect`: TLS handshake time.
- `time_starttransfer`: Time to first byte (TTFB).
- `-o /dev/null`: Discards the response body.

**High-frequency ping:**

Flood-style ping to stress-test latency or detect intermittent packet loss:

```bash
ping -i 0.002 <host>
```

- `-i 0.002`: Send a packet every 2ms. Requires root.

**Jumbo frame ping:**

Test whether the network path supports large MTU frames (useful for diagnosing MTU mismatches):

```bash
ping -s 1472 -i 0.01 <host>
```

- `-s 1472`: Payload size of 1472 bytes (1472 + 28-byte IP/ICMP header = 1500-byte MTU).
- Increase `-s` to test jumbo frames (e.g., `-s 8972` for 9000-byte MTU).

## Diagnosis

### Debian Upgrade Issues

**Apt Logs**

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

**Journal Filtering by Date and Keyword**

Search logs within a specific time window:

```bash
journalctl --since "<date>" --until "<date>" | grep -i <keyword>
```

Example:

```bash
journalctl --since "2026-01-01" --until "2026-01-02" | grep -i btrfs
```

**Kernel microcode events:**

```bash
journalctl -k | grep -i "microcode"
```

- `-k`: Show only kernel messages (equivalent to `dmesg` output via the journal).

## Fonts

**Download and Install Fonts**

1. **Download the Font Archive:**

   ```bash
   wget https://<font-archive-url>
   ```

2. **Extract the Font Files:**

   ```bash
   tar -xzvf <font-archive>.tar.gz
   ```

3. **Copy the Font Files:**

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

```bash
sudo su -
fc-cache -fv
fc-cache -frv
```

- **`-f`**: Force re-generation of cache files, overriding timestamp checking.
- **`-r`**: Erase all existing cache files and rescan.
- **`-v`**: Display status information while busy.
