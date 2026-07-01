@echo off
REM ============================================================
REM  Trace ambient bubble — double-click to launch.
REM  Starts a tiny local web app and opens the bubble in your
REM  browser, wired live to the Trace engine (chat really works).
REM  Close this window (or Ctrl+C) to stop it.
REM ============================================================
cd /d "%~dp0Trace"
python bubble.py
if errorlevel 1 pause
