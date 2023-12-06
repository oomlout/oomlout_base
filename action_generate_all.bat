@echo off
setlocal

rem Fetch the latest changes from the remote repository
git fetch origin

rem echo the current folder name 
echo working_on %cd%

set run=0

rem check if %overwrite% is set if not set it to 1
if "%overwrite%"=="" (
    set overwrite=1
)

rem if git isn't set set it to one
if "%git%"=="" (
    set git=1
)

rem Get the commit hashes of the local and remote main branches
for /f %%i in ('git rev-parse HEAD') do set localCommit=%%i
for /f %%i in ('git rev-parse origin/main') do set remoteCommit=%%i
rem Compare the commit hashes to check for changes
rem Compare the commit hashes to check for changes

if "%localCommit%" neq "%remoteCommit%" (
    echo     changes_made running
    set run=1
)
rem run regardless if git is off
if "%git%" neq "1" (
    echo     git_off running
    set run=1
)



if %run% equ 1 (
    echo    running
    rem Your action for an existing Git repository with changes goes here.
    git pull
    rem if overwrite = 1
    if %overwrite% equ 1 (
        call action_generate_kicad_outputs_overwrite.py
        call action_generate_corel_outputs_overwrite.py
        call action_generate_office_outputs_overwrite.py
        call action_generate_resolutions_overwrite.py
        call action_generate_readme_outputs_overwrite.py
    ) else (
        call action_generate_kicad_outputs.py
        call action_generate_corel_outputs.py
        call action_generate_office_outputs.py
        call action_generate_resolutions.py
        call action_generate_readme_outputs.py
    )
    action_git_commit.py

) else (
    echo     not running
    rem Your action for an existing Git repository without changes goes here.
)

endlocal
