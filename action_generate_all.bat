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


rem Get the commit hashes of the local and remote main branches
for /f %%i in ('git rev-parse HEAD') do set localCommit=%%i
for /f %%i in ('git rev-parse origin/main') do set remoteCommit=%%i
rem Compare the commit hashes to check for changes
rem Compare the commit hashes to check for changes

if "%localCommit%" neq "%remoteCommit%" (
    set run=1
)



if %run% equ 1 (
    echo     changes_made
    rem Your action for an existing Git repository with changes goes here.
    git pull
    rem if overwrite = 1
    if %overwrite% equ 1 (
        call action_generate_kicad_outputs_overwrite.bat
        call action_generate_corel_outputs_overwrite.bat
        call action_generate_office_outputs_overwrite.bat
        call action_generate_resolutions_overwrite.bat
        call action_generate_readme_outputs_overwrite.bat
    ) else (
        call action_generate_kicad_outputs.bat
        call action_generate_corel_outputs.bat
        call action_generate_office_outputs.bat
        call action_generate_resolutions.bat
        call action_generate_readme_outputs.bat
    )
    action_git_commit.py

) else (
    echo     changes_not_made
    rem Your action for an existing Git repository without changes goes here.
)

endlocal
