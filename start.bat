@echo off
:: =========================================================================
:: DELHI POLICE - LAW & ORDER DEPLOYMENT QUICK INSTRUCTION PORTAL
:: Startup & Deployment System
:: =========================================================================
title Delhi Police - Law & Order Deployment Quick Instructions & Admin Portal

cd /d "%~dp0"

cls
echo =========================================================================
echo  DELHI POLICE - LAW & ORDER DEPLOYMENT QUICK INSTRUCTION PORTAL
echo  Modern Brutalist-Institutional Field Reference System
echo =========================================================================
echo.

echo [1/2] Pre-rendering static HTML pages, checking EN/HI invariants & QR codes...
python build.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Build failed! Please check your Python installation and content/content.json.
    pause
    exit /b %ERRORLEVEL%
)
echo.

echo [2/2] Starting Server & Auto-Opening Web Browser...
python admin_server.py

pause
