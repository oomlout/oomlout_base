set "appdata_dir=%LOCALAPPDATA%"
echo Local App Data Directory is %appdata_dir%
set "gh_dir=%appdata_dir%\GitHubDesktop\app-3.4.18\resources\app\git\cmd"
cd %gh_dir%
git config --system core.longpaths true
pause