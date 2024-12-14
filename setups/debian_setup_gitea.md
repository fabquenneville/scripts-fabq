# Installing Gitea on Debian

## Table of Contents

- [Installing Gitea on Debian](#installing-gitea-on-debian)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Why Gitea?](#why-gitea)
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

Welcome to the installation guide for Gitea on Debian! Gitea is a lightweight self-hosted Git service that offers a streamlined and user-friendly interface, perfect for managing your repositories and collaborating with your team. By following this guide, you'll be able to set up Gitea on your Debian system quickly and efficiently.

## Why Gitea?

Gitea provides a powerful alternative to centralized Git hosting services, offering full control over your repositories and data privacy. With features such as issue tracking, wiki, and pull requests, Gitea empowers developers to collaborate effectively while keeping their codebase secure.

## Prerequisites

Before you begin the installation process, ensure that your Debian system meets the following requirements:

- Debian GNU/Linux 9 (Stretch) or later
- Access to a terminal with sudo privileges
- Basic familiarity with the command line interface
- Stable internet connection to download necessary packages

## What This Guide Covers

This guide will walk you through the installation of Gitea on Debian step by step, covering:

1. **Installation**: Installing Gitea from the official repository or using a binary release.
2. **Configuration**: Configuring Gitea to suit your environment and preferences.
3. **Setup**: Setting up Gitea as a service and accessing it.

## Placeholders

Replace the placeholders below with the appropriate values for your setup:

- **User Details**

  - Username: `<username>` (e.g., admin)
  - Username - Hypervisor: `<username-hypervisor>` (e.g., admin)
  - User full name: `<user-full-name>` (e.g., John Doe)
  - User email address: `<user-email-address>` (e.g., johndoe@example.com)

- **Server Configuration**

  - Server IP address: `<server-ip-address>` (e.g., 192.168.1.100)
  - Hostname - Intranet: `<hostname-intranet>` (e.g., gitea-server.domain.com)
  - Hostname - Internet: `<hostname-internet>` (e.g., gitea.domain.com)
  - Hostname - Hypervisor: `<hostname-hypervisor>` (e.g., proxmox-hypervisor.domain.com)
  - Hostname - Hypervisor NAS: `<hostname-hypervisor-nas>` (e.g., nas-server.domain.com)
  - Name - Hypervisor NAS: `<name-hypervisor-nas>` (e.g., nas-server)

- **SSH Keys**

  - SSH key - Proxmox: `<ssh-key-proxmox>` (e.g., /home/user/.ssh/id_rsa.pub)
  - SSH key - Client: `<ssh-key-client>` (e.g., /home/user/.ssh/client_id_rsa.pub)

- **Networking**

  - Wireguard port: `<wireguard-port>` (e.g., 51820)

- **Paths**

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

- [Documentation](https://docs.gitea.com/)

### Links

- [Gitea Repository](https://<hostname-internet>/)

### Software on the Machine

- **Operating System**: Debian
- **Database**: MariaDB (configured as MySQL)
- **Web Server**: Nginx
- **Security**: GnuPG, WireGuard, UFW
- **Other**: Git, sudo, certbot (for SSL certificate management)

### Paths

- **Gitea Configuration**: `/etc/gitea/app.ini`
- **Gitea Work Path**: `/var/lib/gitea`

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
scp /home/<username>/.ssh/<username>* <username>@<hostname-intranet>:/home/<username>/.ssh/
mkdir -p /home/<username>/.ssh/
mv /home/<username>/.ssh/<username>* /home/<username>/.ssh/
chown -R <username>:<username> /home/<username>/.ssh/
cat /home/<username>/.ssh/<username>.pub >> /home/<username>/.ssh/authorized_keys
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
   apt install -y sudo tar wget mariadb-server git nginx
   apt install -y gnupg wireguard-tools ufw
   apt install -y certbot python3-certbot-nginx
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
   adduser --system --shell /bin/bash --gecos 'Gitea repository' --group --disabled-password --home /home/gitea gitea

   adduser --gecos "<user-full-name>,,,<user-email-address>" <username>
   usermod -aG sudo <username>
   usermod -aG gitea <username>
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
   ufw allow <wireguard-port>/udp
   ```

   **Enable firewall**

   ```bash
   ufw enable
   ```

10. **Configure Mariadb**

    1. **Security**
       ```bash
       mariadb-secure-installation
       mariadb
       ```
    2. **Mariadb Users**

       ```sql
       SET old_passwords=0;
       CREATE USER 'gitea' IDENTIFIED BY '';
       ```

       ```sql
       CREATE USER IF NOT EXISTS 'gitea'@'192.168.1.%' IDENTIFIED BY '';
       GRANT ALL PRIVILEGES ON *.* TO 'gitea'@'192.168.1.%' IDENTIFIED BY '' WITH GRANT OPTION;
       GRANT ALL PRIVILEGES ON *.* TO 'gitea'@'localhost' IDENTIFIED BY '' WITH GRANT OPTION;
       SET PASSWORD FOR 'gitea'@'localhost' = PASSWORD('');
       SET PASSWORD FOR 'gitea'@'192.168.1.%' = PASSWORD('');
       FLUSH PRIVILEGES;
       ```

11. **Install Gitea**

    [Download](https://dl.gitea.io/gitea/)

    ```bash
    wget -O gitea https://dl.gitea.com/gitea/1.22.0-rc0/gitea-1.22.0-rc0-linux-amd64
    mv gitea /usr/local/bin/gitea
    chmod 755 /usr/local/bin/gitea
    chown -R gitea:gitea /usr/local/bin/gitea
    ```

12. **Create required directory structure**

    ```bash
    mkdir -p /var/lib/gitea/{custom,data,log}
    mkdir /etc/gitea
    ```

13. **Gitea configuration**
    Configure gitea before starting the service.

    ```bash
    nano /etc/gitea/app.ini
    ```

14. **Adjust File Permissions**

    - Ensure proper file owners and permissions are set for the Gitea directories:

    ```bash
    chown -R gitea:gitea /var/lib/gitea/
    chown -R gitea:gitea /home/gitea/gitea-repositories/
    chown -R root:gitea /etc/gitea
    chown gitea:gitea /etc/gitea/app.ini
    ```

    ```bash
    chmod -R 750 /var/lib/gitea/
    chmod -R 770 /etc/gitea
    ```

15. **Service**
    [Documentation](https://github.com/go-gitea/gitea/blob/main/contrib/systemd/gitea.service)

    ```bash
    nano /etc/systemd/system/gitea.service
    systemctl enable gitea --now
    ```

16. **Nginx Configuration**

    1. **Allow http https**

       ```bash
       ufw allow https
       ufw allow http
       ```

    2. **Backup Default Files**
       Backup the default index.html and configuration files.

       ```bash
       mv /var/www/html /var/www/.html
       mv /etc/nginx/sites-available/default /etc/nginx/sites-available/.default
       rm /etc/nginx/sites-enabled/default
       ```

    3. **Create Default Server Block for Unauthorized Access**

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

    4. **Site configuration**

       Edit the Nginx configuration file to proxy to the Gitea repository.

       ```bash
       nano /etc/nginx/sites-available/<hostname-internet>.conf
       ```

       Add the following configuration:

       ```nginx
       server {
           listen 80;
           listen [::]:80;

           server_name <hostname-internet> www.<hostname-internet>;

           client_max_body_size 50m;
           location / {
               proxy_pass http://localhost:3000;
           }
       }
       ```

    5. **Enabling the new VirtualHost**

       ```bash
       ln -s /etc/nginx/sites-available/unauthorized /etc/nginx/sites-enabled/
       ln -s /etc/nginx/sites-available/<hostname-internet>.conf /etc/nginx/sites-enabled/
       ```

    6. **Test Nginx configuration**

       ```bash
       nginx -t
       ```

    7. **Managing Nginx**

       **Enable Nginx**

       ```bash
       systemctl enable nginx
       ```

       **Nginx reload**

       ```bash
       systemctl reload nginx
       ```

       **`Optional` Nginx restart**

       ```bash
       systemctl restart nginx
       ```

17. **Certbot (If directly accessed)**

    ```bash
    certbot --nginx -d <hostname-internet>
    systemctl status certbot.timer
    certbot renew --dry-run
    ```

18. **Verify installation**

    - Verify that the Gitea instance is installed restored by accessing it through a web browser. Ensure that all repositories, users, and configurations are intact.

    ```bash
    systemctl status gitea
    systemctl status nginx
    ```

    Visit the server at [http://<hostname-internet>](http://<hostname-internet>) or [https://<hostname-internet>](https://<hostname-internet>).

19. **Backup post installation**

    ```bash
    ssh <username-hypervisor>@<hostname-hypervisor> "ha-manager set ct:100 --state stopped"
    ssh <username-hypervisor>@<hostname-hypervisor> "vzdump 100 --compress zstd --mode stop --storage <name-hypervisor-nas> --note \"$(date +'%Y-%m-%d %H:%M') Backup post installation\""
    ```

20. **Start the server**
    ```bash
    ssh <username-hypervisor>@<hostname-hypervisor> "ha-manager set ct:100 --state started --max_relocate 3 --max_restart 3"
    ```
