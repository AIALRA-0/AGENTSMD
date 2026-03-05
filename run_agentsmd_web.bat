@echo off
set BASE_DIR=%~dp0
if exist "%BASE_DIR%\.venv_agentsmd_web\Scripts\python.exe" (
  "%BASE_DIR%\.venv_agentsmd_web\Scripts\python.exe" "%BASE_DIR%\launch_agentsmd_web.py"
) else (
  py -3 "%BASE_DIR%\launch_agentsmd_web.py"
)
