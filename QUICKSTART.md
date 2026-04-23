# Netscan Quick Reference

## Install

```bash
git clone https://github.com/CodeEtienne/netscan.git
cd netscan
python3 -m pip install -e .
```

For development:

```bash
make install-dev
source .venv/bin/activate
```

## Common Commands

```bash
# Ping-based host discovery
netscan 192.168.1.0/24

# Scan specific ports
netscan 192.168.1.10 -p 22 80 443

# Scan port lists and ranges
netscan 192.168.1.10 -p 22,80,443,8000-8010

# Scan the common port list
netscan 192.168.1.0/24 --common-ports

# Export CSV
netscan 192.168.1.0/24 --common-ports --output-csv results.csv

# Control concurrency
netscan 192.168.1.0/24 --common-ports --workers 32

# Emit JSON
netscan 192.168.1.10 -p 22,80 --json

# Run as a module
python3 -m netscan --version
```

## Build

```bash
make build
make build-binary
make dist
```

## Development

```bash
make format
make lint
make test
```

`make test` runs the pytest suite in `tests/`.

## Project Files

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

See [README.md](README.md) for the full usage guide.
