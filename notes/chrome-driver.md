# Installing ChromeDriver on Linux

## Table of Contents

- [Installing ChromeDriver on Linux](#installing-chromedriver-on-linux)
  - [Table of Contents](#table-of-contents)
  - [Download and Install ChromeDriver](#download-and-install-chromedriver)
    - [Install Steps](#install-steps)
  - [Verify Installation](#verify-installation)

## Download and Install ChromeDriver

Before proceeding, check the official ChromeDriver downloads page for the latest release:  
[https://sites.google.com/chromium.org/driver/downloads](https://sites.google.com/chromium.org/driver/downloads)

### Install Steps

Navigate to the `/bin` directory:

```bash
cd /bin
```

Download the specific version of ChromeDriver (replace with the latest version if necessary):

```bash
wget https://chromedriver.storage.googleapis.com/102.0.5005.61/chromedriver_linux64.zip
```

Unzip the downloaded file:

```bash
unzip chromedriver_linux64.zip
```

Remove the zip file after extraction:

```bash
rm chromedriver_linux64.zip
```

Make the `chromedriver` executable:

```bash
chmod +x chromedriver
```

Move the `chromedriver` binary to `/bin`:

```bash
sudo mv chromedriver /bin/
```

Update the `PATH` environment variable:

```bash
export PATH=$PATH:/bin/chromedriver
```

## Verify Installation

To verify the installation was successful, check the ChromeDriver version:

```bash
chromedriver --version
```
