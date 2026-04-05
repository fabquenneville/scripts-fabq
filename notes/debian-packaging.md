# Debian packaging

## Table of Contents

- [Debian packaging](#debian-packaging)
  - [Table of Contents](#table-of-contents)
  - [Upstream documentation](#upstream-documentation)
  - [Required Tools](#required-tools)
  - [Packaging steps](#packaging-steps)
    - [Notes](#notes)

## Upstream documentation

- [Packaging portal](https://wiki.debian.org/Packaging)
  - [Introduction to Debian Packaging](https://wiki.debian.org/Packaging/Intro)
  - [Binary package](https://wiki.debian.org/Packaging/BinaryPackage)
  - [Source package](https://wiki.debian.org/Packaging/SourcePackage)
- [Simple packaging tutorial](https://wiki.debian.org/SimplePackagingTutorial)

## Required Tools

Ensure that you have the necessary tools (`build-essential`, `devscripts`, `debhelper`, `dh-python`, and optionally `lintian` for linting) installed on your Debian system. You can install them using `apt`:

```bash
apt update
apt install build-essential devscripts debhelper dh-python lintian
```

`Lintian` is recommended as it helps ensure your package adheres to Debian standards.

## Packaging steps

**1. Download source archive**
You can either download the source tarball directly from GitHub or create it using Git. Since you have already created it, you can skip the wget step:

- **Direct download (optional)**:

  ```bash
  wget https://github.com/fabquenneville/mediacurator/archive/refs/tags/v1.0.1.tar.gz
  ```

- **Using Git to create the tarball from tag v1.0.1 (already done)**:

  ```bash
  git archive --format=tar.gz --prefix=mediacurator/ v1.0.1 -o /mnt/workbench/builds/mediacurator/v1.0.1/mediacurator_1.0.1.orig.tar.gz
  ```

- **Using Git to create the tarball from the latest commit (already done)**:

  ```bash
  git archive --format=tar.gz --prefix=mediacurator/ HEAD -o /mnt/workbench/builds/mediacurator/v1.0.1/mediacurator_1.0.1.orig.tar.gz
  ```

**2. Extract source archive**

```bash
tar -xvzf mediacurator_1.0.1.orig.tar.gz
```

**3. Create necessary folder**
Create a `debian` directory where all Debian packaging files will reside:

```bash
mkdir debian
mkdir debian/source
```

**4. Create changelog**
Initialize the changelog file with your package version. Make sure to follow Debian formatting standards (`package (version) distribution; urgency=urgency-level`):

```bash
dch --create -v 1.0.1-1 --package mediacurator
```

Example changelog entry:

```text
mediacurator (1.0.1-1) unstable; urgency=medium

  * Initial release

 -- Fabrice Quenneville <fabrice@fabq.ca>  Wed, 23 Oct 2024 10:00:00 +0000
```

**5. Create control files**
Create the necessary files for packaging:

```bash
touch debian/control
touch debian/copyright
touch debian/rules
touch debian/source/format
touch debian/source/options
touch debian/install
```

Explanation of files:

- **`control`**: Contains package metadata (dependencies, package name, description, etc.)
- **`copyright`**: Specifies copyright and license information for your package.
- **`rules`**: The main script for building the package. This file orchestrates the build process.
- **`source/format`**: Defines the source package format, e.g., "3.0 (quilt)" for most packages.
- **`install`**: Lists files to install and their destinations.

**6. Make rules executable**
Make the `rules` file executable, as it's the main script for building the package:

```bash
chmod +x debian/rules
```

**7. Add dependencies in `debian/control`**

Make sure to declare both Python and non-Python dependencies in the `debian/control` file. For example, if your application requires `ffmpeg`:

```text
Depends: ${misc:Depends}, ${python3:Depends}, ffmpeg
```

**8. Copy python source tarball**

Copy your generated source tarball to the appropriate location for Debian packaging:

```bash
cp ./mediacurator-1.0.1.tar.gz ../mediacurator_1.0.1.orig.tar.gz
```

Ensure you are in the correct directory where `mediacurator-1.0.1.tar.gz` exists before running this command.

**9. Run lintian (optional but recommended)**

Before building your package, it’s a good practice to run `lintian` to check for any packaging issues:

```bash
lintian
```

This step ensures your package complies with Debian policy.

**10. Build the package**

Finally, build your Debian package:

```bash
debuild -us -uc
```

**11. Test the package**
After building, you can test the package by installing it:

**With `dpkg`**

```bash
dpkg -i ../mediacurator_1.0.1-1_all.deb
```

**With `apt`**

```bash
apt install ../mediacurator_1.0.1-1_all.deb
```

Then check if it works as expected. If there are missing dependencies, you can run:

```bash
apt --fix-broken install
```

### Notes

- Make sure your `debian/control` and other files are filled with the necessary package information (dependencies, description, etc.).
- Ensure that non-Python dependencies (e.g., `ffmpeg`) are listed in the `debian/control` file.
- If you encounter any issues or errors during the build process, review the output logs for clues on what might need adjusting.
- It’s a good idea to test the `.deb` package after building to ensure it installs and runs as expected.
