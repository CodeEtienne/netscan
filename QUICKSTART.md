# Netscan Quick Reference

## For End Users

### Installation
```bash
# Option 1: Standalone binary (no Python needed)
wget https://github.com/CodeEtienne/netscan/releases/download/v1.0.1/netscan
chmod +x netscan

# Option 2: Python package
pip install netscan
```

### Basic Usage
```bash
# Scan a network
netscan 192.168.1.0/24

# Scan specific ports
netscan 192.168.1.0/24 -p 80 443 22

# Scan common ports
netscan 192.168.1.0/24 --common-ports

# Export to CSV
netscan 192.168.1.0/24 --common-ports --output-csv results.csv
```

See [README.md](README.md) for full documentation.

---

## For Developers

### Setup
```bash
git clone https://github.com/CodeEtienne/netscan.git
cd netscan
make install-dev
source .venv/bin/activate
```

### Common Commands
```bash
make help          # Show all commands
make format        # Format code
make lint          # Check code quality
make build         # Build wheel package
make build-binary  # Build standalone binary
make clean         # Clean build files
```

### Project Structure
```
netscan/
├── __init__.py       # Version and metadata
├── __main__.py       # Module entry point
└── cli.py            # Main scanning logic

pyproject.toml       # Modern Python packaging
setup.py             # Legacy packaging (backward compatible)
Makefile             # Development automation
netscan.spec         # PyInstaller configuration
```

### Build & Release Workflow

1. **Local Testing**
   ```bash
   make build-binary
   ./dist/netscan --version
   ```

2. **Release**
   ```bash
   git tag v1.0.2
   git push origin v1.0.2
   # GitHub Actions automatically builds binaries for:
   # - Linux (x86_64)
   # - macOS (x86_64)  
   # - Windows (x86_64)
   ```

3. **Publish to PyPI**
   ```bash
   python -m build
   python -m twine upload dist/
   ```

### Testing Locally
```bash
# Test installed command
netscan 192.168.1.0/24 --help

# Test as module
python -m netscan --version

# Test scan
netscan 8.8.8.8 -p 53 80 443
```

---

## Configuration Files Overview

| File | Purpose |
|------|---------|
| `pyproject.toml` | Modern Python packaging metadata & tool config |
| `setup.py` | Legacy setup (kept for backward compatibility) |
| `Makefile` | Development task automation |
| `netscan.spec` | PyInstaller binary build configuration |
| `.github/workflows/build.yml` | CI/CD automation for releases |
| `requirements.txt` | Production dependencies |
| `requirements-dev.txt` | Development dependencies |
| `.editorconfig` | Editor configuration for consistency |
| `CONTRIBUTING.md` | Contribution guidelines |
| `CHANGELOG.md` | Version history and changes |

---

## Continuous Integration

Automated workflows trigger on:
- **Git tags** (`git tag v1.0.1`): Builds binaries for all platforms
- **Manual dispatch**: Via GitHub Actions workflow_dispatch

Artifacts automatically uploaded to GitHub Releases.

---

## Support

- **Documentation:** [README.md](README.md)
- **Contributing:** [CONTRIBUTING.md](CONTRIBUTING.md)
- **Issues:** GitHub Issues
- **Discussions:** GitHub Discussions
- **Email:** etienne.jannin@gmail.com
