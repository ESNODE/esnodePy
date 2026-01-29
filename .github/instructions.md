# esnodePy Developer Guide

## Project Overview

**esnodePy** is a boundary intelligence tool that detects **Assumption Drift**—misalignment between declared type hints and actual runtime behavior in Python codebases. Think of it as a zero-config linter that surfaces silent failures at function boundaries.

**Core philosophy**: Python fails silently at boundaries; esnodePy makes boundaries visible.

## Architecture

### Four-Module Pattern

1. **Engine** (`esnodepy/engine/`) - Core analysis logic
   - `boundaries.py`: `FunctionBoundary` class models declared vs. observed behavior
   - `graph.py`: `BoundaryGraph` for cross-component relationships
   - `report.py`: Output formatting for drift findings

2. **Scanners** (`esnodepy/scanners/`) - CLI-driven analysis strategies
   - `scan.py`: AST-based return type drift detection (primary scanner)
   - `imports.py`: External import boundary risk analysis
   - `runtime.py`: Placeholder for pytest plugin observation (opt-in)
   - `diff.py`: Placeholder for change impact analysis across revisions

   **New features**:
   - CLI `target` positional argument supports local paths and `http/https` git URLs. Remote repos are auto-cloned into a temp dir.
   - `--output / -o` writes structured JSON; see the JSON schema at `.github/esnode_report.schema.json`.
   - `runtime` remains local-only for security (remote URLs are rejected).

3. **CLI** (`cli.py`) - Entry point; delegates to scanner modules via `run()` functions

### Data Flow

```
cli.py (subcommand router)
  └─> scanners/{scan,imports,runtime,diff}.py
       └─> engine/boundaries.py (FunctionBoundary model)
       └─> engine/report.py (formatting)
```

## Key Patterns

### Drift Definition (v0.2)
```python
# In boundaries.py:has_drift()
# Drift = declared return type exists AND is not None, 
# BUT we observe None (explicit or implicit)
```
Type mismatches (e.g., `int` declared but `str` observed) are **NOT** drift yet. This is intentional—drift focuses on the most critical: unhandled None returns.

### Scanner Module Convention
Every scanner exposes `run(target_dir: str = ".")` function called from CLI:
- `scan.py:run()` walks AST tree, extracts return types, detects drift
- `imports.py:run()` lists external imports (risky boundaries)
- `runtime.py:run()` and `diff.py:run()` currently placeholder stubs

### AST-Based Analysis
`scan.py` uses Python's `ast` module to:
1. Parse source code safely
2. Extract function signatures and return statements
3. Infer return value shapes via `infer_return_value()`—handles Constants, Names, Calls, Attributes

## Development Conventions

### Testing
- Use pytest; test files mirror source structure: `tests/engine/`, `tests/scanners/`
- Example: [test_boundaries.py](tests/engine/test_boundaries.py) tests drift logic directly
- Drift test: `fb.observe_return("None (implicit)"); assert fb.has_drift()`

### Code Style
- **Strict mypy**: `pyproject.toml` enforces `strict = true`
- **Imports**: isort (profile=black) + black formatter
- **No external dependencies**: Project is zero-config by design; stdlib only

### Error Handling
- Logging at ERROR level (configured in each scanner); non-blocking for robustness
- Failed parses logged but don't halt traversal: `except (OSError, SyntaxError, UnicodeDecodeError)`

## When Adding Features

1. **New scanner**: Add `run(target_dir: str = ".")` to `esnodepy/scanners/`, wire into `cli.py`
2. **Boundary logic**: Extend `FunctionBoundary` class or drift model in `boundaries.py`
3. **Graph analysis**: Use `BoundaryGraph` for multi-function relationships
4. **Reporting**: Format output with `report.py` utilities (`print_header()`)

## Testing Commands

```bash
pytest                    # Run all tests
pytest tests/             # Test a directory
pytest -v                 # Verbose
pytest --cov             # Coverage report (installed in [dev])
```

Example: produce machine-readable scan in CI

```bash
esnodepy scan https://github.com/ESNODE/esnodePy.git --output report.json
```

CI: A sample GitHub Actions workflow is provided at `.github/workflows/ci.yml` which installs dev deps, runs `pytest`, `mypy`, and emits `esnode_report.json` as an artifact.

Validator: A lightweight report validator was added at `esnodepy/engine/validation.py`. The CLI validates `scan` output prior to writing JSON; CI also runs the same validator to ensure schema integrity.

Coverage: CI now runs `pytest --cov` and uploads `coverage.xml` as an artifact.

## Known Limitations

- **Runtime observation** (--runtime): Not implemented; awaiting pytest plugin design
- **Diff analysis** (--diff): Placeholder; needs git integration
- **Type variance**: Current drift model is conservative (None-only); future versions expand to type mismatches
