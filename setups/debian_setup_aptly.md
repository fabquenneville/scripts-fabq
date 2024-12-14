# Installing Aptly on Debian

## Table of Contents

- [Installing Aptly on Debian](#installing-aptly-on-debian)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Why Aptly?](#why-aptly)
  - [Prerequisites](#prerequisites)
  - [What This Guide Covers](#what-this-guide-covers)
  - [Placeholders](#placeholders)
  - [Important Warnings and Security Practices](#important-warnings-and-security-practices)
  - [Useful Commands and Information](#useful-commands-and-information)
    - [Documentation](#documentation)
    - [Links](#links)
    - [Software on the Machine](#software-on-the-machine)
    - [Paths](#paths)
    - [Proxmox Commands](#proxmox-commands)
    - [SSH Connection](#ssh-connection)
  - [Installation Procedure](#installation-procedure)

## Introduction

Welcome to the installation guide for Aptly on Debian in a Proxmox LXC container. Aptly is a powerful Debian repository management tool that can help you manage your custom APT repositories efficiently.

## Why Aptly?

Aptly simplifies Debian package management and allows you to:

- Create local APT repositories.
- Mirror remote repositories.
- Take consistent snapshots of repositories.
- Publish snapshot repositories.

## Prerequisites

Before you begin the installation process, ensure that your Debian system meets the following requirements:

- Debian GNU/Linux 9 (Stretch) or later
- Access to a terminal with sudo privileges
- Basic familiarity with the command line interface
- Stable internet connection to download necessary packages

## What This Guide Covers

This guide will walk you through the installation of Aptly on Debian step by step, covering:

1. **Installation**: Installing Aptly from the official repository or using a binary release.
2. **Configuration**: Configuring Aptly to suit your environment and preferences.
3. **Setup**: Setting up Aptly as a service and accessing it.

## Placeholders

Replace the placeholders below with the appropriate values for your setup:

- **User Details**

  - Username: `<username>` (e.g., admin)
  - Username - Hypervisor: `<username-hypervisor>` (e.g., admin)
  - User full name: `<user-full-name>` (e.g., John Doe)
  - User email address: `<user-email-address>` (e.g., johndoe@example.com)

- **Server Configuration**

  - Server IP address: `<server-ip-address>` (e.g., 192.168.1.100)
  - Hostname - Intranet: `<hostname-intranet>` (e.g., aptly-server.domain.com)
  - Hostname - Internet: `<hostname-internet>` (e.g., aptly.domain.com)
  - Hostname - Hypervisor: `<hostname-hypervisor>` (e.g., proxmox-hypervisor.domain.com)
  - Hostname - Hypervisor NAS: `<hostname-hypervisor-nas>` (e.g., nas-server.domain.com)
  - Name - Hypervisor NAS: `<name-hypervisor-nas>` (e.g., nas-server)

- **SSH Keys**

  - SSH key - Proxmox: `<ssh-key-proxmox>` (e.g., /home/user/.ssh/id_rsa.pub)
  - SSH key - Client: `<ssh-key-client>` (e.g., /home/user/.ssh/client_id_rsa.pub)

- **Networking**

  - Wireguard port: `<wireguard-port>` (e.g., 51820)

- **Repository Details**

  - Example repository name: `<example-repository-name>` (e.g., myrepository)
  - Example package base: `<example-package-base>` (e.g., mypackage_1.1.1)
  - Example package Debian version: `<example-package-debian-version>` (e.g., mypackage_1.1.1-1)
  - GPG repository key id: `<gpg-repository-key-id>` (e.g., ABCD1234EFGH5678)

- **Paths**

  - Path index: `<path-index>` (e.g., /var/www/html)
  - Path images: `<path-images>` (e.g., /var/www/static/)
  - Path errors: `<path-errors>` (e.g., /var/www/errors)

## Important Warnings and Security Practices

Before executing any commands in this documentation, please adhere to the following guidelines to ensure the security and integrity of the system:

1. **Execute Commands with Caution**: Always review and understand a command before executing it. Misuse of commands can lead to data loss or system instability.
2. **Backup Command Execution**: The backup command must be executed only by authorized users. Ensure that proper permissions are set to prevent unauthorized access to backup files.
3. **Regular Backups**: Maintain regular backups of all critical data. It is advisable to use automated backup solutions and verify backup integrity periodically.
4. **System Updates**: Regularly update the system and all installed packages to protect against vulnerabilities. Use the package manager responsibly to avoid potential conflicts.
5. **Monitor System Logs**: Continuously monitor system logs for any unusual activity. Use logging tools to help identify potential security breaches or system failures.
6. **User Permissions**: Ensure that user permissions are strictly managed. Limit access to sensitive commands and data to only those who need it to perform their job functions.
7. **Network Security**: Implement proper network security measures, such as firewalls and intrusion detection systems, to protect against external threats.
8. **Data Encryption**: Encrypt sensitive data at rest and in transit to prevent unauthorized access.

By following these practices, you will help maintain the security and stability of the system while minimizing the risk of data loss or compromise.

## Useful Commands and Information

### Documentation

- [Documentation Overview](https://www.aptly.info/doc/overview/)
- [Tutorials](https://www.aptly.info/tutorial/)

### Links

- [Aptly Repository](https://<hostname-internet>/)

### Software on the Machine

- **Operating System**: Debian
- **Web Server**: Nginx
- **Security**: GnuPG, WireGuard, UFW
- **Other**: Git, sudo

### Paths

- **Aptly Configuration**: `/home/aptly/.aptly.conf`
- **Aptly Work Path**: `/home/aptly/.aptly/`

### Proxmox Commands

**List available Proxmox templates**

```bash
ssh <username>@<hostname-hypervisor-nas> "ls /mnt/proxmox/template/cache/"
```

**Create the container**

```bash
ssh <username-hypervisor>@<hostname-hypervisor> "pct create 100 <name-hypervisor-nas>:vztmpl/debian-12-upgraded_12.5_amd64.tar.zst --hostname <hostname-intranet> --cores 2 --memory 2048 --swap 2048 --net0 name=net0,bridge=vmbr0,ip=dhcp,firewall=1 --rootfs <name-hypervisor-nas>:250 --unprivileged 1 --features nesting=1 --ssh-public-keys <ssh-key-proxmox> --start 1"
```

**Backup**

```bash
ssh <username-hypervisor>@<hostname-hypervisor> "vzdump 100 --compress zstd --mode stop --storage <name-hypervisor-nas> --note \"$(date +'%Y-%m-%d %H:%M') Backup fresh install\""
```

**Set the state of the Proxmox HA Manager for Container 100**

```bash
ssh <username-hypervisor>@<hostname-hypervisor> "ha-manager add ct:100"
ssh <username-hypervisor>@<hostname-hypervisor> "ha-manager remove ct:100"
```

**Set the state and limits of the Proxmox Container 100 in the HA Manager**

```bash
ssh <username-hypervisor>@<hostname-hypervisor> "ha-manager set ct:100 --state started --max_relocate 3 --max_restart 3"
ssh <username-hypervisor>@<hostname-hypervisor> "ha-manager set ct:100 --state stopped"
ssh <username-hypervisor>@<hostname-hypervisor> "pct reboot 100"
```

**Destroy the Proxmox Container 100 forcefully**

```bash
ssh <username-hypervisor>@<hostname-hypervisor> "pct destroy 100 --force --purge"
```

**Move the Proxmox Container 100 to another host**

```bash
ssh <username-hypervisor>@<hostname-hypervisor> "pct migrate 100 hv2"
```

### SSH Connection

**Connection with specific keys**

```bash
ssh -i <ssh-key-client> root@<hostname-intranet>
ssh -i <ssh-key-client> root@<server-ip-address>
ssh -i <ssh-key-client> <username>@<hostname-intranet>
ssh -i <ssh-key-client> <username>@<server-ip-address>
```

**Remove offending keys from known_hosts**

```bash
ssh-keygen -f "/home/<username>/.ssh/known_hosts" -R "<hostname-intranet>"
ssh-keygen -f "/home/<username>/.ssh/known_hosts" -R "<server-ip-address>"
```

**Copy SSH public key to remote host**

```bash
ssh-copy-id -i <ssh-key-client> root@<server-ip-address>
ssh-copy-id -i <ssh-key-client> root@<hostname-intranet>
ssh-copy-id -i <ssh-key-client> <username>@<server-ip-address>
ssh-copy-id -i <ssh-key-client> <username>@<hostname-intranet>
```

**Transfer SSH keys and files**

```bash
mkdir -p /home/aptly/.ssh/
cp /home/<username>/.ssh/authorized_keys /home/aptly/.ssh/authorized_keys
chown -R aptly:aptly /home/aptly/.ssh/
```

## Installation Procedure

1. **Fresh Debian Installation**

   - Install a fresh Debian operating system on your new server following the standard installation procedure.

2. **Backup before starting**

   ```bash
   ssh <username-hypervisor>@<hostname-hypervisor> "vzdump 100 --compress zstd --mode stop --storage <name-hypervisor-nas> --note \"$(date +'%Y-%m-%d %H:%M') Backup fresh install\""
   ```

3. **Install Required Dependencies**

   **Upgrade the base system**

   ```bash
   apt update
   apt upgrade -y
   ```

   **Install dependencies**

   ```bash
   apt install -y sudo gnupg wget nginx git wireguard-tools ufw
   ```

4. **Ensure Hostname**

   ```bash
   nano /etc/hosts
   # Add line: 127.0.1.1 <hostname-intranet>
   nano /etc/hostname
   # Set to: <hostname-intranet>
   hostnamectl set-hostname <hostname-intranet>
   ```

5. **Add Users**

   ```bash
   adduser --gecos "<user-full-name>,,,<user-email-address>" <username>
   usermod -aG sudo <username>

   adduser --system --shell /bin/bash --gecos 'Aptly repository' --group --disabled-password --home /home/aptly aptly
   ```

6. **Setup SSH Connectors**

   - Configure SSH connectors as per your setup script to establish secure connections to the server.

7. **Test users, SSH, and sudo**

   1. **Transfer SSH keys for User**
   2. **Connect as User with SSH key**
   3. **Test sudo**

   ```bash
   sudo su -
   ```

   4. **Disconnect as root**

8. **Secure SSH**

   ```bash
   nano /etc/ssh/sshd_config
   ```

   ```ini
   PermitRootLogin no
   PasswordAuthentication no
   ChallengeResponseAuthentication no
   ```

   **Restart SSH**

   ```bash
   systemctl restart ssh
   ```

9. **Configure Firewall**

   **Open ports**

   ```bash
   ufw allow OpenSSH
   ufw allow http
   ufw allow https
   ufw allow <wireguard-port>/udp
   ```

   **Enable firewall**

   ```bash
   ufw enable
   ```

10. **Add the Aptly Repository**

    Find the latest instructions at [Aptly Installations](https://www.aptly.info/download/).

    **Import the GPG key**

    ```bash
    mkdir -p /etc/apt/keyrings
    chmod 755 /etc/apt/keyrings
    wget -O /etc/apt/keyrings/aptly.asc https://www.aptly.info/pubkey.txt
    ```

    **Add the Aptly repository**

    ```bash
    echo "deb [signed-by=/etc/apt/keyrings/aptly.asc] http://repo.aptly.info/ squeeze main" | tee /etc/apt/sources.list.d/aptly.list
    ```

11. **Install Aptly**

    After adding the repository, update your package list and install Aptly:

    ```bash
    apt update
    apt install -y aptly
    ```

12. **Configure Aptly**

    **Initialize the Aptly Directory**

    ```bash
    aptly repo create -distribution=stable -component=main <example-repository-name>-stable
    aptly repo create -distribution=testing -component=main <example-repository-name>-testing
    ```

    **Adding Packages**

    ```bash
    sudo -iu aptly
    mkdir /home/aptly/packages/
    ```

    ```bash
    scp <example-package-debian-version>_all.deb <example-package-debian-version>.dsc <example-package-base>.orig.tar.gz <example-package-debian-version>.debian.tar.xz <example-package-debian-version>_amd64.changes aptly@<hostname-intranet>:/home/aptly/packages/
    ```

    To add packages to your local repository:

    ```bash
    aptly repo add <example-repository-name>-stable /home/aptly/packages/
    aptly repo add <example-repository-name>-testing /home/aptly/packages/
    ```

    **Generate and Transfer GPG Keys**

    ```bash
    gpg --full-generate-key
    gpg --list-keys
    gpg --export-secret-keys --armor <gpg-repository-key-id> > ~/<hostname-internet>.private-key.asc
    gpg --export --armor <gpg-repository-key-id> > ~/<hostname-internet>.public-key.asc
    ```

    ```bash
    scp ~/<hostname-internet>.private-key.asc aptly@<hostname-internet>:/home/aptly/
    rm ~/<hostname-internet>.private-key.asc
    ```

    **Register keys with public keyservers**

    ```bash
    gpg --send-keys <gpg-repository-key-id>
    gpg --keyserver hkp://keyserver.ubuntu.com --send-keys <gpg-repository-key-id>
    gpg --keyserver hkp://pgp.mit.edu --send-keys <gpg-repository-key-id>
    ```

    **Import GPG Key**

    ```bash
    sudo -iu aptly
    gpg --import /home/aptly/<hostname-internet>.private-key.asc
    gpg --edit-key <gpg-repository-key-id> # trust
    rm ~/<hostname-internet>.private-key.asc
    ```

    **Add Key to Aptly Config**

    Edit `~/.aptly.conf`:

    ```json
    {
      "gpgKey": "<gpg-repository-key-id>"
    }
    ```

    **Publishing the Repository**

    After adding packages, you can publish the repository:

    ```bash
    aptly publish repo -architectures="amd64,i386" <example-repository-name>-stable
    aptly publish repo -architectures="amd64,i386" <example-repository-name>-testing
    ```

    This will create a new directory with the published APT repository, which can be served via HTTP.

    **Snapshot the repositories**

    ```bash
    sudo -iu aptly
    # Get the current date in YYYY-MM-DD format
    current_date=$(date +%F)

    # Define your repository names
    repository_name="<example-repository-name>"

    # Create snapshots with automatic names
    aptly snapshot create "${repository_name}-stable-${current_date}" from repo "${repository_name}-stable"
    aptly snapshot create "${repository_name}-testing-${current_date}" from repo "${repository_name}-testing"
    ```

13. **nginx Configuration**

    1. **Configure nginx to run as aptly**

       ```bash
       nano /etc/nginx/nginx.conf
       ```

       ```ini
       user aptly;
       ```

    2. **Backup Default Files**
       Backup the default index.html and configuration files.

       ```bash
       mv /var/www/html /var/www/.html
       mv /etc/nginx/sites-available/default /etc/nginx/sites-available/.default
       rm /etc/nginx/sites-enabled/default
       ```

    3. **Create source ssl certificate**

       ```bash
       mkdir -p /etc/nginx/ssl/
       openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/nginx/ssl/<hostname-internet>.key -out /etc/nginx/ssl/<hostname-internet>.crt
       ```

    4. **Create Default Server Block for Unauthorized Access**

       ```bash
       nano /etc/nginx/sites-available/unauthorized
       ```

       ```nginx
       server {
           listen 80 default_server;
           listen [::]:80 default_server;

           server_name _;

           error_page 403 /403.html;
           location = /403.html {
               root <path-errors>;
               internal;
           }

           error_page 404 /404.html;
           location = /404.html {
               root <path-errors>;
               internal;
           }

           error_page 500 /500.html;
           location = /500.html {
               root <path-errors>;
               internal;
           }

           location / {
               return 403;
           }
       }
       ```

    5. **Site configuration**

       Edit the Nginx configuration file to point to the Aptly repository. Open the file:

       ```bash
       nano /etc/nginx/sites-available/<hostname-internet>.conf
       ```

       Add the following configuration:

       ```nginx
        server {
            listen 80;
            listen [::]:80;

            server_name <hostname-internet>;

            # Redirect all HTTP traffic to HTTPS
            return 301 https://$host$request_uri;
        }

        server {
            listen 443 ssl;
            listen [::]:443 ssl;

            server_name <hostname-internet>;

            ssl_certificate /etc/nginx/ssl/<hostname-internet>.crt; # Path to the SSL certificate
            ssl_certificate_key /etc/nginx/ssl/<hostname-internet>.key; # Path to the SSL certificate key

            # Optional: Add HSTS for enhanced security
            add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

            # Security headers for additional protection
            add_header X-Content-Type-Options nosniff;
            add_header X-Frame-Options SAMEORIGIN;
            add_header X-XSS-Protection "1; mode=block";

            # GPG public key location
            location = /<hostname-internet>-public-key.asc {
                root /home/aptly/.aptly/public; # Directory containing the public key
                try_files /<hostname-internet>-public-key.asc =404; # Serve the public key or return 404
            }

            location = /<hostname-internet>-public-key.gpg {
                root /home/aptly/.aptly/public; # Directory containing the GPG key
                try_files /<hostname-internet>-public-key.gpg =404; # Serve the GPG key or return 404
            }

            # Debian repository locations with directory listing enabled
            location /dists/ {
                alias /home/aptly/.aptly/public/dists/; # Repository distribution files
                autoindex on; # Enable directory listing
            }

            location /pool/ {
                alias /home/aptly/.aptly/public/pool/; # Repository package files
                autoindex on; # Enable directory listing
            }

            # Default page served from the specified root directory
            location = / {
                root <path-index>; # Directory for the default page
                try_files /<hostname-internet>.html =404; # Serve the default page or return 404
            }

            # Static images served without directory listing
            location /images/ {
                alias <path-images>; # Directory for static images
                autoindex off; # Disable directory listing
            }

            # Custom error pages for improved user experience
            error_page 403 /403.html; # Custom 403 error page
            location = /403.html {
                root <path-errors>; # Directory for error pages
                internal; # Prevent direct access
            }

            error_page 404 /404.html; # Custom 404 error page
            location = /404.html {
                root <path-errors>; # Directory for error pages
                internal; # Prevent direct access
            }

            error_page 500 /500.html; # Custom 500 error page
            location = /500.html {
                root <path-errors>; # Directory for error pages
                internal; # Prevent direct access
            }

            # Deny access to hidden files and specific file types
            location ~ /\. {
                deny all; # Deny access to hidden files
            }
        }
       ```

    6. **Enabling the new VirtualHost**

       ```bash
       ln -s /etc/nginx/sites-available/unauthorized /etc/nginx/sites-enabled/
       ln -s /etc/nginx/sites-available/<hostname-internet>.conf /etc/nginx/sites-enabled/
       ```

    7. **Test nginx configuration**

       ```bash
       nginx -t
       ```

    8. **Reloading nginx**
       nginx reload

       ```bash
       systemctl reload nginx
       ```

       Optional nginx restart

       ```bash
       systemctl restart nginx
       ```

    Now, your Aptly repository is available at `http://<hostname-internet>`.

14. **Back-up post installation**

    ```bash
    ssh <username-hypervisor>@<hostname-hypervisor> "ha-manager set ct:100 --state stopped"
    ssh <username-hypervisor>@<hostname-hypervisor> "vzdump 100 --compress zstd --mode stop --storage <name-hypervisor-nas> --note \"$(date +'%Y-%m-%d %H:%M') Backup post installation\""
    ```

15. **Start the server**
    ```bash
    ssh <username-hypervisor>@<hostname-hypervisor> "ha-manager set ct:100 --state started --max_relocate 3 --max_restart 3"
    ```
