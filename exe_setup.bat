set "root_path=%~dp0"
cxFreeze --script main.py --icon=%root_path%Assets\icons\logo_orange.ico  --target-dir dist --base-name="win32gui"
set exe_path=%root_path%dist
XCOPY %root_path%\Assets\ %exe_path%\Assets\ /E /I
XCOPY %root_path%\Temp\ %exe_path%\Temp\ /E /I
XCOPY %root_path%\Templates\ %exe_path%\Templates\ /E /I
XCOPY %root_path%\Views\ %exe_path%\Views\ /E /I
XCOPY %root_path%\Sqlite\ %exe_path%\Sqlite\ /E /I
XCOPY %root_path%\.venv\Lib\site-packages\sqlalchemy\ %exe_path%\lib\sqlalchemy\/E /I
echo END!
pause
