set directory_current=%cd%
cd c:\gh
git clone https://github.com/oomlout/oomlout_utility_image_trace
cd c:\gh\oomlout_utility_image_trace
git pull 
cd %directory_current%
python c:\gh\oomlout_utility_image_trace\working.py
cd %directory_current%

REM then run the following command to create a trace image



