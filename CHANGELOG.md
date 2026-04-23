# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Documentation cleanup to match the current repository layout and behavior
- `--workers` CLI option for scan concurrency control
- Richer `--port` parsing for comma-separated lists and ranges
- `--json` CLI output mode
- Pytest coverage for new CLI parsing and output behavior

### Changed
- Removed unused `netifaces` dependency and stale PyInstaller hidden import
- Fixed CLI help text for the timeout option and normalized the displayed program name
- `make test` now runs the test suite instead of printing a placeholder

## [1.0.1] - 2025-01-XX

### Added
- CSV export functionality
- Verbose logging mode
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
