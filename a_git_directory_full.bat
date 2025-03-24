@echo off
REM Check if %OOMLOUT_DIRECTORY% is set, if not set it to %1%

set OOMLOUT_DIRECTORY=%1%

set GIT_DIRECTORY_FULL_PATH=c:\gh\%OOMLOUT_DIRECTORY%
set GITHUB_URL=https://github.com/oomlout/%OOMLOUT_DIRECTORY%
cd c:\gh
git clone %GITHUB_URL%
cd %GIT_DIRECTORY_FULL_PATH%
git pull
start %GIT_DIRECTORY_FULL_PATH%
call code %GIT_DIRECTORY_FULL_PATH%

exit /b