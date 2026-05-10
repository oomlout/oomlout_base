@echo off
title Ollama - RTX 3090 - Qwen 35B Safer VRAM Mode

echo Killing existing Ollama...
taskkill /F /IM ollama.exe >nul 2>&1

echo.
echo Setting Ollama environment variables...

REM Debug logging so you can verify settings reached the runner.
set OLLAMA_DEBUG=1

REM Needed for KV cache quantization.
set OLLAMA_FLASH_ATTENTION=1

REM Equivalent to llama.cpp-style q8_0 KV cache.
set OLLAMA_KV_CACHE_TYPE=q8_0

REM Keep one active request/model path to avoid extra VRAM use.
set OLLAMA_NUM_PARALLEL=1
set OLLAMA_MAX_LOADED_MODELS=1

REM Reduce default context from 32768 to 16384.
REM This is the main fix attempt.
set OLLAMA_CONTEXT_LENGTH=16384

REM Optional safety margin. 512 MiB reserved.
REM Increase to 1073741824 for 1 GiB if things are unstable.
set OLLAMA_GPU_OVERHEAD=536870912

REM Keep model loaded for convenience.
set OLLAMA_KEEP_ALIVE=30m

REM Network access on LAN.
set OLLAMA_HOST=0.0.0.0:11434

echo.
echo Current variables:
echo OLLAMA_FLASH_ATTENTION=%OLLAMA_FLASH_ATTENTION%
echo OLLAMA_KV_CACHE_TYPE=%OLLAMA_KV_CACHE_TYPE%
echo OLLAMA_CONTEXT_LENGTH=%OLLAMA_CONTEXT_LENGTH%
echo OLLAMA_NUM_PARALLEL=%OLLAMA_NUM_PARALLEL%
echo OLLAMA_MAX_LOADED_MODELS=%OLLAMA_MAX_LOADED_MODELS%
echo OLLAMA_GPU_OVERHEAD=%OLLAMA_GPU_OVERHEAD%
echo OLLAMA_KEEP_ALIVE=%OLLAMA_KEEP_ALIVE%
echo OLLAMA_HOST=%OLLAMA_HOST%
echo.

echo Starting Ollama server...
echo Leave this window open.
echo.

ollama serve

pause