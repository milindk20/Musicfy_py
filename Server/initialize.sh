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
pip install -r /data/Musicfy_py/Linux/requirements.txt

# Set up environment variables (if any)
# export VAR_NAME=value

# Print success message
echo "Environment setup complete. Virtual environment is ready."

deactivate

# Copy start_app.sh to /data/
cp Musicfy_py/Server/start_app.sh /data/
# Create logs directory
mkdir /data/Musicfy_py/logs
# Create Downloads Directory
mkdir /$(whoami)/Downloads/Music
# change the permission set to execute for start app
chmod +x /data/start_app.sh

# kill all the running processes of previous running application 
KEYWORD="app"

# Find matching process IDs (excluding grep and this script)
echo $(ps -ef | grep "$KEYWORD" | grep -v grep )

PIDS=$(ps -ef | grep "$KEYWORD" | grep -v grep | grep -v "$0" | awk '{print $2}')

if [ -z "$PIDS" ]; then
    echo "No processes found matching keyword: $KEYWORD"
else
    echo "Killing the following processes:"
    echo "$PIDS"
    # Forcefully kill the processes
    kill -9 $PIDS
    echo "Processes killed successfully."
fi

# Start the application
bash /data/start_app.sh
