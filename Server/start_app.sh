#! /bin/bash


cd /data/Musicfy_py/
source /data/py_venv/bin/activate 

echo "=-=-=-===============================-=-=" $(date) "=--=----------=============================================-=-=--=" >> logs/logging_musicfy.log
echo "Starting app $(date)"
nohup /data/py_venv/bin/python3 ./master_launcher.py >> logs/logging_musicfy.log &
echo "=-=-=-===============================-=-=" $(date) "=--=----------=============================================-=-=--=" >> logs/housekeeping_logging.log
echo "Starting Housekeeping $(date)"
nohup /data/py_venv/bin/python3 ./housekeeping_linux.py >> logs/housekeeping_logging.log &


