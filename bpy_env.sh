# Usage:
#   source ./bpy_env.sh             # activate venv and install bpy
#   source ./bpy_env.sh deactivate  # deactivate venv

if [ "$1" = "deactivate" ]; then
    if [ -n "$VIRTUAL_ENV" ]; then
        echo "Deactivating the environment"
        deactivate
    else
        echo "No virtual environment is currently active."
    fi
else
    if [ ! -d "bpy_env" ]; then
        echo "Creating Python virtual environment in ./bpy_env"
        python -m venv bpy_env
    fi
    echo "Activating the environment"
    # shellcheck disable=SC1091
    source ./bpy_env/bin/activate
    echo "Upgrading pip and installing bpy..."
    python -m pip install --upgrade pip
    pip install bpy
fi
