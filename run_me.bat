@echo off
:start
cls
echo assistant script started!
python --version>NUL
if errorlevel == 9020 goto installPython
goto runScript

:installPython
>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"
if '%errorlevel%' NEQ '0' (
    echo requesting administrative privileges...
    echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
    set params = %*:"=""
    echo UAC.ShellExecute "cmd.exe", "/c %~s0 %params%", "", "runas", 1 >> "%temp%\getadmin.vbs"

    "%temp%\getadmin.vbs"
    del "%temp%\getadmin.vbs"
    exit /B
)
    pushd "%CD%"
    CD /D "%~dp0"
:--------------------------------------
echo python not found!
echo downloading the python3.10.4 amd64 version
curl https://www.python.org/ftp/python/3.10.4/python-3.10.4-amd64.exe -o "%temp%\python_install.exe"
echo installing python quietly.. please wait..
"%temp%\python_install.exe" /quiet InstallAllUsers=1 PrependPath=1
echo.
echo python installed successfully!
echo removing extra files..
del "%temp%\python_install.exe"
goto runScript

:runScript
echo.
python ssdc_bot_alt.py
pause