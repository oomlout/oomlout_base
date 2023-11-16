@echo off
setlocal

rem Fetch the latest changes from the remote repository
git fetch origin

rem echo the current folder name 
echo working_on %cd%


rem Get the commit hashes of the local and remote main branches
for /f %%i in ('git rev-parse HEAD') do set localCommit=%%i
for /f %%i in ('git rev-parse origin/main') do set remoteCommit=%%i

rem Compare the commit hashes to check for changes
if "%localCommit%" neq "%remoteCommit%" (
    echo     changes_made
    rem Your action for an existing Git repository with changes goes here.
    git pull
    action_generate_kicad_outputs_overwrite.py 
    action_generate_corel_outputs_overwrite.py
    action_generate_office_outputs_overwrite.py
    action_generate_resolutions_overwrite.py
    action_generate_readme_outputs_overwrite.py
    action_git_commit.py

) else (
    echo     changes_not_made
    rem Your action for an existing Git repository without changes goes here.
)

endlocal
