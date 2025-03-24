REM take in %OOMLOUT_DIRECTORY% clone it to c:\gh, then navigate there and pull
REM
REM

REM if %OOMLOUT_DIRECTORY% is not set, set it to %1%
if "%OOMLOUT_DIRECTORY%"=="" set OOMLOUT_DIRECTORY=%1%

set GIT_DIRECTORY_FULL_PATH=c:\gh\%OOMLOUT_DIRECTORY%
set GITHUB_URL=https://github.com/oomlout/%OOMLOUT_DIRECTORY%
cd c:\gh
git clone %GITHUB_URL%
cd %GIT_DIRECTORY_FULL_PATH%
git pull
REM start %GIT_DIRECTORY_FULL_PATH%
REM code %GIT_DIRECTORY_FULL_PATH%
exit /b