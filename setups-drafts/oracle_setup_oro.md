# Installing Oro on Oracle Linux

## Table of Contents

- [Installing Oro on Oracle Linux](#installing-oro-on-oracle-linux)
  - [Table of Contents](#table-of-contents)
  - [Disclaimer: Incomplete Guide](#disclaimer-incomplete-guide)
  - [Introduction](#introduction)
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

## Disclaimer: Incomplete Guide

This document is a draft and may contain incomplete, untested, or outdated information. It is a work in progress and has not been verified for accuracy or usability. Use this guide at your own discretion, and consider it as a reference for further development or exploration. Updates may follow in the future, but no guarantees are made.

## Introduction

This guide provides step-by-step instructions for installing and configuring Oro on a Oracle Linux server.

## Prerequisites

Before you begin the installation process, ensure that your Oracle Linux system meets the following requirements:

- Oracle Linux GNU/Linux 9 or later
- Access to a terminal with sudo privileges
- Basic familiarity with the command line interface
- Stable internet connection to download necessary packages

## What This Guide Covers

This guide covers the installation and configuration of Oro on a Oracle Linux server, along with additional setup tasks such as SSH connection management and Proxmox commands. It covers:

1. **Installation**: Installing Oro from the official repository.
2. **Configuration**: Configuring Oro to suit your environment and preferences.
3. **Setup**: Setting up Oro as a service and accessing it.

## Placeholders

Replace the placeholders below with the appropriate values for your setup:

- **User Details**

  - Username: `<username>` (e.g., admin)
  - Username - Hypervisor: `<username-hypervisor>` (e.g., admin)

- **Server Configuration**

  - Server IP address: `<server-ip-address>` (e.g., 192.168.1.100)
  - Hostname - Intranet: `<hostname-intranet>` (e.g., oro-server.domain.com)
  - Hostname - Internet: `<hostname-internet>` (e.g., oro.domain.com)
  - Hostname - Hypervisor: `<hostname-hypervisor>` (e.g., proxmox-hypervisor.domain.com)
  - Hostname - Hypervisor NAS: `<hostname-hypervisor-nas>` (e.g., nas-server.domain.com)
  - Name - Hypervisor NAS: `<name-hypervisor-nas>` (e.g., nas-server)

- **SSH Keys**

  - SSH key - Proxmox: `<ssh-key-proxmox>` (e.g., /home/user/.ssh/id_rsa.pub)
  - SSH key - Client: `<ssh-key-client>` (e.g., /home/user/.ssh/client_id_rsa.pub)

- **Networking**

  - Wireguard port: `<wireguard-port>` (e.g., 51820)

- **Paths**

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

- [Documentation Overview](https://doc.oroinc.com/)
- [Documentation community edition](https://doc.oroinc.com/backend/setup/dev-environment/community-edition/)
- [Installation](https://doc.oroinc.com/backend/setup/installation/)

### Links

- [Oro appliance](https://<hostname-internet>/)

### Software on the Machine

- **Operating System**: Oracle Linux
- **Web Server**:
- **Security**: GnuPG, WireGuard, firewalld
- **Other**: Git, sudo

### Paths

- **Oro Configuration**:
- **Oro Work Path**:

### Proxmox Commands

**List available Proxmox templates**

```bash
ssh <username>@<hostname-hypervisor-nas> "ls /mnt/proxmox/template/cache/"
```

**Create the container**

```bash
ssh <username-hypervisor>@<hostname-hypervisor> "pct create 100 <name-hypervisor-nas>:vztmpl/oracle-9-sshnano_20240603_amd64.tar.zst --hostname <hostname-intranet> --cores 2 --memory 4096 --swap 2048 --net0 name=net0,bridge=vmbr0,ip=dhcp,firewall=1 --rootfs <name-hypervisor-nas>:100 --unprivileged 1 --features nesting=1 --ssh-public-keys <ssh-key-proxmox>"
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
ssh <username-hypervisor>@<hostname-hypervisor> "pct start 100"
ssh <username-hypervisor>@<hostname-hypervisor> "pct stop 100"
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

## Installation Procedure

1. **Fresh Oracle Linux Installation**

   - Install a fresh Oracle Linux operating system on your new server following the standard installation procedure.

2. **Backup before starting**

   ```bash
   ssh <username-hypervisor>@<hostname-hypervisor> "vzdump 100 --compress zstd --mode stop --storage <name-hypervisor-nas> --note \"$(date +'%Y-%m-%d %H:%M') Backup fresh install\""
   ```

3. **Install Required Dependencies**

   **Upgrade the base system**

   ```bash
   dnf update
   ```

   **Enable EPEL repository**
   Extra Package for Enterprise Linux repository has packages like Apache and Nginx

   ```bash
   dnf install epel-release
   ```

   **Enable Postgres repository**

   Get instructions and urls in their [documentation](https://www.postgresql.org/download/linux/redhat/)

   ```bash
   # Install the repository RPM:
   dnf install -y https://download.postgresql.org/pub/repos/yum/reporpms/EL-9-x86_64/pgdg-redhat-repo-latest.noarch.rpm

   # Disable the built-in PostgreSQL module:
   dnf -qy module disable postgresql

   # Install PostgreSQL:
   dnf install -y postgresql15-server

   # Optionally initialize the database and enable automatic start:
   /usr/pgsql-15/bin/postgresql-15-setup initdb
   systemctl enable postgresql-15
   systemctl start postgresql-15
   ```

   **Enable Remi repository**

   ```bash
   cat >"/etc/yum.repos.d/oropublic.repo" <<__EOF__
   [oropublic]
   name=OroPublic
   baseurl=https://nexus.oro.cloud/repository/oropublic/8/x86_64/
   enabled=1
   gpgcheck=0
   module_hotfixes=1
   __EOF__
   ```

   ```bash
   dnf config-manager --set-enabled remi
   ```

   **Enable oro repository**

   ```bash
   dnf install https://rpms.remirepo.net/enterprise/remi-release-9.rpm
   ```

   **Enable DNF streams**

   ```bash
   dnf module list nginx
   dnf module list nodejs
   dnf module list php

   dnf -y module enable nginx:1.24 nodejs:20 php:remi-8.3
   dnf -y upgrade
   ```

   **Install dependencies**

   ```bash
   dnf install -y sudo nano findutils rsync psmisc wget glibc-langpack-en bzip2 unzip p7zip p7zip-plugins parallel patch nodejs npm git-core jq bc postgresql postgresql-server postgresql-contrib
   dnf install -y gnupg wireguard-tools firewalld firewall-config
   ```

   **Install Apache or Nginx**
   Uncomment one of the following lines depending on the web server you prefer to use

   **Apache**

   ```bash
   dnf install -y httpd
   ```

   **Nginx Configuration**

   ```bash
   dnf install -y nginx
   ```

   **PHP and modules**

   ```bash
   dnf install -y php-common php-cli php-fpm php-opcache php-mbstring php-mysqlnd php-pgsql php-pdo php-json php-process php-ldap php-gd php-ctype php-curl php-fileinfo php-intl php-bcmath php-xml php-soap php-sodium php-openssl php-pcre php-simplexml php-tokenizer php-zip php-tidy php-imap php-pecl-zip php-pecl-mongodb
   ```

   **nodejs**

   ```bash
   dnf install -y nodejs
   ```

   Verify Node.js and NPM versions

   ```bash
   node -v
   npm -v
   ```

   **Supervisor for process control**

   ```bash
   dnf install -y supervisor
   ```

   Enable and start Supervisor service

   ```bash
   systemctl enable supervisord
   systemctl start supervisord
   ```

   **Redis**

   ```bash
   dnf install -y redis
   ```

   Enable and start Redis service

   ```bash
   systemctl enable redis
   systemctl start redis
   ```

   **pngquant and jpegoptim**
   dnf install -y pngquant jpegoptim

4. **Ensure Hostname**

   ```bash
   nano /etc/hosts
   # Add line: 127.0.1.1 <hostname-intranet>
   nano /etc/hostname
   # Set to: <hostname-intranet>
   hostnamectl set-hostname <hostname-intranet>
   ```

5. **Add Users and set Credentials**

   ```bash
   passwd -f root
   ```

   ```bash
   adduser <username>
   passwd -f <username>
   groupadd sudo
   usermod -aG sudo <username>
   nano /etc/sudoers
   ```

   ```
   ## Allows people in group sudo to run all commands
   %sudo ALL=(ALL)       ALL
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
   systemctl restart sshd
   ```

9. **Configure Firewall**

   **Open ports**

   ```bash
   firewall-cmd --permanent --add-service=ssh
   firewall-cmd --permanent --add-service=http
   firewall-cmd --permanent --add-service=https
   firewall-cmd --permanent --add-port=<wireguard-port>/udp
   ```

   **Reload firewall to apply changes**

   ```bash
   firewall-cmd --reload
   ```

   **Enable and start firewall**

   ```bash
   systemctl enable firewalld
   systemctl start firewalld
   ```

10. **Configure PHP**

    ```bash
    php --ini
    nano /etc/php.ini
    ```

    **Add or update the following settings**

    ````ini
    date.timezone = America/Toronto
    detect_unicode = Off
    memory_limit = 1G
    max_execution_time = <appropriate-time>

    If xdebug is installed, update or add these settings
    ```ini
    xdebug.scream = Off
    xdebug.show_exception_trace = Off
    xdebug.max_nesting_level = 100
    ````

11. **Install Oro**

    ```bash
    dnf -y --setopt=install_weak_deps=False --best --nogpgcheck install oro-nginx oro-nginx-mod-http-cache_purge oro-nginx-mod-http-cookie_flag oro-nginx-mod-http-geoip oro-nginx-mod-http-gridfs oro-nginx-mod-http-headers_more oro-nginx-mod-http-naxsi oro-nginx-mod-http-njs oro-nginx-mod-http-pagespeed oro-nginx-mod-http-sorted_querystring oro-nginx-mod-http-testcookie_access oro-nginx-mod-http-xslt-filter
    ```

12. **Enable Oro service**

13. **Setup nginx proxy**

14. **Configure SSL**

15. **Correct permissions**

16. **Run the installer**

17. **Verify installation**

18. **Back-up post installation**

    ```bash
    ssh <username-hypervisor>@<hostname-hypervisor> "ha-manager set ct:100 --state stopped"
    ssh <username-hypervisor>@<hostname-hypervisor> "vzdump 100 --compress zstd --mode stop --storage <name-hypervisor-nas> --note \"$(date +'%Y-%m-%d %H:%M') Backup post installation\""
    ```

19. **Start the server**
    ```bash
    ssh <username-hypervisor>@<hostname-hypervisor> "ha-manager set ct:100 --state started --max_relocate 3 --max_restart 3"
    ```
