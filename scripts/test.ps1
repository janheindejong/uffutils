$ErrorActionPreference = "Stop"

ruff format --check
ruff check 
pytest 
mypy uffutils --follow-untyped-imports