# UFFUtils

A Python-based command-line tool for manipulating UFF datasets.

[![PyPI version](https://badge.fury.io/py/uffutils.svg)](https://pypi.org/project/uffutils/)
[![PyPi status](https://img.shields.io/pypi/status/uffutils)](https://pypi.org/project/uffutils/)
![Release date](https://img.shields.io/github/release-date-pre/janheindejong/uffutils)
![Python Package CI](https://github.com/janheindejong/uffutils/actions/workflows/python-package.yml/badge.svg?branch=main)
![Monthly downloads](https://img.shields.io/pypi/dm/uffutils)
![License](https://img.shields.io/pypi/l/uffutils)
![Python versions](https://img.shields.io/pypi/pyversions/uffutils)

## Introduction

UFFUtils lets you inspect and manipulate UFF files. Let's look at an example.

Say you have some dataset - `my_data.uff` - that you want to reduce in size (e.g., by only taking every 1000th node), scale from mm to m, rotate around the y-axis by 90 degrees. With UFFUtils, you would do this in the following way:

```powershell
uffutils subset my_data.uff --step 1000 `
uffutils scale --length 0.001 `
uffutils rotate - rotated.uff --angles 0 90 0
```

Congratulations! You now have a reduced, scaled and rotated version of your dataset!

For more functionality, see the description of each command below.

## Installing

A good way to run UFF utils is through [`uv`](https://docs.astral.sh/uv/getting-started/installation/). Once you have installed `uv`, you can run `uffutils` like so:

```powershell
uvx uffutils
```

No need for any additional software (e.g., Python); `uv` handles it for you.

## Usage

### The `inspect` command

The `inspect` command allows you to view the contents of a UFF file. Example usage:

```powershell
uffutils inspect my_file.uff  # Print nice overview 
uffutils inspect my_file.uff --nodes # Print full list of nodes
```

### The `subset` command

Allows you to create file with a subset of nodes, which is particularly useful if you want to downsize a UFF file. Usage:

```powershell
uffutils subset input.uff output.uff --ids "1,2,3"  # Only takes nodes 1, 2 and 3
uffutils subset input.uff output.uff --step 1000  # Takes every 1000th node, starting at 1 
uffutils subset input.uff output.uff --max 100 # Takes the first 100 nodes 
```

Operations can be combined. The following operation yields a file with nodes 10 and 30.

```powershell
uffutils subset input.uff output.uff --selection "10,20,30,40,50" --step 2 --max 2
```

### The `scale` command  

You can scale length:

```powershell
uffutils scale input.uff output.uff --length 1000 
```

### The `translate` command

You can translate the data:

```powershell
uffutils translate input.uff output.uff --xyz 10.0 20.0 30.0 
```

### The `rotate` command

You can rotate the data:

```powershell
uffutils rotate input.uff output.uff --angles 90 90 90
```

### Combining commands

You can combine commands through piping, like so:

```powershell
uffutils subset input.uff --step 100 | `
    uffutils scale --length 1000 | `
    uffutils translate --xyz 10 20 30 | `
    uffutils rotate - output.uff --angles 90 0 0 
```
