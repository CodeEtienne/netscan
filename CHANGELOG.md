# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Modern Python packaging with `pyproject.toml`
- Standalone binary builds with PyInstaller
- GitHub Actions CI/CD for automated building
- Makefile for development automation
- Development tools configuration (black, isort, flake8, mypy)
- Module entry point (`__main__.py`)
- Comprehensive documentation

### Changed
- Updated README with modern installation and usage instructions
- Improved project structure and documentation

### Deprecated
- Legacy `setup.py` approach (still supported for backward compatibility)

## [1.0.1] - 2025-01-XX

### Added
- CSV export functionality
- Verbose logging mode
- IPv6 support
- Hostname resolution for scanned IPs
- Common ports scanning feature
- Connection timeout configuration

### Fixed
- Timeout handling for network scanning
- Port validation (1-65535 range)
- Hostname vs. CIDR network argument parsing

## [1.0.0] - 2025-01-XX

### Added
- Initial release
- Network scanning with CIDR notation support
- TCP port scanning on specified hosts
- ICMP ping-based host discovery
- Rich terminal output with color formatting
- CSV export capability
- Cross-platform support (Linux, macOS, Windows)

[Unreleased]: https://github.com/CodeEtienne/netscan/compare/v1.0.1...HEAD
[1.0.1]: https://github.com/CodeEtienne/netscan/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/CodeEtienne/netscan/releases/tag/v1.0.0
