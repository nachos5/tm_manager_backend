#!/bin/bash

# Install script for tm_manager_backed

which psql >> /dev/null

# Check if postgresql exists
if [[ $? -ne 0 ]]; then
  echo "Can't find postgres"
  exit 1
fi

python_venv="$PWD/venv"
python_venv_activate="$PWD/venv/bin/activate"
env="$PWD/.env"

# Check if directory venv exists
if [ ! -d $python_venv ]; then
  echo "Setting up venv"
  python3 -m venv venv
fi

# Give access to functions
echo "Activating access to functions"
source $python_venv_activate

# Check if last command was successfull
if [[ $? -ne 0 ]]; then
  echo "File $python_venv_activate not found"
  exit 1
fi

# Install python packages
echo "Installing python packages"
pip install -r "requirements/local.txt"

# Setup .env file
if [ ! -f $env ]; then
  echo -n "Enter postgres username: "
  read username
  echo -n "Enter postgres password: "
  read password
  echo -n "Enter a new postgres database name: "
  read database
  
  # Create a new database
  echo "Creating database $database"
  createdb -O $username $database

  # Create .env file
  echo "DATABASE_URL=postgres://$username:$password@localhost:5432/$database" > .env

  # Fill the database with relations
  echo "Filling the database $database with relations"
  python manage.py migrate

  # Fill the database with random data
  echo "Filling the relations in database $database with random data"
  python manage.py shell_plus << EOF
  generate_initial_data()
EOF

fi

echo "Installation done"
