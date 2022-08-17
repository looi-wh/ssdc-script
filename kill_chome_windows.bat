@echo off
echo please make sure you do not have anything important in any instance of chrome
echo press any key to kill chrome

pause >nul
taskkill /im chrome.exe /f
echo killed chrome brutally
pause
exit