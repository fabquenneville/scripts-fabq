# Pip packaging

## Table of Contents

- [Pip packaging](#pip-packaging)
  - [Table of Contents](#table-of-contents)
  - [Required Tools](#required-tools)
  - [Credentials](#credentials)
  - [Build the package](#build-the-package)
  - [Upload package](#upload-package)
    - [Upload to Test PyPI](#upload-to-test-pypi)
    - [Upload to Live PyPI](#upload-to-live-pypi)

## Required Tools

Ensure that you have the necessary tools (`python3-setuptools`, `python3-wheel`, and `twine`) installed on your Debian system. You can install them using `apt`:

```bash
apt update
apt install python3-setuptools python3-wheel twine
```

## Credentials

Check if your credentials for PyPI and Test PyPI are stored in `~/.pypirc`:

```bash
cat ~/.pypirc
```

Ensure you have the correct tokens and repository configurations in this file if you plan to use token-based authentication for uploads.

## Build the package

Navigate to your project directory (where `setup.py` is located) and build the distribution files. This will generate both a source distribution and a wheel.

```bash
python3 setup.py sdist bdist_wheel
```

The above command will create a `dist/` folder containing `.tar.gz` and `.whl` files.

## Upload package

### Upload to Test PyPI

To upload your package to Test PyPI (a test environment that mirrors the real PyPI), use the following command:

```bash
twine upload --repository-url https://test.pypi.org/legacy/ dist/*
```

You can also specify a particular version of your package:

```bash
twine upload --repository-url https://test.pypi.org/legacy/ dist/MediaCurator-0.0.10*
```

You can also specify the repository from ~/.pypirc:

```bash
twine upload --repository testpypi dist/MediaCurator-0.0.10*
```

You will be prompted to enter your Test PyPI username and password.

**Note:**

If you're having trouble remembering your credentials, you can create or manage your account at [Test PyPI](https://test.pypi.org/account/register/).

**Install the Package from Test PyPI**

To test the package installation from Test PyPI, you can use the following command:

```bash
pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ mediacurator
```

This command first checks Test PyPI for the package and falls back to the official PyPI for dependencies.

### Upload to Live PyPI

Once you are confident everything works, you can upload the package to the real PyPI using:

```bash
twine upload dist/*
```

You can also specify the version:

```bash
twine upload dist/MediaCurator-0.0.10*
```

You can also specify the repository-url:

```bash
twine upload --repository-url https://test.pypi.org/legacy/ dist/MediaCurator-0.0.10*
```

You can also specify the repository from ~/.pypirc:

```bash
twine upload --repository mediacurator dist/MediaCurator-0.0.10*
```

Ensure your PyPI token is configured or provide it directly during the upload:

```bash
twine upload -u __token__ -p <your-testpypi-token> dist/MediaCurator-0.0.10*
```

You will need your credentials for your PyPI account, which you can create/manage at [PyPI](https://pypi.org/account/register/).

---

**Notes**

- Ensure your version numbers are updated in `setup.py` before uploading a new package version.
- Always test your package thoroughly using Test PyPI before uploading to the live PyPI to avoid breaking releases.
