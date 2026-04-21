#!/bin/bash

# Run script for plagiarism checker (macOS/Linux)

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found. Running setup first..."
    bash setup.sh
fi

# Activate virtual environment
source venv/bin/activate

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "Warning: .env file not found. Creating template..."
    cat > .env << EOF
# Gemini API Configuration
# Get your API key from: https://ai.google.dev/
GEMINI_API_KEY=your_gemini_api_key_here

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
EOF
    echo "Please update .env file with your Gemini API key and run again."
    exit 1
fi

# Start the application
echo ""
echo "===================================="
echo "Starting AI Plagiarism Checker"
echo "===================================="
echo ""
echo "Application running at: http://localhost:5000"
echo "Press Ctrl+C to stop the server"
echo ""

python app.py
