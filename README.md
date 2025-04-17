# Netscan Distribution Guide

This guide explains how to build and distribute the `netscan` package.

## Steps to Build the Package

1. **Clean Previous Builds**
   ```bash
   rm -rf build dist *.egg-info
   ```

2. **Build the Package**
   ```bash
   python3 setup.py sdist bdist_wheel
   ```

   This will generate the `.whl` file in the `dist/` directory.

3. **Verify the Build**
   Navigate to the `dist/` directory and confirm the presence of the `.whl` file:
   ```bash
   ls dist/
   ```

## Steps to Install the Package

1. **Copy the `.whl` File**
   Transfer the `.whl` file to the target machine using `scp` or another method:
   ```bash
   scp dist/netscan-1.0.0-py3-none-any.whl <user>@<target-machine>:<destination-path>
   ```

2. **Install the Package**
   On the target machine, install the package using `pip` or `pipx`:
   ```bash
   pip install netscan-1.0.0-py3-none-any.whl
   ```

   Or, if using `pipx`:
   ```bash
   pipx install netscan-1.0.0-py3-none-any.whl
   ```

## Notes
- Ensure all dependencies are listed in `setup.py` under `install_requires`.
- Use `--force` with `pipx` if reinstalling an existing package.