@echo off

echo "Running installation of"
echo "requirements.txt"
py -m pip install -r requirements.txt
echo "Runing the app"
py main.py