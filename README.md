# Netscan: A Powerful and Lightweight Network Scanner

**A fast, efficient network scanner for discovering hosts and scanning ports with modern Python packaging.**

## About Netscan

Netscan is a simple yet powerful network scanner that allows you to scan a network range or a specific hostname for open ports. It provides detailed results, including IP addresses, hostnames, port statuses, and associated services. The tool is designed to be lightweight and easy to use, with options for scanning common ports, specifying custom ports, and exporting results to CSV. It supports both IPv4 and IPv6 scanning.

### Features

- 🚀 **Fast scanning** - Multi-threaded port scanning with configurable concurrency
- 📊 **Flexible output** - Display results in the terminal or export to CSV
- 🔍 **Smart detection** - ICMP ping-based host discovery or TCP port scanning
- 🌐 **IPv4 & IPv6 support** - Works with both address families
- 🎨 **Rich formatting** - Beautiful, color-coded terminal output
- 🔧 **Customizable** - Adjust timeout, ports, and scanning behavior
- 📦 **Easy distribution** - Standalone binary or Python package

## Installation

### Option 1: Standalone Binary (Recommended for End Users)

Download the latest binary for your platform from [Releases](https://github.com/CodeEtienne/netscan/releases):

```bash
# Linux
wget https://github.com/CodeEtienne/netscan/releases/download/v1.0.1/netscan
chmod +x netscan
./netscan --help

# macOS / Windows
# Download from Releases and run directly
```

**Advantages:**
- No Python installation required
- Works out of the box
- Easy to distribute to non-technical users

### Option 2: Python Package via pip (Recommended for Developers)

```bash
# Install from PyPI (when published)
pip install netscan

# Or install from local wheel
pip install dist/netscan-1.0.1-py3-none-any.whl

# Or use pipx for isolated environment
pipx install netscan
```

### Option 3: Development Installation

```bash
git clone https://github.com/CodeEtienne/netscan.git
cd netscan
make install-dev
source .venv/bin/activate
```

## Quick Start

```bash
# Scan a single host
netscan 192.168.1.1

# Scan a network range
netscan 192.168.1.0/24

# Scan specific ports
netscan 192.168.1.0/24 -p 80 443 22

# Scan common ports (FTP, SSH, HTTP, HTTPS, etc.)
netscan 192.168.1.0/24 --common-ports

# Scan with custom timeout
netscan 192.168.1.0/24 --common-ports -t 1.0

# Export results to CSV
netscan 192.168.1.0/24 --common-ports --output-csv results.csv

# Scan by hostname
netscan example.com

# Verbose output
netscan 192.168.1.0/24 --verbose

# Show all ports (including closed ones)
netscan 192.168.1.0/24 -p 22 80 443 --show-all
```

## Usage Reference

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
  --common-ports        Scan a list of common ports (21, 22, 53, 80, 443, 3306, 5432, etc.)
  -t TIMEOUT, --timeout TIMEOUT
                        Connection timeout in seconds (default: 0.5)
  --verbose             Enable verbose mode for detailed logs
  --output-csv OUTPUT_CSV
                        Path to output results in CSV format
  --show-all            Show all results, including closed ports
  -v, --version         Show the version of the netscan tool and exit
```

## Building from Source

### Prerequisites

- Python 3.8+
- `pip` and `build`
- `PyInstaller` (for standalone binary)

### Quick Build

```bash
# 1. Set up development environment (one-time)
make install-dev
source .venv/bin/activate

# 2. View all available commands
make help

# 3. Build your distribution
make build              # Build wheel distribution
make build-binary       # Build standalone binary
make dist               # Build both wheel and binary
```

**Important:** You must run steps 1-2 once before building. After that, always activate the virtual environment:
```bash
source .venv/bin/activate
```

### Detailed Build Steps

#### Setup (Required Once)

```bash
# Create virtual environment and install dependencies
make install-dev

# Activate the virtual environment
source .venv/bin/activate

# After activation, you should see (.venv) in your shell prompt
```

#### 1. Build Python Wheel (Recommended)

```bash
# Ensure virtual environment is activated
source .venv/bin/activate

# Build
make build
# Or manually: python -m build --wheel

# Output: dist/netscan-1.0.1-py3-none-any.whl
```

**Advantages:**
- Lightweight (~50-100 KB)
- Works on any system with Python 3.8+
- Standard Python distribution format

#### 2. Build Standalone Binary (Recommended for End Users)

```bash
# Ensure virtual environment is activated
source .venv/bin/activate

# Build binary using the Makefile (all dependencies already installed)
make build-binary
# Or manually: python -m PyInstaller netscan.spec

# Output: dist/netscan (executable binary, ~12 MB)
```

**Advantages:**
- Single executable file
- No Python interpreter needed
- Easy to distribute
- Works on systems without Python

**Note:** Standalone binaries are larger (~100-200 MB depending on OS) due to bundled Python runtime.

#### 3. Install & Test

```bash
# Test the built binary directly
./dist/netscan --help
./dist/netscan --version

# Option A: Install binary system-wide
sudo cp dist/netscan /usr/local/bin/netscan
sudo chmod +x /usr/local/bin/netscan
netscan --help

# Option B: Install wheel package (if built)
pip install dist/netscan-1.0.1-py3-none-any.whl

# Option C: Install in development mode
pip install -e .
```

## Development Workflow

### Setup Development Environment

```bash
make install-dev
source .venv/bin/activate
```

### Available Commands

```bash
make lint              # Run code linting
make format            # Auto-format code
make test              # Run tests (if configured)
make clean             # Remove build artifacts
make clean-all         # Remove everything including venv
```

### Code Style

This project uses:
- **black** for code formatting
- **isort** for import sorting
- **flake8** for linting
- **mypy** for type checking (optional)

### Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make your changes and run: `make format && make lint`
4. Commit and push to your fork
5. Submit a pull request

## Continuous Integration

Builds are automatically triggered on git tags (e.g., `git tag v1.0.1`) via GitHub Actions. This builds binaries for:
- Linux (x86_64)
- macOS (x86_64)
- Windows (x86_64)

Artifacts are automatically uploaded to GitHub Releases.

## Distribution

### Publish to PyPI

```bash
# Build distributions
python -m build

# Upload to PyPI (requires credentials)
python -m twine upload dist/
```

### Create GitHub Release

```bash
# Tag the release
git tag v1.0.1
git push origin v1.0.1

# GitHub Actions automatically builds and releases binaries
```

## Troubleshooting

### "Permission denied" when running binary

```bash
chmod +x ./netscan
```

### "Module not found" error

Ensure all dependencies are installed:
```bash
pip install -r requirements.txt
```

Or in development:
```bash
make install-dev
```

### Build fails with PyInstaller

Make sure you have all dependencies installed:
```bash
pip install -e .
pip install pyinstaller
```

## Architecture

### Project Structure

```
netscan/
├── __init__.py           # Version and metadata
├── __main__.py           # Module entry point
└── cli.py                # Main CLI and scanning logic

Configuration Files:
├── pyproject.toml        # Modern Python packaging config
├── setup.py              # Legacy setup (still supported)
├── Makefile              # Development automation
├── netscan.spec          # PyInstaller configuration
└── .github/workflows/    # CI/CD automation
```

### How It Works

1. **Network Scanning:** Parses CIDR notation or resolves hostnames
2. **Host Discovery:** Uses ICMP ping or TCP handshake to find live hosts
3. **Port Scanning:** Multi-threaded TCP connection attempts on specified ports
4. **Output:** Displays results in formatted tables or CSV export

## Performance Tips

- **Fast scanning:** Use `-t 0.1` for aggressive scans on LAN (requires root/admin)
- **Large networks:** Reduce timeout with `-t 0.2` to complete scans faster
- **Specific ports:** Scanning fewer ports significantly speeds up the scan
- **Common ports:** Use `--common-ports` instead of scanning all 65535 ports

## Limitations

- Requires root/admin privileges for certain scan types
- IPv6 scanning may have limitations depending on network configuration
- Reverse DNS lookups can slow down scanning

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## Support

- **Issues:** [GitHub Issues](https://github.com/CodeEtienne/netscan/issues)
- **Discussions:** [GitHub Discussions](https://github.com/CodeEtienne/netscan/discussions)
- **Email:** etienne.jannin@gmail.com