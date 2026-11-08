@echo off
setlocal
cd /d "%~dp0.."
where uv >nul 2>nul
if not errorlevel 1 (
    uv run python -m unittest discover -s tests -p "test_*.py" -v
) else (
    python -m unittest discover -s tests -p "test_*.py" -v
)
if errorlevel 1 exit /b 1
echo.
echo All lab smoke tests passed.
