set directory_current=%cd%
set url=%1%
cd c:\gh
git clone https://github.com/oomlout/oomlout_utility_file_git_github_clone
cd oomlout_utility_file_git_github_clone
git pull 
cd %directory_current%
python c:\gh\oomlout_utility_file_git_github_clone\working.py -u %url%
cd %directory_current%

REM then run the following command to create a trace image



