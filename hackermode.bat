@echo off
if "%imahacker%"=="1" (
    set imahacker=0
    tts "deactivating hacker mode"
    color 0F
    tts "hacker mode deactivated"
) else (
    set imahacker=1
    tts "activating hacker mode"
    color 0A
    tts "hacker mode activated"
)