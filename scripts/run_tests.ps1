$ErrorActionPreference = "Stop"

Set-Location (Join-Path $PSScriptRoot "..")
if (Get-Command uv -ErrorAction SilentlyContinue) {
    uv run python -m unittest discover -s tests -p "test_*.py" -v
} else {
    python -m unittest discover -s tests -p "test_*.py" -v
}
