# ![Fabrice Quenneville' Logo](https://fabq.ca/img/icons/favicon-32x32.webp) scripts-fabq

**scripts-fabq** is a collection of useful scripts and notes aimed at streamlining command-line operations and improving productivity. This repository is currently incomplete, as I am in the slow process of adding notes and scripts that are stored in closed-source repositories as I revise them.

## 📚 Overview

This repository is structured into several key directories:

- **scripts/**: Contains individual scripts for various tasks. Currently, it includes:

  - `video_remove_audio.py`: A script for removing audio from video files.
  - `video_autoreduce.py`: A script for automatic video resolution reduction of video files.

- **notes/**: A collection of markdown files containing notes on various topics, including:

  - `brother.md`: Information about Brother printers on Linux.
  - `btrfs.md`: Btrfs filesystem configuration and tips.
  - `chrome-driver.md`: Notes on ChromeDriver setup and usage on Linux.
  - `debian packaging.md`: Debian packaging guidelines.
  - `dns.md`: DNS configuration and troubleshooting.
  - `linux.md`: General Linux tips.
  - `pdf.md`: PDF manipulation with Linux command line.
  - `pdftk.md`: PDF Toolkit usage.
  - `pip packaging.md`: Packaging Python projects with pip.
  - `ssh.md`: Secure Shell (SSH) configuration and tips.
  - `wordpress.md`: WordPress debugging and tips.

- **pages/other/**: Templates for other pages, such as the homepage of my Debian package repository. These are provided as inspiration and should not be used as-is.

  - `debrepo.fabq.ca.html`: This file serves as the homepage for my Debian package repository. It provides the instructions to add the repository to user's system's sources list and install packages securely.

- **pages/errors/**: Templates for error pages. These are provided as inspiration and should not be used as-is.

- **pages/static/**: This directory contains static images used throughout the pages in the repository. These images are copyrighted to me and may be used to enhance the visual appeal of the documentation and guides.

- **requests/errors/**: Similar to the `pages/errors/` directory, this contains error pages structured as requests for software like HAProxy.

- **setups/**: A collection of markdown files containing notes on configuring servers, including:
  - `debian_setup_aptly.md`: Comprehensive guide for installing Aptly on Debian.
  - `debian_setup_gitea.md`: Comprehensive guide for installing Gitea on Debian.

## 📖 Documentation

Comprehensive documentation will be published at [https://fabquenneville.github.io/script-fabq/](https://fabquenneville.github.io/script-fabq/) but is not available yet.

## ⚙️ Usage

To use the scripts, navigate to the `scripts` directory and execute the desired script using Python or Bash.

**Example for python:**

```bash
cd scripts
python video_remove_audio.py
```

## 🤝 Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss your ideas.

Please ensure to update any tests as appropriate.

## 📜 License

This project is licensed under the [GNU GPLv3](https://choosealicense.com/licenses/gpl-3.0/)
