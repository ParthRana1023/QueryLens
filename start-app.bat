@echo off

:: Start Client
cd client
start cmd /k "npm install && npm run dev"

:: Start Server
cd ../server
python3.11 -m venv venv
call venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload