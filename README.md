# Netscan

Lightweight network and port scanner with terminal output and optional CSV export.

## What It Does

- Scans a CIDR range or a single hostname/IP
- Uses ICMP ping for host discovery when no ports are specified
- Uses TCP connect scans when ports are specified
- Resolves reverse DNS hostnames for scanned IPs when available
- Prints results with `rich`
- Supports explicit worker concurrency control with `--workers`
- Accepts port lists and ranges like `80,443,8000-8010`
- Supports JSON output with `--json`
- Exports results to CSV with `--output-csv`

## Current Scope

- Python package with a `netscan` console script
- Module entry point via `python -m netscan`
- Local build support for wheels and a PyInstaller binary
- Pytest-based CLI tests for parsing and output behavior
- No CI workflow is present in this repository

## Installation

### Install From Source

```bash
git clone https://github.com/CodeEtienne/netscan.git
cd netscan
python3 -m pip install -e .
```

### Development Setup

```bash
git clone https://github.com/CodeEtienne/netscan.git
cd netscan
make install-dev
source .venv/bin/activate
```

## Quick Start

```bash
# Scan a single host with ping discovery
netscan 192.168.1.10

# Scan a network range with ping discovery
netscan 192.168.1.0/24

# Scan specific TCP ports
netscan 192.168.1.10 -p 22 80 443

# Scan port lists and ranges
netscan 192.168.1.10 -p 22,80,443,8000-8010

# Scan the built-in common port list
netscan 192.168.1.0/24 --common-ports

# Increase connection timeout
netscan 192.168.1.0/24 --common-ports -t 1.0

# Export results to CSV
netscan 192.168.1.0/24 --common-ports --output-csv results.csv

# Scan a hostname
netscan example.com -p 80 443

# Show closed ports too
netscan 192.168.1.10 -p 22 80 443 --show-all

# Enable debug logging
netscan 192.168.1.0/24 --verbose

# Use fewer or more concurrent workers
netscan 192.168.1.0/24 --common-ports --workers 32

# Emit JSON instead of table output
netscan 192.168.1.10 -p 22,80,443 --json
```

## Usage

```text
usage: netscan [-h] [-v] [-p [PORT ...]] [--common-ports] [-t TIMEOUT]
               [--verbose] [--output-csv OUTPUT_CSV] [--show-all] [--workers WORKERS]
               [--json]
               network
```

Arguments:

- `network`: CIDR range or hostname/IP to scan
- `-p`, `--port`: TCP ports to scan, including comma-separated lists and ranges
- `--common-ports`: scan the built-in common port list
- `-t`, `--timeout`: connection timeout in seconds
- `--verbose`: enable debug logging
- `--output-csv`: write results to a CSV file
- `--show-all`: include closed ports in the table output
- `--workers`: maximum number of concurrent host scan workers
- `--json`: print JSON instead of the rich table
- `-v`, `--version`: print the version

## How Scanning Works

1. Host input is validated as a CIDR range or resolved from a hostname to a single IPv4 address.
2. If no ports are specified, Netscan runs ping-based host discovery.
3. If ports are specified, Netscan attempts TCP connections to each host/port pair.
4. Reverse DNS lookups are attempted for each scanned IP.
5. Results are displayed in a table and can also be exported to CSV.

## Build Commands

```bash
make help
make build
make build-binary
make dist
```

Notes:

- `make build` builds a wheel
- `make build-binary` builds a standalone binary with PyInstaller
- `make dist` builds both artifacts

## Development Commands

```bash
make format
make lint
make test
make clean
make clean-all
```

`make test` runs the pytest suite in `tests/`.

## Project Structure

```text
netscan/
├── __init__.py
├── __main__.py
└── cli.py

CHANGELOG.md
CONTRIBUTING.md
LICENSE
Makefile
QUICKSTART.md
netscan.spec
pyproject.toml
requirements-dev.txt
requirements.txt
README.md
tests/
```

## Limitations

- Ping-based discovery depends on the system `ping` command being available
- Hostname input is resolved with `socket.gethostbyname`, so hostname scanning is currently IPv4-only
- Reverse DNS lookups can slow down large scans
- Some network environments may block ICMP or TCP probes

## License

MIT. See [LICENSE](LICENSE).
