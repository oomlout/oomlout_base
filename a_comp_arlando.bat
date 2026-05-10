start python C:\gh\oomlout_base_webserver_flask_template_oomp\working_web_oomp.py 

REM ollama section

start a_comp_arlando_ollama.bat

start open-webui serve
start powershell -NoExit -Command "cd 'C:\od\OneDrive\docs\ai_agent_claude_code_local\test_app_1\glm-4.7-flashq4_K_M'; ollama launch claude --model glm-4.7-flash:q4_K_M -- --dangerously-skip-permissions"
start "C:\Program Files (x86)\openhardwaremonitor\OpenHardwareMonitor.exe"