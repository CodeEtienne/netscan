# Netscan Distribution Guide

This guide explains how to build and distribute the `netscan` package.

## About Netscan

Netscan is a simple network scanner that allows you to scan a network range or a specific hostname for open ports. It provides detailed results, including IP addresses, hostnames, port statuses, and associated services. The tool is designed to be lightweight and easy to use, with options for scanning common ports, specifying custom ports, and exporting results to CSV or JSON files. It supports both IPv4 and IPv6 scanning.

## Command-Line Help

Below is the output of the `-h` (help) option for the `netscan` command:

```
usage: netscan [-h] [-p [PORT [PORT ...]]] [--common-ports] [-t TIMEOUT]
               [--verbose] [--output-csv OUTPUT_CSV] [--show-all]
               network

Simple network scanner

positional arguments:
  network               CIDR network range to scan (e.g., 192.168.1.0/24) or a simple hostname

optional arguments:
  -h, --help            show this help message and exit
  -p [PORT [PORT ...]], --port [PORT [PORT ...]]
                        TCP port(s) to scan (e.g., -p 80 443)
  --common-ports        Scan a list of common ports (e.g., FTP, SSH, HTTP, etc.). Common ports include: 21 (FTP), 22 (SSH), 23 (Telnet), 25 (SMTP), 53 (DNS), 80 (HTTP), 110 (POP3), 139 (NetBIOS), 143 (IMAP), 443 (HTTPS), 445 (SMB), 3389 (RDP).
  -t TIMEOUT, --timeout TIMEOUT
                        Connection timeout in seconds (default: 0.01)
  --verbose             Enable verbose mode for detailed logs
  --output-csv OUTPUT_CSV
                        Path to output results in CSV format
  --show-all            Show all results, including closed ports
```

## Features

- Scan both IPv4 and IPv6 networks.
- Specify custom ports or scan a predefined list of common ports.
- Export scan results to CSV formats.
- Display detailed results, including IP addresses, hostnames, port statuses, and associated services.
- Option to show all results, including closed ports.
- Adjustable connection timeout for scans.
- Verbose mode for detailed logging.

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