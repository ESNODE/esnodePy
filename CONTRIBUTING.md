# Contributing to esnodePy

First off, thanks for taking the time to contribute! ❤️

All types of contributions are encouraged and valued. See the [Table of Contents](#table-of-contents) for different ways to help and details about how this project handles them.

## Table of Contents

- [I Have a Question](#i-have-a-question)
- [I Want To Contribute](#i-want-to-contribute)
  - [Reporting Bugs](#reporting-bugs)
  - [Suggesting Enhancements](#suggesting-enhancements)
  - [Your First Code Contribution](#your-first-code-contribution)
- [Development Setup](#development-setup)
- [Style Guide](#style-guide)

## I Have a Question

If you want to ask a question, we assume that you have read the available [Documentation](https://github.com/ESNODE/esnodePy#readme).

## I Want To Contribute

### Reporting Bugs

This section guides you through submitting a bug report for esnodePy. Following these guidelines helps maintainers and the community understand your report, reproduce the behavior, and find related reports.

*   **Use the Bug Report template** in the issue tracker.
*   **Provide a reproduction** (a small script that demonstrates the issue).

### Suggesting Enhancements

This section guides you through submitting an enhancement suggestion for esnodePy, including completely new features and minor improvements to existing functionality.

*   **Use the Feature Request template** in the issue tracker.

### Your First Code Contribution

1.  Fork the repo and create your branch from `main`.
2.  Install development dependencies.
3.  Make sure your code lints and tests pass.

## Development Setup

1.  **Clone your fork**:
    ```bash
    git clone https://github.com/your-username/esnodePy.git
    cd esnodePy
    ```

2.  **Install in editable mode with dev dependencies**:
    ```bash
    pip install -e ".[dev]"
    ```

3.  **Run Tests**:
    ```bash
    pytest tests/
    ```

4.  **Run Type Checking**:
    ```bash
    mypy esnodepy tests
    ```

## Style Guide

We adhere to strict Python standards:
*   **Formatting**: Use `black` for code formatting.
*   **Imports**: Use `isort` for import sorting.
*   **Typing**: All code must be fully typed and pass `mypy --strict`.

Running the formatters:
```bash
isort .
black .
```
