d:
set root_path=D:\GitHub\AiProject
cd %root_path%
cxFreeze --script main.py
pause
set exe_path=%root_path%\build\exe.win-amd64-3.10
XCOPY %root_path%\Assets\ %exe_path%\Assets\ /E /I
XCOPY %root_path%\Temp\ %exe_path%\Temp\ /E /I
XCOPY %root_path%\Templates\ %exe_path%\Templates\ /E /I
XCOPY %root_path%\Views\ %exe_path%\Views\ /E /I
XCOPY %root_path%\Sqlite\ %exe_path%\Sqlite\ /E /I
XCOPY %root_path%\.venv\Lib\site-packages\sqlalchemy\ %exe_path%\lib\sqlalchemy\/E /I
echo END!
pause
