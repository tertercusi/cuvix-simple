@echo off

call .venv\Scripts\activate.bat
pip install -r requirements.txt
py windows.py
