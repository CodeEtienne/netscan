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

# Scan the common port list
netscan 192.168.1.0/24 --common-ports

# Export CSV
netscan 192.168.1.0/24 --common-ports --output-csv results.csv

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

`make test` is currently a placeholder because the repository does not yet contain a configured automated test suite.

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
```

See [README.md](README.md) for the full usage guide.
