set "currentDirectory=%cd%
pyinstaller --distpath %currentDirectory% -i favicon.ico --onefile Braids-Manager.py
pause