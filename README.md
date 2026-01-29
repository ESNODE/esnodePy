<p align="center">
  <img src="assets/logo.png" alt="esnodePy Logo" width="300">
</p>

# esnodePy

**Zero-config Python boundary intelligence.**

`esnodePy` is a developer tool that scans your Python codebase to detect **Assumption Drift**—places where your type hints (what you claim) and your function logic (what actually happens) disagree.

It surfaces:
- Type drift
- Import boundary risks
- Mock vs reality mismatches
- Change impact across boundaries

Without configuration, strictness, or rewrites.

## Install
```bash
pip install esnodePy
```

## Usage
```bash
esnodepy scan
esnodepy imports
esnodepy runtime
esnodepy diff
```
CLI examples (local, remote, structured output):

```bash
# Scan current directory (human readable)
esnodepy scan

# Scan a specific local path
esnodepy scan /path/to/project

# Scan a remote git repo (auto-cloned to temp dir)
esnodepy scan https://github.com/ESNODE/esnodePy.git

# Produce structured JSON output
esnodepy scan --output report.json

# Combine remote + JSON
esnodepy scan https://github.com/ESNODE/esnodePy.git --output remote_report.json
```

CI badge and quick consumption

[![CI](https://github.com/ESNODE/esnodePy/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/ESNODE/esnodePy/actions)

After the CI job emits `esnode_report.json` you can assert failures in shell using `jq`:

```bash
# Exit non-zero if any drift found
if [ $(jq '.drift_count' esnode_report.json) -gt 0 ]; then
  echo "Assumption drift detected"; exit 1;
fi
```

## Philosophy

Python doesn’t fail loudly — it fails silently at boundaries.

esnodePy makes those boundaries visible.
