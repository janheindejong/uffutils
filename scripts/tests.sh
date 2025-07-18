#!/usr/bin/bash

ruff check 
pytest 
mypy .\uffutils --follow-untyped-imports
