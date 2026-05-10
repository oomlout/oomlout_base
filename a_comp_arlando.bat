start python C:\gh\oomlout_base_webserver_flask_template_oomp\working_web_oomp.py 
taskkill /IM ollama.exe /F
start ollama serve
start open-webui serve
start powershell -NoExit -Command "cd 'C:\od\OneDrive\docs\ai_agent_claude_code_local'; ollama launch claude --model gpt-oss:20b -- --dangerously-skip-permissions"
