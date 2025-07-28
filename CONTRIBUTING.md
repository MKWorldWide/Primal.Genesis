# Contributing to Primal Genesis Engine

Welcome to the Primal Genesis Engine project! We're excited to have you contribute. This document will guide you through the process of setting up your development environment and making contributions.

## Table of Contents
- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Fork and Clone](#fork-and-clone)
  - [Environment Setup](#environment-setup)
- [Development Workflow](#development-workflow)
  - [Branch Naming](#branch-naming)
  - [Making Changes](#making-changes)
  - [Testing](#testing)
  - [Code Style](#code-style)
  - [Documentation](#documentation)
- [Submitting Changes](#submitting-changes)
  - [Pull Requests](#pull-requests)
  - [Code Review](#code-review)
  - [Merging](#merging)
- [Reporting Issues](#reporting-issues)
- [Asking Questions](#asking-questions)

## Code of Conduct

This project adheres to the [Contributor Covenant Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## Getting Started

### Prerequisites

- Python 3.9+
- Git
- [Poetry](https://python-poetry.org/) (recommended) or pip
- [Docker](https://www.docker.com/) (optional, for containerized development)

### Fork and Clone

1. Fork the repository on GitHub
2. Clone your fork locally:
   ```bash
   git clone git@github.com:YOUR_USERNAME/Primal-Genesis-Engine-Sovereign.git
   cd Primal-Genesis-Engine-Sovereign
   ```
3. Add the upstream repository:
   ```bash
   git remote add upstream git@github.com:MKWorldWide/Primal-Genesis-Engine-Sovereign.git
   ```

### Environment Setup

#### Using Poetry (Recommended)

1. Install Poetry (if not already installed):
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

2. Install dependencies:
   ```bash
   poetry install
   ```

3. Activate the virtual environment:
   ```bash
   poetry shell
   ```

#### Using pip

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-test.txt
   ```

## Development Workflow

### Branch Naming

Branches should be named using the following format:

```
<type>/<description>-<issue-number>
```

Where `<type>` is one of:
- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code changes that neither fix bugs nor add features
- `perf`: Performance improvements
- `test`: Adding or modifying tests
- `chore`: Maintenance tasks

Example: `feat/quantum-sync-42`

### Making Changes

1. Update your local repository:
   ```bash
   git fetch upstream
   git checkout main
   git merge upstream/main
   ```

2. Create a new branch for your changes:
   ```bash
   git checkout -b type/description-issue
   ```

3. Make your changes following the code style guidelines.

4. Run tests to ensure everything works:
   ```bash
   make test
   ```

5. Commit your changes with a descriptive message:
   ```bash
   git commit -m "type(scope): brief description of changes"
   ```

### Testing

Run the full test suite:
```bash
make test
```

Run specific tests:
```bash
pytest tests/path/to/test_file.py::test_function_name -v
```

Check code coverage:
```bash
pytest --cov=athenamist_integration tests/
```

### Code Style

We use:
- **Black** for code formatting
- **isort** for import sorting
- **flake8** for linting
- **mypy** for type checking

To automatically format and check your code:
```bash
make format
make lint
make type-check
```

### Documentation

- Update relevant documentation when making changes
- Add docstrings to new functions and classes following [Google style](https://google.github.io/styleguide/pyguide.html#381-docstrings)
- Update the README.md if your changes affect setup or usage

## Submitting Changes

### Pull Requests

1. Push your changes to your fork:
   ```bash
   git push origin your-branch-name
   ```

2. Open a Pull Request (PR) on GitHub from your fork to the main repository's `main` branch.

3. Fill out the PR template with details about your changes.

### Code Review

- All PRs require at least one approval from a maintainer
- Address all review comments and CI failures
- Keep your PR focused on a single change

### Merging

- Squash and merge PRs after approval
- Delete the branch after merging

## Reporting Issues

If you find a bug or have a feature request, please open an issue on GitHub with:

1. A clear title and description
2. Steps to reproduce (for bugs)
3. Expected vs. actual behavior
4. Environment details
5. Screenshots or logs if applicable

## Asking Questions

For questions about the project:

- Check the [documentation](README.md)
- Search existing issues
- If you can't find an answer, open a discussion or ask in the project's community space

---

Thank you for contributing to Primal Genesis Engine! Your contributions help make this project better for everyone.
