#!/usr/bin/env bash
VENV_DIR="venv"
REQUIREMENTS_FILE="requirements.txt"
PYTHON_BIN="python3"

setup_env() {
    if [ ! -f ".env" ]; then
        echo "Creating .env configuration..."
        cat <<EOT >> .env
APP_PORT=
DB_URL=
EOT
    fi
}

create_venv() {
    echo "creating venv in $VENV_DIR"
    $PYTHON_BIN -m venv "$VENV_DIR"
}

activate_venv() {
    source "$VENV_DIR/bin/activate"

    export PS1="(.venv) $PS1"
    echo "Virtual environment activated."
}

install_packages() {
    if [ -f "$REQUIREMENTS_FILE" ]; then
        echo "installing package listed in $REQUIREMENTS_FILE..."
        pip install --upgrade pip
        pip install -r "$REQUIREMENTS_FILE"
    else
        echo "no $REQUIREMENTS_FILE, skip install."
    fi
}

if [ ! -d "$VENV_DIR" ]; then
    create_venv
else
    echo "venv are already exist, skipping making the new one."
fi

setup_env
activate_venv
install_packages

echo "all done."

