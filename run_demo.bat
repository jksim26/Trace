@echo off
REM ============================================================
REM  Trace demo — double-click this file to run the 3 scenes.
REM  (Tanglin Rise: capture -> red invalidation alert -> recall)
REM  Needs: Trace\.env with DASHSCOPE_API_KEY (already set up).
REM ============================================================
cd /d "%~dp0Trace"
python cli.py
echo.
echo (demo finished - press any key to close this window)
pause >nul
