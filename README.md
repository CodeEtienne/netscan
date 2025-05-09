# Netscan: A Powerful and Lightweight Network Scanner

This guide explains how to build, install, and use the `netscan` package.

## About Netscan

Netscan is a simple network scanner that allows you to scan a network range or a specific hostname for open ports. It provides detailed results, including IP addresses, hostnames, port statuses, and associated services. The tool is designed to be lightweight and easy to use, with options for scanning common ports, specifying custom ports, and exporting results to CSV. It supports both IPv4 and IPv6 scanning.

## Command-Line Help

```
usage: netscan [-h] [-p [PORT [PORT ...]]] [--common-ports] [-t TIMEOUT]
               [--verbose] [--output-csv OUTPUT_CSV] [--show-all] [-v]
               network

Simple network scanner

positional arguments:
  network               CIDR network range to scan (e.g., 192.168.1.0/24) or a simple hostname

optional arguments:
  -h, --help            show this help message and exit
  -p [PORT [PORT ...]], --port [PORT [PORT ...]]
                        TCP port(s) to scan (e.g., -p 80 443)
  --common-ports        Scan a list of common ports (e.g., FTP, SSH, HTTP, etc.). Common ports include: 21 (FTP), 22 (SSH), 23 (Telnet), 25 (SMTP), 53 (DNS), 80 (HTTP), 110 (POP3), 139 (NetBIOS), 143 (IMAP), 443 (HTTPS), 445 (SMB), 3389 (RDP), 3306 (MySQL), 5432 (PostgreSQL), 5900 (VNC), 8000 (Dev Server), 8080 (HTTP-Alt), 8443 (HTTPS-Alt), 8888 (Jupyter), 9200 (Elasticsearch), 6379 (Redis), 27017 (MongoDB), 25565 (Minecraft Server).
  -t TIMEOUT, --timeout TIMEOUT
                        Connection timeout in seconds (default: 0.5)
  --verbose             Enable verbose mode for detailed logs
  --output-csv OUTPUT_CSV
                        Path to output results in CSV format
  --show-all            Show all results, including closed ports
  -v, --version         Show the version of the netscan tool and exit
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

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/netscan.git
   ```

2. **Navigate to the Project Directory**
   ```bash
   cd netscan
   ```

3. **Clean Previous Builds**
   ```bash
   rm -rf build dist *.egg-info
   ```

4. **Build the Package**
   ```bash
   python3 setup.py sdist bdist_wheel
   ```

   This will generate the `.whl` file in the `dist/` directory.

5. **Verify the Build**
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

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.