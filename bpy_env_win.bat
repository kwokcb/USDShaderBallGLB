@echo off
REM Windows version
REM Usage:
REM   bpy_env.bat             -- activate venv and install bpy
REM   bpy_env.bat deactivate  -- deactivate venv

IF "%1"=="deactivate" (
    IF DEFINED VIRTUAL_ENV (
        echo Deactivating the environment
        call bpy_env\Scripts\deactivate.bat
    ) ELSE (
        echo No virtual environment is currently active.
    )
) ELSE (
    IF NOT EXIST "bpy_env" (
        echo Creating Python virtual environment in .\bpy_env
        python -m venv bpy_env
    )
    echo Activating the environment
    call bpy_env\Scripts\activate.bat
    echo Upgrading pip and installing bpy...
    python -m pip install --upgrade pip
    pip install bpy
)
