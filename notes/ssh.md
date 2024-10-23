# SSH

## Table of Contents

- [SSH](#ssh)
  - [Table of Contents](#table-of-contents)
  - [Connect with specific key](#connect-with-specific-key)
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

## Connect with specific key

```bash
ssh -i /home/fabrice/.ssh/fabquenneville root@servername.fabq.ca
ssh -i /home/fabrice/.ssh/fabquenneville fabrice@servername.fabq.ca
```

## SSH Key Management

**Generate a new RSA SSH key pair with a 4096-bit key length**

```bash
ssh-keygen -t rsa -b 4096 -C "fabrice@fabq.ca" -f ~/.ssh/fabrice@fabq.ca
```

- `ssh-keygen -t rsa -b 4096`: This command generates a new RSA SSH key pair with a key size of 4096 bits for enhanced security.
- `-C "fabrice@fabq.ca"`: This option adds a comment to the key, usually the email address of the key owner.
- `-f ~/.ssh/fabrice@fabq.ca`: This specifies the filename for the private key; the public key will be saved with the same name but with a `.pub` extension.

**Copy the generated SSH keys to the remote server**

```bash
scp ~/.ssh/fabrice@fabq.ca* fabrice@servername.fabq.ca:~/.ssh/
```

- `scp ~/.ssh/fabrice@fabq.ca*`: This command securely copies both the private and public keys to the remote server.
- `fabrice@servername.fabq.ca:~/.ssh/`: Specifies the destination path on the remote server where the keys will be copied.

**Install the public key on the remote server for passwordless authentication**

```bash
ssh-copy-id fabrice@192.168.1.100
ssh-copy-id fabrice@servername.fabq.ca
```

- `ssh-copy-id "fabrice@servername.fabq.ca"`: This command installs the public key on the specified remote server, allowing for passwordless SSH login.

**Install the public key on multiple servers using specific private key**

```bash
ssh-copy-id -i /home/fabrice/.ssh/fabquenneville root@192.168.1.100
ssh-copy-id -i /home/fabrice/.ssh/fabquenneville fabrice@servername.fabq.ca
```

- `ssh-copy-id -i /home/fabrice/.ssh/fabquenneville`: This specifies which private key to use for authentication when copying the public key.
- `root@192.168.1.100` and `fabrice@servername.fabq.ca`: These commands install the public key on the respective remote servers, allowing for secure, passwordless access.

## Verbose

- Use the 'ssh' command with the '-v' option to enable verbose mode, which provides detailed information about the connection process.

```bash
ssh -i /home/fabrice/.ssh/fabquenneville -v root@servername.fabq.ca
ssh -i /home/fabrice/.ssh/fabquenneville -v fabrice@servername.fabq.ca
```

## Enable root login

- Modify the SSH configuration file to allow root login.

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

- `firewall-cmd`: This is the command-line tool used to manage `firewalld`.
- `--permanent`: This option ensures that the change persists across reboots.
- `--zone=public`: Specifies the zone to which the rule applies. The "public" zone is typically used for untrusted networks.
- `--add-service=ssh`: This adds the SSH service to the specified zone, allowing incoming SSH connections.

**Examples of configuring other Linux firewalls**

1. **Using UFW (Uncomplicated Firewall)**

   **Allow SSH traffic**

   ```bash
   ufw allow ssh
   ```

   - This command allows incoming SSH traffic through the firewall. UFW is designed to simplify the process of managing a firewall.

2. **Using iptables**

   **Allow SSH traffic**

   ```bash
   iptables -A INPUT -p tcp --dport 22 -j ACCEPT
   ```

   - `iptables`: This is a low-level tool for managing Linux firewalls.
   - `-A INPUT`: Appends the rule to the INPUT chain.
   - `-p tcp`: Specifies that this rule applies to TCP packets.
   - `--dport 22`: Indicates that this rule applies to traffic on port 22 (the default SSH port).
   - `-j ACCEPT`: Instructs the firewall to accept the specified traffic.

3. **Using nftables**

   **Allow SSH traffic**

   ```bash
   nft add rule ip filter input tcp dport 22 accept
   ```

   - `nft`: The command-line tool for interacting with the nftables framework.
   - `add rule ip filter input`: Adds a new rule to the input chain of the filter table.
   - `tcp dport 22`: Matches TCP packets directed to port 22.
   - `accept`: Specifies that the matching packets should be accepted.

**Note:** Be sure to reload or restart the firewall service after making changes to apply the new rules effectively.

## SCP (Secure Copy Protocol)

- The `scp` command is used to securely transfer files and directories between local and remote systems over SSH.

**Copy Local File to Remote Server**

To copy a file from your local machine to a remote server, use the following syntax:

```bash
scp /local/file/path fabrice@servername.fabq.ca:/remote/file/path
```

- `/local/file/path`: Specify the path to the local file you want to copy.
- `fabrice@servername.fabq.ca`: This is the user and remote server where the file will be copied.
- `/remote/file/path`: This is the destination path on the remote server.

**Copy a Directory**

To copy an entire directory, use the `-r` option, which stands for "recursive":

```bash
scp -r /home/fabrice/foldername/ root@servername.fabq.ca:/remote/parent/
```

- `-r`: This option enables recursive copying of directories and their contents.
- `/home/fabrice/foldername/`: The path to the local directory you wish to copy.
- `root@servername.fabq.ca:/remote/parent/`: The destination path on the remote server where the directory will be copied.

**Copy a Configuration File Using a Specific SSH Key**

To copy a configuration file while specifying a particular SSH key for authentication, use the following command:

```bash
scp -i /home/fabrice/.ssh/fabquenneville /mnt/workbench/webserver/projectname/config.ini fabrice@servername.fabq.ca:/mnt/workbench/projectname/
```

- `-i /home/fabrice/.ssh/fabquenneville`: This option specifies the identity file (private key) for authentication.
- `/mnt/workbench/webserver/projectname/config.ini`: The path to the local configuration file being transferred.
- `fabrice@servername.fabq.ca`: The user and server to which the file is being copied.
- `/mnt/workbench/projectname/`: The destination path on the remote server where the file will be stored.

## Send Remote Commands

**Execute Commands Directly on a Remote Server**

You can use the `ssh` command to execute various commands on a remote server. Here are some examples:

**Run a Local Script on a Remote Server**

```bash
ssh fabrice@servername.fabq.ca 'bash -s' < /local/path/to/script.sh
```

- This command will execute the local script located at `/local/path/to/script.sh` on the remote server.

**Remove a file:**

```bash
ssh fabrice@192.168.1.100 "rm /home/fabrice/filename.log"
```

**Mount all filesystems:**

```bash
ssh root@servername.fabq.ca "mount -a"
```

**Reboot the remote server:**

```bash
ssh root@servername.fabq.ca "reboot -h now"
```

**Connect using a host key alias:**

```bash
ssh -o "HostKeyAlias=servername" root@192.168.1.100
```

## Test Connection, Add Alias, and Update Known Hosts

**Test Connection with Host Key Alias**

Use the following commands to establish an SSH connection while specifying a host key alias. This helps avoid conflicts with existing entries in the `known_hosts` file.

```bash
ssh -o 'HostKeyAlias=servername.fabq.ca' fabrice@192.168.1.100
ssh -o 'HostKeyAlias=servername' fabrice@192.168.1.100
```

**Test Host Identity without Authenticating**

To test the identity of a remote server without fully authenticating and to check connectivity, use the following command:

```bash
ssh -e none -o 'BatchMode=yes' -o 'HostKeyAlias=servername' fabrice@192.168.1.100 /bin/true
```

- `-e none`: Disables encryption for this command, which is useful in specific testing scenarios.
- `-o 'BatchMode=yes'`: Ensures that SSH does not prompt for user interaction, making it suitable for scripts.
- `/bin/true`: Executes a simple command that always returns success, confirming the connection without further actions.

This command allows you to verify that you can connect to the server while avoiding any authentication prompts.

**Retrieve Public SSH Keys**

To retrieve the public SSH keys from a remote server, use the following command:

```
ssh-keyscan -H servername.fabq.ca
```

- This command fetches the public SSH keys from the specified server, allowing you to add them to your `known_hosts` file.
- It does not establish a full SSH session and is primarily used for key retrieval, which helps ensure secure connections in future interactions.

By using both commands, you can test connectivity to a remote server and gather its public SSH keys for secure authentication later.

**Add Alias to SSH Config for Easy Access**

To simplify your SSH connections, you can create an alias for your SSH connections by editing the `~/.ssh/config` file:

```ini
Host servername
    HostName servername.fabq.ca
    User fabrice
    IdentityFile ~/.ssh/fabquenneville
```

- `Host servername`: This defines the alias you will use for the SSH connection.
- `HostName servername.fabq.ca`: This is the actual hostname of the remote server.
- `User fabrice`: This specifies the user to log in as.
- `IdentityFile ~/.ssh/fabquenneville`: This indicates the SSH key file to use for authentication.

## Remove Offending SSH Keys

When you encounter an "offending key" warning when connecting to a server, you can remove the old key from the `known_hosts` file. This is necessary if the server's host key has changed.

**View Known Hosts**

To view the contents of your `known_hosts` file, use:

```bash
cat ~/.ssh/known_hosts
```

**Edit Known Hosts Manually (Optional)**

You can edit the `known_hosts` file manually if you prefer:

```bash
nano ~/.ssh/known_hosts
```

**Update Known Hosts File with SSH Key**

```bash
ssh-keyscan -H servername.fabq.ca >> ~/.ssh/known_hosts
```

- This command retrieves the public key of the specified server and appends it to your `known_hosts` file, allowing SSH to recognize the server during subsequent connections.

**Remove Offending Key by Hostname**

You can use the `ssh-keygen` command to remove specific keys from your `known_hosts` file. Here are examples for different scenarios:

- To remove the offending key for a specific server:

```bash
ssh-keygen -R "servername.fabq.ca"
ssh-keygen -R "192.168.1.100"
```

- To specify the `known_hosts` file directly:

```bash
ssh-keygen -f "/home/fabrice/.ssh/known_hosts" -R "servername.fabq.ca"
ssh-keygen -f "/root/.ssh/known_hosts" -R "192.168.1.100"
ssh-keygen -f "/etc/ssh/ssh_known_hosts" -R "servername.fabq.ca"
```

**Summary of Key Removal**

You can also use a shorthand command to remove the offending key without specifying the file:

```bash
ssh-keygen -R servername.fabq.ca
```

This will automatically target the correct `known_hosts` file based on your user and system configuration.

## Change SSH Port

To enhance security, you may want to change the default SSH port (22) to a custom port. Follow these steps:

**1. Edit the SSH Configuration File**

Open the SSH daemon configuration file using a text editor:

```bash
nano /etc/ssh/sshd_config
```

Edit the following line to set a new port (e.g., port 2222):

```ini
Port 2222
```

- Locate the line that specifies the port (usually `#Port 22`) and change it to your desired port number (e.g., `Port 2222`).
- Make sure to uncomment the line by removing the `#`.

**2. Create Directory for Systemd Override**

If you're using systemd, create a directory for the SSH socket override:

```bash
mkdir -p /etc/systemd/system/ssh.socket.d
```

**3. Create an Override Configuration File**

Create or edit the override configuration file for the SSH socket:

```bash
nano /etc/systemd/system/ssh.socket.d/override.conf
```

- Add the following lines to specify the custom port:

```ini
[Socket]
ListenPort=2222  # Replace with your desired port number
```

**4. (Optional) Edit the Sockets Target Configuration**

You may also want to edit the sockets target configuration to ensure it points to the correct SSH socket:

```bash
nano /etc/systemd/system/sockets.target.wants/ssh.socket
```

- Make any necessary adjustments based on your custom port.

**5. Restart the SSH service to apply the changes**

After making changes, restart the SSH service to apply the new configuration:

```bash
systemctl restart sshd
```

**6. (Optional) Verify the New Port**

To verify that SSH is listening on the new port, you can use:

```bash
netstat -tuln | grep LISTEN
```

This will display the ports currently being listened to, allowing you to confirm that your changes were successful.

## Restart ssh

**Restart the SSH service to apply changes**

To restart the SSH service, use the following command:

```bash
systemctl restart sshd
```
