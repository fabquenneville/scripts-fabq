# SSH

## Table of Contents

- [SSH](#ssh)
  - [Table of Contents](#table-of-contents)
  - [Placeholders](#placeholders)
  - [Connect with specific key](#connect-with-specific-key)
  - [Skip Host Key Verification](#skip-host-key-verification)
  - [SSH Key Management](#ssh-key-management)
  - [Verbose](#verbose)
  - [Enable root login](#enable-root-login)
  - [Firewall Configuration with firewalld](#firewall-configuration-with-firewalld)
  - [SCP (Secure Copy Protocol)](#scp-secure-copy-protocol)
  - [Send Remote Commands](#send-remote-commands)
  - [Test Connection, Add Alias, and Update Known Hosts](#test-connection-add-alias-and-update-known-hosts)
  - [Remove Offending SSH Keys](#remove-offending-ssh-keys)
  - [Change SSH Port](#change-ssh-port)
  - [Restart ssh](#restart-ssh)

## Placeholders

Replace the placeholders below with the appropriate values for your setup:

- **Connection**
  - Username: `<username>` (e.g., john)
  - Hostname: `<hostname>` (e.g., server.example.com)
  - IP address: `<ip>` (e.g., 192.168.1.100)
  - SSH port: `<port>` (e.g., 2222)
  - SSH key: `<keyfile>` (e.g., ~/.ssh/id_rsa)
  - Key comment: `<key-comment>` (e.g., john@example.com)
  - Host alias: `<alias>` (e.g., myserver)

- **Paths**
  - Local file: `<local-path>` (e.g., /home/user/file.txt)
  - Remote path: `<remote-path>` (e.g., /home/user/file.txt)
  - Local script: `<script-path>` (e.g., /home/user/script.sh)
  - Project name: `<project>` (e.g., myapp)

## Connect with specific key

```bash
ssh -i <keyfile> root@<hostname>
ssh -i <keyfile> <username>@<hostname>
```

## Skip Host Key Verification

Useful for ephemeral machines, VMs, or hosts that are frequently rebuilt where saved known_hosts entries would cause conflicts:

```bash
ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null <username>@<hostname>
```

- `StrictHostKeyChecking=no`: Automatically accepts new or changed host keys without prompting.
- `UserKnownHostsFile=/dev/null`: Discards the host key entirely — nothing is saved to `~/.ssh/known_hosts`.
- ⚠️ Do not use on untrusted networks — this disables MITM protection.

## SSH Key Management

**Generate a new RSA SSH key pair with a 4096-bit key length**

```bash
ssh-keygen -t rsa -b 4096 -C "<key-comment>" -f <keyfile>
```

- `ssh-keygen -t rsa -b 4096`: Generates a new RSA SSH key pair with a key size of 4096 bits for enhanced security.
- `-C "<key-comment>"`: Adds a comment to the key, usually the email address of the key owner.
- `-f <keyfile>`: Specifies the filename for the private key; the public key will be saved with the same name but with a `.pub` extension.

**Copy the generated SSH keys to the remote server**

```bash
scp <keyfile>* <username>@<hostname>:~/.ssh/
```

- `scp <keyfile>*`: Securely copies both the private and public keys to the remote server.
- `<username>@<hostname>:~/.ssh/`: Specifies the destination path on the remote server where the keys will be copied.

**Install the public key on the remote server for passwordless authentication**

```bash
ssh-copy-id <username>@<ip>
ssh-copy-id <username>@<hostname>
```

- `ssh-copy-id`: Installs the public key on the specified remote server, allowing for passwordless SSH login.

**Install the public key on multiple servers using a specific private key**

```bash
ssh-copy-id -i <keyfile> root@<ip>
ssh-copy-id -i <keyfile> <username>@<hostname>
```

- `-i <keyfile>`: Specifies which private key to use for authentication when copying the public key.

**Install the public key on the remote server for passwordless authentication manually**

This process is useful when `ssh-copy-id` is unavailable, or when you want more granular control over the setup. Follow these steps on the remote server:

1. Create the `.ssh` directory if it doesn't exist and set proper permissions:

   ```bash
   mkdir -p /home/<username>/.ssh
   chmod 700 /home/<username>/.ssh
   ```

2. Open the `authorized_keys` file and paste the public key (usually from `~/.ssh/id_rsa.pub` on the local machine):

   ```bash
   nano /home/<username>/.ssh/authorized_keys
   ```

3. Set the correct permissions for the `authorized_keys` file:

   ```bash
   chmod 600 /home/<username>/.ssh/authorized_keys
   ```

4. Ensure the ownership of the `.ssh` directory and its contents is set to the correct user:

   ```bash
   chown -R <username>:<username> /home/<username>/.ssh
   ```

## Verbose

Use the `-v` option to enable verbose mode, which provides detailed information about the connection process:

```bash
ssh -i <keyfile> -v root@<hostname>
ssh -i <keyfile> -v <username>@<hostname>
```

## Enable root login

Modify the SSH configuration file to allow root login:

```bash
nano /etc/ssh/sshd_config
```

**Edit the configuration as follows:**

```ini
PermitRootLogin prohibit-password
PermitRootLogin yes
```

## Firewall Configuration with firewalld

**Allow SSH service through the firewall**

```bash
firewall-cmd --permanent --zone=public --add-service=ssh
```

- `firewall-cmd`: The command-line tool used to manage `firewalld`.
- `--permanent`: Ensures that the change persists across reboots.
- `--zone=public`: Specifies the zone to which the rule applies. The "public" zone is typically used for untrusted networks.
- `--add-service=ssh`: Adds the SSH service to the specified zone, allowing incoming SSH connections.

**Examples of configuring other Linux firewalls**

1. **Using UFW (Uncomplicated Firewall)**

   ```bash
   ufw allow ssh
   ```

2. **Using iptables**

   ```bash
   iptables -A INPUT -p tcp --dport 22 -j ACCEPT
   ```

   - `-A INPUT`: Appends the rule to the INPUT chain.
   - `-p tcp --dport 22`: Matches TCP traffic on port 22.
   - `-j ACCEPT`: Accepts the specified traffic.

3. **Using nftables**

   ```bash
   nft add rule ip filter input tcp dport 22 accept
   ```

   - `add rule ip filter input`: Adds a new rule to the input chain of the filter table.
   - `tcp dport 22`: Matches TCP packets directed to port 22.
   - `accept`: Accepts the matching packets.

**Note:** Reload or restart the firewall service after making changes to apply the new rules.

## SCP (Secure Copy Protocol)

The `scp` command securely transfers files and directories between local and remote systems over SSH.

**Copy a local file to a remote server:**

```bash
scp <local-path> <username>@<hostname>:<remote-path>
```

**Copy a directory recursively:**

```bash
scp -r <local-path>/ <username>@<hostname>:<remote-path>/
```

- `-r`: Enables recursive copying of directories and their contents.

**Copy a file using a specific SSH key:**

```bash
scp -i <keyfile> <local-path> <username>@<hostname>:<remote-path>
```

- `-i <keyfile>`: Specifies the identity file (private key) for authentication.

## Send Remote Commands

**Run a local script on a remote server:**

```bash
ssh <username>@<hostname> 'bash -s' < <script-path>
```

**Remove a file:**

```bash
ssh <username>@<ip> "rm <remote-path>"
```

**Mount all filesystems:**

```bash
ssh root@<hostname> "mount -a"
```

**Reboot the remote server:**

```bash
ssh root@<hostname> "reboot -h now"
```

**Connect using a host key alias:**

```bash
ssh -o "HostKeyAlias=<alias>" root@<ip>
```

## Test Connection, Add Alias, and Update Known Hosts

**Test connection with host key alias:**

Commands to establish an SSH connection while specifying a host key alias. This helps avoid conflicts with existing entries in the `known_hosts` file.

```bash
ssh -o 'HostKeyAlias=<hostname>' <username>@<ip>
ssh -o 'HostKeyAlias=<alias>' <username>@<ip>
```

**Test host identity without authenticating:**

```bash
ssh -e none -o 'BatchMode=yes' -o 'HostKeyAlias=<alias>' <username>@<ip> /bin/true
```

- `-e none`: Disables escape character processing.
- `-o 'BatchMode=yes'`: Suppresses all prompts, suitable for scripts.
- `/bin/true`: Simple command that always returns success, confirming the connection without further actions.

**Retrieve public SSH keys from a remote server:**

```bash
ssh-keyscan -H <hostname>
```

- Fetches the server's public SSH keys without establishing a full session. Used to pre-populate `known_hosts`.

**Add an alias to SSH config for easy access:**

```ini
Host <alias>
    HostName <hostname>
    User <username>
    IdentityFile <keyfile>
```

## Remove Offending SSH Keys

When a server's host key has changed, remove the old entry from `known_hosts`.

**View known hosts:**

```bash
cat ~/.ssh/known_hosts
```

**Edit known hosts manually:**

```bash
nano ~/.ssh/known_hosts
```

**Update known hosts with current server key:**

```bash
ssh-keyscan -H <hostname> >> ~/.ssh/known_hosts
```

**Remove offending key by hostname or IP:**

```bash
ssh-keygen -R "<hostname>"
ssh-keygen -R "<ip>"
```

**Remove offending key specifying the known_hosts file:**

```bash
ssh-keygen -f "/home/<username>/.ssh/known_hosts" -R "<hostname>"
ssh-keygen -f "/root/.ssh/known_hosts" -R "<ip>"
ssh-keygen -f "/etc/ssh/ssh_known_hosts" -R "<hostname>"
```

## Change SSH Port

**1. Edit the SSH configuration file:**

```bash
nano /etc/ssh/sshd_config
```

Set the desired port:

```ini
Port <port>
```

**2. Create directory for systemd override:**

```bash
mkdir -p /etc/systemd/system/ssh.socket.d
```

**3. Create the override configuration file:**

```bash
nano /etc/systemd/system/ssh.socket.d/override.conf
```

```ini
[Socket]
ListenPort=<port>
```

**4. (Optional) Edit the Sockets Target Configuration**

You may also want to edit the sockets target configuration to ensure it points to the correct SSH socket:

```bash
nano /etc/systemd/system/sockets.target.wants/ssh.socket
```

**5. Restart the SSH service to apply the changes:**

```bash
systemctl restart sshd
```

**6. Verify the new port:**

```bash
netstat -tuln | grep LISTEN
```

## Restart ssh

```bash
systemctl restart sshd
```
