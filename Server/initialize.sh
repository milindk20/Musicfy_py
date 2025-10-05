#!/bin/bash

# Update package lists and install system dependencies
 apt update 
 apt install -y python3 python3-pip python3-venv git

cd /data

# Create a virtual environment
python3 -m venv py_venv

# Activate the virtual environment
source py_venv/bin/activate

# Install required Python packages
pip install --upgrade pip
pip install -r ../Linux/requirements.txt

# Set up environment variables (if any)
# export VAR_NAME=value

# Print success message
echo "Environment setup complete. Virtual environment is ready."

deactivate

# Copy start_app.sh to /data/
cp Musicfy_py/Server/start_app.sh /data/
# Create logs directory
mkdir /data/Musicfy_py/logs
# Start the application
bash /data/start_app.sh
