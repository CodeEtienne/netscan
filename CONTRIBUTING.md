# Contributing to Netscan

Thank you for your interest in contributing to Netscan! We welcome contributions from the community.

## Development Setup

### Prerequisites

- Python 3.8+
- Git

### Getting Started

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/yourusername/netscan.git
   cd netscan
   ```

2. **Set up development environment**
   ```bash
   make install-dev
   source .venv/bin/activate
   ```

3. **Verify setup**
   ```bash
   netscan --version
   ```

## Development Workflow

### Code Style

We use automatic code formatting tools. Before committing:

```bash
make format    # Auto-format code with black and isort
make lint      # Check for issues with flake8
```

### Testing

Run tests with:
```bash
make test      # Placeholder until automated tests are added
```

### Building

Test your changes by building the package:

```bash
make build         # Build wheel distribution
make build-binary  # Build standalone binary
```

## Making Changes

1. **Create a feature branch**
   ```bash
   git checkout -b feature/my-feature
   ```

2. **Make your changes** and keep commits focused

3. **Format and lint your code**
   ```bash
   make format
   make lint
   ```

4. **Commit with clear messages**
   ```bash
   git commit -m "feat: add new feature"
   git commit -m "fix: resolve issue #123"
   git commit -m "docs: update README"
   ```

5. **Push to your fork**
   ```bash
   git push origin feature/my-feature
   ```

6. **Submit a Pull Request**
   - Describe what your PR does
   - Reference any related issues
   - Include test cases if applicable

## Commit Message Format

Use conventional commits for clarity:

- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `style:` - Code formatting (no logic changes)
- `refactor:` - Code refactoring
- `perf:` - Performance improvements
- `test:` - Adding/updating tests
- `chore:` - Maintenance tasks

Example: `feat: add IPv6 support for network scanning`

## Pull Request Guidelines

- Keep PRs focused on a single feature or fix
- Include tests for new functionality when a test harness is added
- Update documentation as needed
- Ensure formatting, linting, and builds pass
- Respond to review feedback promptly

## Code Quality

- **Python 3.8+ compatibility** - Ensure code works on Python 3.8 and later
- **Type hints** - Encourage type hints for new code
- **Documentation** - Add docstrings to functions and modules
- **Tests** - Add tests alongside new features once the test suite is in place

## Reporting Issues

When reporting bugs:

1. **Check existing issues** - Avoid duplicates
2. **Provide details:**
   - What version of Netscan are you using?
   - What OS and Python version?
   - What command were you running?
   - What error did you get?
3. **Include reproduction steps**
4. **Attach error logs** if applicable

## License

By contributing, you agree your work will be licensed under the MIT License.

## Questions?

Feel free to:
- Open an issue labeled `question`
- Email: etienne.jannin@gmail.com
