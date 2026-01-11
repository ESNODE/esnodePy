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

## Philosophy

Python doesn’t fail loudly — it fails silently at boundaries.

esnodePy makes those boundaries visible.
