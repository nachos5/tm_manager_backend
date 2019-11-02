#!/bin/bash

# Start server

python_venv_activate="$PWD/venv/bin/activate"

# Give access to functions
echo "Activating access to functions"
source $python_venv_activate

# Start server
echo "Starting server"
python manage.py runserver
