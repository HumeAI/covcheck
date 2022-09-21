---
hide:
  - navigation
---

# Covcheck Docs

`covcheck` is a command-line tool for code coverage validation.

`covcheck` is intended to be used in conjunction with [coverage.py](https://coverage.readthedocs.io/), which already has support for `pytest`, `unittest`, and `nosetest`. All you have to do is point `covcheck` to the `coverage.xml` file produced when running your tests.

## Requirements

Python versions 3.7, 3.8, and 3.9 are supported

## Installation

```bash
$ pip install coverage
$ pip install covcheck
```

## Usage

### 1. Produce a `coverage.xml` file while running your tests:

```bash
# pytest
$ coverage run --branch -m pytest ...
$ coverage xml

# unittest
$ coverage run --branch -m unittest ...
$ coverage xml

# nosetest
$ coverage run --branch -m nose ...
$ coverage xml
```

### 2. Validate that line and branch coverage meet the provided thresholds:

```bash
$ covcheck coverage.xml --line 96 --branch 84
```

## Configuration

### Basic configuration

Arguments passed through the command-line can also be configured with a pyproject.toml file.

```toml
# pyproject.toml

[tool.covcheck]
line = 92.0
branch = 79.0
```

```bash
$ covcheck coverage.xml --config pyproject.toml
```

### Coverage groups

Define groups in a pyproject.toml file to configure coverage requirements for multiple sets of tests.

```toml
# pyproject.toml

[tool.covcheck.group.unit.coverage]
line = 92.0
branch = 79.0

[tool.covcheck.group.service.coverage]
line = 53.0
branch = 45.0
```

```bash
$ covcheck coverage.xml --config pyproject.toml --group unit
```
