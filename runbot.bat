@echo off
rem Bypass "Terminate Batch Job" prompt.
if "%~1"=="-FIXED_CTRL_C" (
   REM Remove the -FIXED_CTRL_C parameter
   SHIFT
) ELSE (
   REM Run the batch with <NUL and -FIXED_CTRL_C
   CALL <NUL %0 -FIXED_CTRL_C %*
   GOTO :EOF
)

set var=0
cls
:srcds
title Launcher - Restarted %var% times...
echo (%time%) Server started.
start /wait Kirsi" "Bot.py
set /a var+=1
echo.
echo (%time%) WARNING: Bot closed or crashed, restarting.
goto srcds