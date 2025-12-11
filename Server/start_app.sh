#! /bin/bash


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

cd /data/Musicfy_py/
source /data/py_venv/bin/activate 

echo "=-=-=-===============================-=-=" $(date) "=--=----------=============================================-=-=--=" >> logs/logging_musicfy.log
echo "Starting app $(date)"
nohup /data/py_venv/bin/python3 ./master_launcher.py >> logs/logging_musicfy.log &
echo "=-=-=-===============================-=-=" $(date) "=--=----------=============================================-=-=--=" >> logs/housekeeping_logging.log
echo "Starting Housekeeping $(date)"
nohup /data/py_venv/bin/python3 ./housekeeping_linux.py >> logs/housekeeping_logging.log &


