# esnodePy

**esnodePy** is a zero-config Python tool that shows where your code’s assumptions break.

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
