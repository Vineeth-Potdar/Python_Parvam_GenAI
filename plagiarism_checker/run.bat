@echo off
REM Windows batch script to run the plagiarism checker

REM Check if virtual environment exists
if not exist "venv" (
    echo Virtual environment not found. Running setup first...
    call setup.bat
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Check if .env file exists
if not exist ".env" (
    echo Warning: .env file not found. Creating template...
    (
        echo # Gemini API Configuration
        echo # Get your API key from: https://ai.google.dev/
        echo GEMINI_API_KEY=your_gemini_api_key_here
        echo.
        echo # Flask Configuration
        echo FLASK_ENV=development
        echo FLASK_DEBUG=True
    ) > .env
    echo Please update .env file with your Gemini API key and run again.
    pause
    exit /b 1
)

REM Start the application
echo.
echo ====================================
echo Starting AI Plagiarism Checker
echo ====================================
echo.
echo Application running at: http://localhost:5000
echo Press Ctrl+C to stop the server
echo.

python app.py
