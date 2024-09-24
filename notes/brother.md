# Brother

## Table of Contents

- [Brother](#brother)
  - [Table of Contents](#table-of-contents)
  - [Resources](#resources)
  - [Installation Commands](#installation-commands)
  - [Installation Instructions](#installation-instructions)

## Resources

- **Brother MFC-9010CN**: [Driver Download](https://support.brother.com/g/b/downloadtop.aspx?c=ca&lang=en&prod=mfc9010cn_us)
- **Brother DCP-L2520DW**: [Driver Download](https://support.brother.com/g/b/downloadtop.aspx?c=ca&lang=en&prod=dcpl2520dw_us_eu)

## Installation Commands

Download and install the printer drivers using the following commands:

```bash
wget https://download.brother.com/welcome/dlf006893/linux-brprinter-installer-2.2.2-2.gz
gunzip linux-brprinter-installer-*.*.*-*.gz
bash linux-brprinter-installer-*.*.*-* MFC-9010CN
bash linux-brprinter-installer-*.*.*-* DCP-L2520DW
```

## Installation Instructions

1. **Download the Tool** (linux-brprinter-installer-_._._-_.gz)
   The tool will be downloaded to your default "Downloads" directory (e.g., `/home/(LoginName)/Downloads`).

2. **Open a Terminal Window**

3. **Navigate to the Download Directory**
   Use the `cd` command to change to the directory where the file was downloaded.

   ```bash
   cd Downloads
   ```

4. **Extract the Downloaded File**
   Uncompress the downloaded `.gz` file.

   ```bash
   gunzip linux-brprinter-installer-*.gz
   ```

5. **Gain Superuser Access**
   Obtain superuser privileges using either the `su` or `sudo su` command.

6. **Run the Installer**
   Execute the installer script for your Brother printer model.

   ```bash
   bash linux-brprinter-installer-*-* Brother machine name
   ```

   Example:

   ```bash
   bash linux-brprinter-installer-2.1.1-1 MFC-J880DW
   ```

7. **Follow the Installation Prompts**
   The driver installation process will begin. Follow the on-screen instructions.
   When prompted with "Will you specify the DeviceURI?", select:

   - **For USB Users**: Choose `N` (No)
   - **For Network Users**: Choose `Y` (Yes) and provide the DeviceURI number

   The installation process may take some time. Wait until it completes.
