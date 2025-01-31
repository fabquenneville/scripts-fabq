# Installing Wordpress on AlmaLinux

## Table of Contents

- [Installing Wordpress on AlmaLinux](#installing-wordpress-on-almalinux)
  - [Table of Contents](#table-of-contents)
  - [Disclaimer: Incomplete Guide](#disclaimer-incomplete-guide)
  - [Introduction](#introduction)
  - [Why WordPress?](#why-wordpress)
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

Welcome to the installation guide for WordPress on AlmaLinux in a Proxmox LXC container. WordPress is a powerful content management system (CMS) that allows you to create and manage websites efficiently.

## Why WordPress?

WordPress is one of the most popular content management systems (CMS) in the world, powering over 40% of websites on the internet. It offers a flexible and user-friendly platform for building anything from simple blogs to complex e-commerce sites.

**Key Benefits:**

- **Open-Source & Free** – No licensing fees, with a large community contributing to its continuous development.
- **Extensive Plugin Ecosystem** – Thousands of plugins to add features like SEO, security, performance optimization, and more.
- **Customizable Themes** – A wide variety of free and premium themes allow you to tailor your website's design.
- **SEO-Friendly** – Built-in SEO features and plugins like Yoast SEO help improve search engine rankings.
- **Scalability** – Suitable for small personal blogs to large enterprise websites with high traffic.
- **Active Community & Support** – Large developer and user communities provide extensive documentation, forums, and professional support options.

Whether you're launching a blog, a portfolio, or a business website, WordPress provides the flexibility and power to meet your needs.

## Prerequisites

Before you begin the installation process, ensure that your AlmaLinux system meets the following requirements:

- AlmaLinux GNU/Linux 9 or later
- Access to a terminal with sudo privileges
- Basic familiarity with the command line interface
- Stable internet connection to download necessary packages

## What This Guide Covers

This guide covers the installation and configuration of Wordpress on an AlmaLinux server, along with additional setup tasks such as SSH connection management and Proxmox commands. It covers:

1. **Installation**: Installing Wordpress from the official site.
2. **Configuration**: Configuring Wordpress to suit your environment and preferences.
3. **Setup**: Setting up Wordpress as a service and accessing it.

## Placeholders

Replace the placeholders below with the appropriate values for your setup:

- **User Details**

  - Username: `<username>` (e.g., admin)
  - Username - Hypervisor: `<username-hypervisor>` (e.g., admin)

- **Server Configuration**

  - Server IP address: `<server-ip-address>` (e.g., 192.168.1.100)
  - Hostname - Intranet: `<hostname-intranet>` (e.g., wordpress-server.domain.com)
  - Hostname - Internet: `<hostname-internet>` (e.g., wordpress.domain.com)
  - Hostname - Hypervisor: `<hostname-hypervisor>` (e.g., proxmox-hypervisor.domain.com)
  - Hostname - Hypervisor NAS: `<hostname-hypervisor-nas>` (e.g., nas-server.domain.com)
  - Name - Hypervisor NAS: `<name-hypervisor-nas>` (e.g., nas-server)
  - Container ID: `<container-id>` (e.g., 100)

- **SSH Keys**

  - SSH key - Proxmox: `<ssh-key-proxmox>` (e.g., /home/user/.ssh/id_rsa.pub)
  - SSH key - Client: `<ssh-key-client>` (e.g., /home/user/.ssh/client_id_rsa.pub)

- **Networking**

  - Wireguard port: `<wireguard-port>` (e.g., 51820)

- **Database**

  - Database password : `<database-password>` (e.g., 15GbGnOn3Vjy9RQ4G9TfUF95wPcoKAy5)

- **Paths**

  - Path index: `<path-index>` (e.g., /var/www/html)

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

- [AlmaLinux Wiki](https://wiki.almalinux.org/)
- [Documentation Overview](https://www.wordpress.info/doc/overview/)
- [Tutorials](https://wordpress.com/learn/)

### Links

- [Wordpress appliance](https://<hostname-internet>/)

### Software on the Machine

- **Operating System**: AlmaLinux
- **Web Server**: Apache
- **Database**: Mariadb
- **Security**: GnuPG, WireGuard, firewalld
- **Other**: Git, sudo

### Paths

- **Apache AlmaLinux Default Configuration**: `/etc/httpd/conf.d/welcome.conf`
- **Wordpress Configuration**: `/var/www/html/wp-config.php`
- **Wordpress Work Path**: `/var/www/html`

### Proxmox Commands

**List available Proxmox templates**

```bash
ssh <username>@<hostname-hypervisor-nas> "ls /mnt/proxmox/template/cache/"
```

**Create the container**

```bash
ssh <username-hypervisor>@<hostname-hypervisor> "pct create <container-id> <name-hypervisor-nas>:vztmpl/almalinux-9-default_20240911_amd64.tar.xz --hostname <hostname-intranet> --cores 2 --memory 4096 --swap 2048 --net0 name=net0,bridge=vmbr0,ip=dhcp,firewall=1 --rootfs <name-hypervisor-nas>:100 --unprivileged 1 --features nesting=1 --ssh-public-keys <ssh-key-proxmox>"
```

**Backup**

```bash
ssh <username-hypervisor>@<hostname-hypervisor> "vzdump <container-id> --compress zstd --mode stop --storage <name-hypervisor-nas> --note \"$(date +'%Y-%m-%d %H:%M') Backup fresh install\""
```

**Set the state of the Proxmox HA Manager for Container <container-id>**

```bash
ssh <username-hypervisor>@<hostname-hypervisor> "ha-manager add ct:<container-id>"
ssh <username-hypervisor>@<hostname-hypervisor> "ha-manager remove ct:<container-id>"
```

**Set the state and limits of the Proxmox Container <container-id> in the HA Manager**

```bash
ssh <username-hypervisor>@<hostname-hypervisor> "ha-manager set ct:<container-id> --state started --max_relocate 3 --max_restart 3"
ssh <username-hypervisor>@<hostname-hypervisor> "ha-manager set ct:<container-id> --state stopped"
ssh <username-hypervisor>@<hostname-hypervisor> "pct start <container-id>"
ssh <username-hypervisor>@<hostname-hypervisor> "pct stop <container-id>"
ssh <username-hypervisor>@<hostname-hypervisor> "pct reboot <container-id>"
```

**Destroy the Proxmox Container <container-id> forcefully**

```bash
ssh <username-hypervisor>@<hostname-hypervisor> "pct destroy <container-id> --force --purge"
```

**Move the Proxmox Container <container-id> to another host**

```bash
ssh <username-hypervisor>@<hostname-hypervisor> "pct migrate <container-id> hv2"
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

## Installation Procedure

1. **Fresh AlmaLinux Installation**

   - Install a fresh AlmaLinux operating system on your new server following the standard installation procedure.

2. **Backup before starting**

   ```bash
   ssh <username-hypervisor>@<hostname-hypervisor> "vzdump <container-id> --compress zstd --mode stop --storage <name-hypervisor-nas> --note \"$(date +'%Y-%m-%d %H:%M') Backup fresh install\""
   ```

3. **Install Required Dependencies**

   **Upgrade the base system**

   ```bash
   dnf update
   ```

   **Enable EPEL repository**
   Extra Package for Enterprise Linux repository has packages like Apache and Nginx

   ```bash
   dnf install -y epel-release
   dnf makecache
   ```

4. **Install LAMP Stack**

   **Install dependencies**

   ```bash
   dnf install -y sudo nano firewalld firewall-config tar wget curl unzip
   dnf install -y gnupg nginx git wireguard-tools

   dnf install -y httpd httpd-tools mariadb-server mariadb

   # Basic command
   dnf install -y php php-mysqlnd php-fpm php-json php-mbstring php-xml php-curl php-zip php-gd php-intl php-bcmath php-soap php-exif
   # More tooling and security
   dnf install -y httpd mod_ssl php php-cli php-common php-fpm php-gd php-intl php-json php-mbstring php-mysqlnd php-opcache php-pdo php-pecl-imagick php-xml php-zip  policycoreutils-python-utils
   # Other xml php modules
   dnf install -y php-dom php-simplexml php-xmlreader php-iconv php-posix php-sockets php-tokenizer
   ```

   **WordPress Dependencies on AlmaLinux (MariaDB)**

   **Web Server**

   - `httpd` (Apache)
   - `mod_ssl` (For HTTPS support)
   - OR `nginx` (If using Nginx instead of Apache)

   **PHP**

   - `php` (Main PHP package)
   - `php-cli` (Command-line interface for PHP)
   - `php-common` (Common PHP files)
   - `php-fpm` (FastCGI Process Manager for PHP, required for Nginx)
   - `php-gd` (Image processing)
   - `php-intl` (Internationalization)
   - `php-json` (JSON support)
   - `php-mbstring` (Multibyte string functions)
   - `php-mysqlnd` (MySQL/MariaDB support)
   - `php-opcache` (Performance optimization)
   - `php-pdo` (PHP Data Objects)
   - `php-pecl-imagick` (ImageMagick extension, recommended for media handling)
   - `php-xml` (XML parsing)
   - `php-zip` (ZIP file support)

   **Database (MariaDB)**

   - `mariadb-server` (MariaDB database server)
   - `mariadb` (MariaDB client)

   **Additional System Packages**

   - `tar` (Required for extracting WordPress archives)
   - `wget` (To fetch files from the web)
   - `curl` (For network requests)
   - `unzip` (Extracting ZIP files)
   - `policycoreutils-python-utils` (SELinux tools, required if SELinux is enabled)
   - `firewalld` (For firewall management, if needed)

   **Optional Debugging & Performance Tools**

   - `php-pecl-apcu` (APC User Cache for PHP)
   - `php-pecl-memcached` (Memcached support)
   - `php-pecl-redis` (Redis support)

5. **Ensure Hostname**

   ```bash
   nano /etc/hosts
   # Add line: 127.0.1.1 <hostname-intranet>
   nano /etc/hostname
   # Set to: <hostname-intranet>
   hostnamectl set-hostname <hostname-intranet>
   ```

6. **Add Users and set Credentials**

   ```bash
   passwd root
   ```

   ```bash
   adduser <username>
   passwd <username>

   groupadd sudo
   usermod -aG sudo <username>
   nano /etc/sudoers
   ```

   ```
   ## Allows people in group sudo to run all commands
   %sudo ALL=(ALL)       ALL
   ```

7. **Setup SSH Connectors**

   - Configure SSH connectors as per your setup script to establish secure connections to the server.

8. **Test users, SSH, and sudo**

   1. **Transfer SSH keys for User**
   2. **Connect as User with SSH key**
   3. **Test sudo**

   ```bash
   sudo su -
   ```

   4. **Disconnect as root**

9. **Secure SSH**

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

10. **Configure Firewall**

    **Open ports**

    ```bash
    firewall-cmd --permanent --zone=public --add-service=ssh
    firewall-cmd --permanent --zone=public --add-service=http
    firewall-cmd --permanent --zone=public --add-service=https
    firewall-cmd --permanent --zone=public --add-port=<wireguard-port>/udp
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

11. **Start Apache And MariaDB**

    ```bash
    systemctl enable httpd --now
    systemctl enable mariadb --now
    ```

    Now, your web server is available at `http://<hostname-intranet>`.

12. **Create PHP test page**

    ```bash
    echo "<?php phpinfo() ?>" > /var/www/html/info.php
    ```

    Now, your web server php information is available at `http://<hostname-intranet>/info.php`.

    ```bash
    rm /var/www/html/info.php
    ```

13. **Secure MariaDB Installation**

    ```bash
    mysql_secure_installation
    ```

14. **Creating the new Database**

    ```bash
    mariadb
    ```

    ```sql
    CREATE DATABASE wordpress;
    CREATE USER `admin`@`localhost` IDENTIFIED BY '<database-password>';
    GRANT ALL ON wordpress.* TO `admin`@`localhost`;
    FLUSH PRIVILEGES;
    EXIT;
    ```

15. **Download and Extract WordPress**

    ```bash
    curl https://wordpress.org/latest.tar.gz --output wordpress.tar.gz
    tar xf wordpress.tar.gz
    cp -r wordpress/* /var/www/html/
    ```

16. **Modify Permissions**

    Set appropriate ownership and adjust the SELinux security context for WordPress files:

    ```bash
    chown -R apache:apache /var/www/html
    chmod -R 755 /var/www/html
    ```

    Enable Apache's ability to establish network connections, allowing WordPress to download updates and plugins:

    ```bash
    setsebool -P httpd_can_network_connect true
    ```

17. **Allow Override**

    ```bash
    nano /etc/httpd/conf/httpd.conf
    ```

    Allow Overrides on `/var/www` and `/var/www/html`:

    ```apache
    AllowOverride All
    ```

18. **Configure Wordpress**

    Now, visit `http://<hostname-intranet>` to follow the wordpress configuration.

19. **Configure WireGuard**

    ```bash
    nano /etc/wireguard/proxy-lan.conf
    systemctl enable wg-quick@proxy-lan --now
    wg show
    ```

20. **Back-up post installation**

    ```bash
    ssh <username-hypervisor>@<hostname-hypervisor> "ha-manager set ct:<container-id> --state stopped"
    ssh <username-hypervisor>@<hostname-hypervisor> "vzdump <container-id> --compress zstd --mode stop --storage <name-hypervisor-nas> --note \"$(date +'%Y-%m-%d %H:%M') Backup post installation\""
    ```

21. **Start the server**

    ```bash
    ssh <username-hypervisor>@<hostname-hypervisor> "pct start <container-id>"
    ssh <username-hypervisor>@<hostname-hypervisor> "ha-manager set ct:<container-id> --state started --max_relocate 3 --max_restart 3"
    ```
