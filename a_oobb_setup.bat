cd c:\gh
git clone https://github.com/oomlout/oomlout_opsc_version_3
git clone https://github.com/oomlout/oomlout_oobb_version_4
git clone https://github.com/oomlout/oomlout_oobb_version_4_generated_parts
cd c:\gh\oomlout_opsc_version_3
git pull
cd c:\gh\oomlout_oobb_version_4
git pull
cd c:\gh\oomlout_oobb_version_4_generated_parts
git pull

SET "NEW_PATH_1=C:\gh\oomlout_opsc_version_3"
SET "NEW_PATH_2=C:\gh\oomlout_oobb_version_4"
SET "NEW_PATH_3=C:\gh\oomlout_oobb_version_4_generated_parts"

ECHO %PATH% | FINDSTR /I /C:"%NEW_PATH_1%" >NUL
IF ERRORLEVEL 1 SET "PATH=%PATH%;%NEW_PATH_1%"

ECHO %PATH% | FINDSTR /I /C:"%NEW_PATH_2%" >NUL
IF ERRORLEVEL 1 SET "PATH=%PATH%;%NEW_PATH_2%"

ECHO %PATH% | FINDSTR /I /C:"%NEW_PATH_3%" >NUL
IF ERRORLEVEL 1 SET "PATH=%PATH%;%NEW_PATH_3%"