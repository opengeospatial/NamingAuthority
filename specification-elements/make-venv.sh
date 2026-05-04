#!/usr/bin/env bash

set -e

VENV_NAME=".venv"

echo "Creating virtual environment..."
python3 -m venv $VENV_NAME

echo "Activating virtual environment..."
source $VENV_NAME/bin/activate

echo "Upgrading pip..."
pip install --upgrade pip

echo "Installing dependencies..."
#pip install jsonref
pip install lxml

echo ""
echo "Done!"
echo "To activate later, run:"
echo "source $VENV_NAME/bin/activate"
