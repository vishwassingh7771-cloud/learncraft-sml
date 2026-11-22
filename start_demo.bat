@echo off
title LearnCraft AI - Final Project Demo
color 0B
echo =====================================================================
echo           LEARNCRAFT AI - FINAL PROJECT DEMO LAUNCHER     
echo     UN-SDG Goal 4: Quality Education -- Dynamic Curriculum Engine
echo =====================================================================
echo.
echo [1/2] Opening Interactive Web Prototype in your default browser...
start "" "%~dp0index.html"
echo       - Web prototype opened successfully in your browser!
echo.
echo [2/2] Launching Backend REST API Server on Port 5000...
cd /d "%~dp0backend"
start "LearnCraft AI Backend" cmd /k "node server.js"
echo       - Backend server launched in separate console!
echo.
echo =====================================================================
echo  Final deliverables in this folder:
echo   - LearnCraft_AI_Final_Project_Report.pdf / .docx
echo   - LearnCraft_AI_Final_Presentation.pptx
echo   - results\figures (all plots), models\ (trained models)
echo =====================================================================
echo.
echo Press any key to close this launcher window (server and UI will stay open).
pause >nul
