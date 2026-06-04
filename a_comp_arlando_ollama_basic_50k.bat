@echo off
title Ollama - Normal Settings

echo Killing existing Ollama...
taskkill /F /IM ollama.exe >nul 2>&1

echo Clearing custom Ollama environment variables...

set OLLAMA_DEBUG=1
set OLLAMA_FLASH_ATTENTION=
set OLLAMA_KV_CACHE_TYPE=
set OLLAMA_CONTEXT_LENGTH=50000
set OLLAMA_NUM_PARALLEL=1
set OLLAMA_MAX_LOADED_MODELS=
set OLLAMA_GPU_OVERHEAD=
set OLLAMA_KEEP_ALIVE=
set OLLAMA_LOG_LEVEL=debug
set OLLAMA_FLASH_ATTN=1

REM Keep LAN access if you still want it.
REM Remove this line too if you want fully default localhost-only behavior.
set OLLAMA_HOST=0.0.0.0:11434

echo.
echo Starting Ollama with normal/default settings...
echo.

ollama serve

pause