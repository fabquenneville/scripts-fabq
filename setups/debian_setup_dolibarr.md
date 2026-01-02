# Installing Dolibarr on Debian

## Table of Contents

- [Installing Dolibarr on Debian](#installing-dolibarr-on-debian)
  - [Table of Contents](#table-of-contents)
  - [Introduction](#introduction)
  - [Why Dolibarr?](#why-dolibarr)
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

Welcome to the installation guide for Dolibarr on Debian. Dolibarr is an open-source ERP and CRM platform designed for small and medium-sized businesses, offering features such as invoicing, accounting, inventory management, and customer relationship management through a clean, web-based interface. By following this guide, you’ll be able to install and configure Dolibarr on your Debian system efficiently.

## Why Dolibarr?

Dolibarr is a flexible and open-source ERP/CRM solution that allows you to keep full control over your business data and infrastructure. It covers a wide range of needs for small and medium-sized organizations, including invoicing, accounting, customer management, inventory, and project tracking, all from a single web interface. Being self-hosted, Dolibarr gives you data ownership, transparency, and the ability to customize or extend the platform to fit your workflows without relying on third-party SaaS providers.

## Prerequisites

Before you begin the installation process, ensure that your Debian system meets the following requirements:

- Debian GNU/Linux 9 (Stretch) or later
- Access to a terminal with sudo privileges
- Basic familiarity with the command line interface
- Stable internet connection to download necessary packages

## What This Guide Covers

This guide will walk you through the installation of Dolibarr on Debian step by step, covering:

1. **Installation**: Installing Dolibarr from the official Git repository.
2. **Configuration**: Adjusting Dolibarr and system settings to match your environment.
3. **Web Setup**: Configuring Dolibarr with Apache and accessing the web installer.
4. **Security**: Hardening Debian, PHP, and Dolibarr for a production setup.

## Placeholders

Replace the placeholders below with the appropriate values for your setup:

- **User Details**

  - Username: `<username>` (e.g., admin)
  - Username - Hypervisor: `<username-hypervisor>` (e.g., admin)

- **Server Configuration**

  - Server IP address: `<server-ip-address>` (e.g., 192.168.1.100)
  - Hostname - Intranet: `<hostname-intranet>` (e.g., dolibarr-server.domain.com)
  - Hostname - Internet: `<hostname-internet>` (e.g., dolibarr.domain.com)
  - Hostname - Hypervisor: `<hostname-hypervisor>` (e.g., proxmox-hypervisor.domain.com)
  - Hostname - Hypervisor NAS: `<hostname-hypervisor-nas>` (e.g., nas-server.domain.com)
  - Name - Hypervisor NAS: `<name-hypervisor-nas>` (e.g., nas-server)
  - Container ID - Hypervisor: `<container-id-hypervisor>` (e.g., 100)

- **SSH Keys**

  - SSH key - Proxmox: `<ssh-key-proxmox>` (e.g., /home/user/.ssh/id_rsa.pub)
  - SSH key - Client: `<ssh-key-client>` (e.g., /home/user/.ssh/client_id_rsa.pub)

- **Networking**

  - Wireguard port: `<wireguard-port>` (e.g., 51820)

- **Dolibarr specifics post-install**

  - Contract paths: `<dolibarr-contract-paths-source>` (e.g., /home/username/contracts/)
  - Fonts paths: `<dolibarr-fonts-paths-source>` (e.g., /home/username/fonts/)

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

- [Setup other](https://wiki.dolibarr.org/index.php?title=Setup_Other)
- [Create an ODT or ODS document template](https://wiki.dolibarr.org/index.php?title=Create_an_ODT_or_ODS_document_template)
- [Setup Other](https://wiki.dolibarr.org/index.php?title=Setup_Other)
- [List of releases, change log and compatibilities](https://wiki.dolibarr.org/index.php?title=List_of_releases,_change_log_and_compatibilities)
- [GitHub](https://github.com/Dolibarr/dolibarr)

### Links

- [https](https://<hostname-intranet>/)
- [http](http://<hostname-intranet>/)
- [local https](https://<hostname-intranet>/)
- [local http](http://<hostname-intranet>/)
- [<server-ip-address>](http://<server-ip-address>/)

### Software on the Machine

- **Operating System**: Debian
- **Database**: MariaDB (configured as MySQL)
- **Web Server**: Apache
- **Security**: GnuPG, WireGuard, UFW
- **Other**: Git, sudo, certbot (for SSL certificate management)

### Paths

- **Dolibarr Configuration**: `/etc/dolibarr/app.ini`
- **Dolibarr Work Path**: `/var/lib/dolibarr`

### Proxmox Commands

**List available Proxmox templates**

```bash
ssh <username>@<hostname-hypervisor-nas> "ls /mnt/proxmox/template/cache/"
```

**Create the container**

```bash
ssh <username-hypervisor>@<hostname-hypervisor> "pct create <container-id-hypervisor> <name-hypervisor-nas>:vztmpl/debian-12-upgraded_12.5_amd64.tar.zst --hostname <hostname-intranet> --cores 4 --memory 4096 --swap 2048 --net0 name=net0,bridge=vmbr0,ip=dhcp,firewall=1 --rootfs <name-hypervisor-nas>:250 --unprivileged 1 --features nesting=1 --ssh-public-keys <ssh-key-proxmox>"
```

**Backup**

```bash
ssh <username-hypervisor>@<hostname-hypervisor> "vzdump <container-id-hypervisor> --compress zstd --mode stop --storage <name-hypervisor-nas> --note \"$(date +'%Y-%m-%d %H:%M') Backup fresh install\""
```

**Set the state of the Proxmox HA Manager for Container <container-id-hypervisor>**

```bash
ssh <username-hypervisor>@<hostname-hypervisor> "ha-manager add ct:<container-id-hypervisor>"
ssh <username-hypervisor>@<hostname-hypervisor> "ha-manager remove ct:<container-id-hypervisor>"
```

**Set the state and limits of the Proxmox Container <container-id-hypervisor> in the HA Manager**

```bash
ssh <username-hypervisor>@<hostname-hypervisor> "ha-manager set ct:<container-id-hypervisor> --state started --max_relocate 3 --max_restart 3"
ssh <username-hypervisor>@<hostname-hypervisor> "ha-manager set ct:<container-id-hypervisor> --state stopped"
ssh <username-hypervisor>@<hostname-hypervisor> "pct start <container-id-hypervisor>"
ssh <username-hypervisor>@<hostname-hypervisor> "pct stop <container-id-hypervisor>"
ssh <username-hypervisor>@<hostname-hypervisor> "pct reboot <container-id-hypervisor>"
```

**Destroy the Proxmox Container <container-id-hypervisor> forcefully**

```bash
ssh <username-hypervisor>@<hostname-hypervisor> "pct destroy <container-id-hypervisor> --force --purge"
```

**Move the Proxmox Container <container-id-hypervisor> to another host**

```bash
ssh <username-hypervisor>@<hostname-hypervisor> "pct migrate <container-id-hypervisor> hv2"
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
   ssh <username-hypervisor>@<hostname-hypervisor> "vzdump <container-id-hypervisor> --compress zstd --mode stop --storage <name-hypervisor-nas> --note \"$(date +'%Y-%m-%d %H:%M') Backup fresh install\""
   ```

3. **Install Required Dependencies**

   **Upgrade the base system**

   ```bash
   apt update
   apt upgrade -y
   ```

   **Install dependencies**

   - [Prerequisites](https://wiki.dolibarr.org/index.php?title=Prerequisites)
   - [Dolibarr downloads](https://www.dolibarr.org/downloads.php)
   - [Dolibarr Sourceforge Debian packages](https://sourceforge.net/projects/dolibarr/files/Dolibarr%20installer%20for%20Debian-Ubuntu%20%28DoliDeb%29/20.0.3/)

   ```bash
   apt install -y git apache2 mariadb-server php php-mysql php-mbstring php-gd php-curl php-xml php-intl php-imap php-zip libapache2-mod-php sudo
   apt install -y libreoffice-common libreoffice-writer --no-install-recommends
   apt install -y fonts-dejavu fonts-liberation ttf-mscorefonts-installer

   apt install -y gpg
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
   adduser <username>
   usermod -aG sudo <username>
   ```

   ```bash
   mkdir -p /home/www-data
   chown www-data:www-data /home/www-data
   usermod -d /home/www-data www-data
   usermod -s /bin/bash www-data
   ```

   ```bash
   adduser --system --shell /bin/bash --gecos 'Dolibarr CRM' --group --disabled-password --home /home/www-data www-data
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
       CREATE USER 'dolibarr' IDENTIFIED BY '';
       ```

       ```sql
       CREATE USER IF NOT EXISTS 'dolibarr'@'192.168.1.%' IDENTIFIED BY '';
       GRANT ALL PRIVILEGES ON *.* TO 'dolibarr'@'192.168.1.%' IDENTIFIED BY '' WITH GRANT OPTION;
       GRANT ALL PRIVILEGES ON *.* TO 'dolibarr'@'localhost' IDENTIFIED BY '' WITH GRANT OPTION;
       SET PASSWORD FOR 'dolibarr'@'localhost' = PASSWORD('');
       SET PASSWORD FOR 'dolibarr'@'192.168.1.%' = PASSWORD('');
       FLUSH PRIVILEGES;
       ```

    3. **Create Dolibarr Database**

       ```bash
       mariadb -u root -p
       ```

       Inside the MariaDB shell:

       ```sql
       CREATE DATABASE dolibarr;
       CREATE USER 'dolibarruser'@'localhost' IDENTIFIED BY 'strongpassword';
       GRANT ALL PRIVILEGES ON dolibarr.* TO 'dolibarruser'@'localhost';
       FLUSH PRIVILEGES;
       EXIT;
       ```

11. **Install Dolibarr**

    [Versions](https://wiki.dolibarr.org/index.php?title=List_of_releases,_change_log_and_compatibilities)

    ```bash
    sudo su -
    mv /var/www/html /var/www/.html

    cd /var/www
    git clone --depth 1 -b 20.0.3 https://github.com/Dolibarr/dolibarr.git dolibarr
    mv dolibarr-20.0.3 dolibarr
    ```

12. **Create required directory structure**

    ```bash
    chmod -R 755 /var/www/dolibarr
    chown -R www-data:www-data /var/www/dolibarr
    cd dolibarr ; touch htdocs/conf/conf.php ; chown www-data htdocs/conf/conf.php
    mkdir -p /var/lib/dolibarr/sessions ; chown www-data /var/lib/dolibarr/sessions
    mkdir -p /var/lib/dolibarr/documents ; chown www-data /var/lib/dolibarr/documents
    ```

13. **Apache Configuration**

    1. **Allow http https**

       ```bash
       ufw allow https
       ufw allow http
       ```

    2. **Backup Default Files**
       Backup the default index.html and configuration files.

       ```bash
       mv /var/www/html /var/www/.html
       mv /etc/apache2/sites-available/000-default.conf /etc/apache2/sites-available/.000-default.conf
       rm /etc/apache2/sites-enabled/000-default.conf
       ```

    3. **Create Default Server Block for Unauthorized Access**

    4. **Site configuration**

       Edit the Apache configuration file to proxy to the Dolibarr CRM.

       ```bash
       nano /etc/apache2/sites-available/<hostname-intranet>.conf
       ```

       Add the following configuration:

       ```apache
       <VirtualHost *:80>
           LogLevel info
           ServerName <hostname-intranet>
           ServerAdmin admin@fabq.ca
           DocumentRoot /var/www/dolibarr

           # Alias for Dolibarr
           Alias / /var/www/dolibarr/htdocs/

           <Directory /var/www/dolibarr/htdocs>
               Options +FollowSymLinks
               AllowOverride All
               Require all granted
           </Directory>

           ErrorLog ${APACHE_LOG_DIR}/error.dolibarr.log
           CustomLog ${APACHE_LOG_DIR}/access.dolibarr.log combined
       </VirtualHost>
       ```

    5. **Enabling the new VirtualHost**

       ```bash
       a2ensite <hostname-intranet>.conf
       a2enmod rewrite
       ```

    6. **Managing Apache**

       **Enable Apache**

       ```bash
       systemctl enable apache2
       ```

       **Apache reload**

       ```bash
       systemctl reload apache2
       ```

       **`Optional` Apache restart**

       ```bash
       systemctl restart apache2
       ```

14. **Create folders**

    ```bash
    mkdir -p /var/tmp
    mkdir -p /var/upload_tmp
    ```

15. **Set temporary file paths**

    ```bash
    nano /etc/php/8.2/apache2/php.ini
    ```

    ```ini
    sys_temp_dir = "/var/tmp"
    upload_tmp_dir = "/var/upload_tmp"
    open_basedir = "/var/www/dolibarr:/var/lib/dolibarr/documents:/var/lib/dolibarr/sessions:/var/tmp:/var/upload_tmp"
    ```

16. **Fix permissions**

    ```bash
    chown -R www-data:www-data /var/lib/php/sessions

    chown -R www-data:www-data /var/www/dolibarr/htdocs/conf/conf.php
    chmod 640 /var/www/dolibarr/htdocs/conf/conf.php

    find /var/www/dolibarr -type d -exec chmod 755 {} \;
    find /var/www/dolibarr -type f -exec chmod 644 {} \;

    chmod go-w /var/lib/dolibarr/documents;
    chmod go-w /var/lib/dolibarr/sessions;

    chown -R www-data:www-data /var/tmp
    chown -R www-data:www-data /var/upload_tmp
    chmod -R 750 /var/tmp
    chmod -R 750 /var/upload_tmp
    ```

17. **Secure PHP**

    ```bash
    nano /etc/php/8.2/apache2/php.ini
    ```

    ```ini
    session.use_strict_mode = 1

    allow_url_fopen = No

    disable_functions = dl, apache_note, apache_setenv, pcntl_alarm, pcntl_fork, pcntl_waitpid, pcntl_wait, pcntl_wifexited, pcntl_wifstopped, pcntl_wifsignaled, pcntl_wifcontinued, pcntl_wexitstatus, pcntl_wtermsig, pcntl_wstopsig, pcntl_signal, pcntl_signal_get_handler, pcntl_signal_dispatch, pcntl_get_last_error, pcntl_strerror, pcntl_sigprocmask, pcntl_sigwaitinfo, pcntl_sigtimedwait, pcntl_exec, pcntl_getpriority, pcntl_setpriority, pcntl_async_signals, show_source, virtual, passthru, shell_exec, system, proc_open, popen

    session.gc_maxlifetime = 604800
    ```

18. **Complete the Installation through Web Interface**

    - Open your web browser and navigate to `http://<hostname-intranet>/install/`
    - Follow the on-screen instructions to complete the installation.

19. **Lock installation**

    ```bash
    chmod -w /var/www/dolibarr/htdocs/conf/conf.php
    touch /var/lib/dolibarr/documents/install.lock;
    chmod go-w /var/lib/dolibarr/documents;
    ```

20. **Secure installation**

    ```bash
    chmod -R -w /var/www/dolibarr/htdocs
    cp /etc/php/8.4/apache2/php.ini /etc/php/8.4/apache2/php.ini.back
    nano /etc/php/8.4/apache2/php.ini
    ```

    ```ini
    session.save_path = /var/lib/dolibarr/sessions
    session.use_strict_mode = 1
    session.use_only_cookies = 1
    session.cookie_httponly = 1
    session.cookie_samesite = Lax
    session.gc_maxlifetime = 604800
    open_basedir = "/var/www/dolibarr:/var/lib/dolibarr/documents:/var/lib/dolibarr/sessions:/var/tmp:/var/upload_tmp"
    short_open_tag = Off
    allow_url_fopen = Off
    allow_url_include = Off
    disable_functions = dl, apache_note, apache_setenv, pcntl_alarm, pcntl_fork, pcntl_waitpid, pcntl_wait, pcntl_wifexited, pcntl_wifstopped, pcntl_wifsignaled, pcntl_wifcontinued, pcntl_wexitstatus, pcntl_wtermsig, pcntl_wstopsig, pcntl_signal, pcntl_signal_get_handler, pcntl_signal_dispatch, pcntl_get_last_error, pcntl_strerror, pcntl_sigprocmask, pcntl_sigwaitinfo, pcntl_sigtimedwait, pcntl_exec, pcntl_getpriority, pcntl_setpriority, pcntl_async_signals, show_source, virtual, passthru, shell_exec, system, proc_open, popen
    ```

    ```bash
    nano /var/www/dolibarr/htdocs/conf/conf.php
    chmod o-r /var/www/dolibarr/htdocs/conf/conf.php
    ```

    ```php
    $dolibarr_main_prod='1';
    ```

21. **Configure SSL with Certbot (Optional, If directly accessed)**

    ```bash
    certbot --apache -d <hostname-internet>
    systemctl status certbot.timer
    certbot renew --dry-run
    ```

22. **Verify installation**

    - Verify that the Dolibarr instance is installed restored by accessing it through a web browser. Ensure that all repositories, users, and configurations are intact.

    ```bash
    systemctl status apache2
    ```

    Visit the server at [http://<hostname-internet>](http://<hostname-internet>) or [https://<hostname-internet>](https://<hostname-internet>).

23. **Backup post installation**

    ```bash
    ssh <username-hypervisor>@<hostname-hypervisor> "ha-manager set ct:<container-id-hypervisor> --state stopped"
    ssh <username-hypervisor>@<hostname-hypervisor> "vzdump <container-id-hypervisor> --compress zstd --mode stop --storage <name-hypervisor-nas> --note \"$(date +'%Y-%m-%d %H:%M') Backup post installation\""
    ```

24. **Start the server**

    ```bash
    ssh <username-hypervisor>@<hostname-hypervisor> "ha-manager set ct:<container-id-hypervisor> --state started --max_relocate 3 --max_restart 3"
    ```

25. **Move contracts**

    ```bash
    scp '<dolibarr-contract-paths-source>/contract.odt' <username>@<hostname-intranet>:~/

    sudo su -
    mv /home/<username>/*.odt /var/lib/dolibarr/documents/doctemplates/contracts/
    chown -R www-data:www-data /var/lib/dolibarr/documents/doctemplates/contracts/
    ```

26. **ODT to PDF**

    [See forum 1](https://www.dolibarr.org/forum/t/solved-odt-to-pdf/16931)
    [See forum 2](https://www.dolibarr.org/forum/t/setup-dolibarr-to-generate-odt-to-pdf/22112/9)

    ```bash
    MAIN_ODT_AS_PDF
    ```

27. **Install fonts**

    ```bash
    scp -r <dolibarr-fonts-paths-source>/Lato <username>@<hostname-intranet>:~/
    ```

    ```bash
    mv /home/<username>/Lato /usr/local/share/fonts/
    chmod -R 755 /usr/local/share/fonts/
    chown -R root:root /usr/local/share/fonts/
    ```
