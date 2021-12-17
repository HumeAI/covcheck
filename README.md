# covcheck

Command-line tool for code coverage validation.

`covcheck` is intented to be used in conjunction with [coverage.py](https://coverage.readthedocs.io/), which already has support for `pytest`, `unittest`, and `nosetest`. All you have to do is point `covcheck` to the `coverage.xml` file produced when running your tests.

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
$ covcheck coverage.xml --line 96 --branch --84
```
