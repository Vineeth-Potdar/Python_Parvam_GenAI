# 🚀 AI-Powered Plagiarism Checker - Complete Setup Guide

This guide will help you set up and run the AI-powered Plagiarism Checker application.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Getting Your Gemini API Key](#getting-your-gemini-api-key)
3. [Installation](#installation)
4. [Configuration](#configuration)
5. [Running the Application](#running-the-application)
6. [Troubleshooting](#troubleshooting)

---

## Prerequisites

Before you begin, ensure you have:

- **Python 3.8 or higher** - [Download](https://www.python.org/downloads/)
- **Internet connection** - For API calls to Google Gemini
- **A Google account** - To generate Gemini API key
- **Git** (optional) - For cloning the repository

### Verify Python Installation

Open a terminal/command prompt and run:

```bash
python --version
```

You should see something like `Python 3.10.x` or higher.

---

## Getting Your Gemini API Key

### Step 1: Visit Google AI Studio

1. Go to [Google AI Studio](https://ai.google.dev/)
2. Click on **"Get API Key"** button
3. If prompted, sign in with your Google account

### Step 2: Create API Key

1. Click **"Create API Key"**
2. Select or create a Google Cloud project
3. Click **"Create API Key in Google Cloud Console"**
4. The API key will be generated and copied to clipboard
5. Save it in a safe place

### Step 3: Enable Required APIs

The Generative AI API should be automatically enabled. If not:

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Select your project
3. Search for "Generative AI API"
4. Click "Enable"

---

## Installation

### Option 1: Quick Setup (Windows Users)

1. **Download the project** to your computer
2. **Double-click** `setup.bat` file
3. Wait for setup to complete
4. Follow the [Configuration](#configuration) section

### Option 2: Manual Setup (All Platforms)

#### Windows

```bash
# Open Command Prompt in the project folder

# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

#### macOS/Linux

```bash
# Open Terminal in the project folder

# Make setup script executable
chmod +x setup.sh

# Run setup
./setup.sh
```

---

## Configuration

### Step 1: Edit .env File

1. Open the `.env` file in any text editor (VS Code, Notepad, etc.)
2. Find this line:
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   ```
3. Replace `your_gemini_api_key_here` with your actual API key
4. Save the file

**Example .env file:**
```env
GEMINI_API_KEY=AIzaSyDx-xxxxxxxxxxxxxxxxxxxxxxxxxxxx

FLASK_ENV=development
FLASK_DEBUG=True
```

### Step 2: Verify Configuration

Create a test file to verify your setup:

1. Open a terminal in the project folder
2. Activate virtual environment:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`

3. Test the setup:
   ```bash
   python -c "import google.generativeai as genai; print('✓ Gemini AI module loaded successfully')"
   ```

If successful, you should see: `✓ Gemini AI module loaded successfully`

---

## Running the Application

### Option 1: Quick Start (Windows)

Simply double-click the `run.bat` file. The application will start automatically.

### Option 2: Manual Start

#### Windows

```bash
# Activate virtual environment (if not already active)
venv\Scripts\activate

# Run the application
python app.py
```

#### macOS/Linux

```bash
# Activate virtual environment
source venv/bin/activate

# Run the application
python app.py
```

### Step 3: Access the Application

1. Open your web browser
2. Go to: **http://localhost:5000**
3. You should see the plagiarism checker interface

**Expected output in terminal:**
```
 * Running on http://127.0.0.1:5000
 * Press CTRL+C to quit
 * Restarting with reloader
```

---

## Using the Application

### Step 1: Upload PDFs

1. On the home page, you'll see two upload fields
2. Click **"Upload PDF 1"** and select your first document
3. Click **"Upload PDF 2"** and select your second document
4. Click the **"Analyze Plagiarism"** button

### Step 2: View Results

The application will:
1. Extract text from both PDFs
2. Calculate TF-IDF similarity (ML-based detection)
3. Call Gemini AI for semantic analysis
4. Display comprehensive results

### Step 3: Interpret Results

- **0-30%**: Low similarity (document is likely original)
- **30-70%**: Moderate similarity (review for citations)
- **70-100%**: High similarity (potential plagiarism detected)

---

## Troubleshooting

### Issue 1: "ModuleNotFoundError: No module named 'flask'"

**Solution:**
```bash
# Activate virtual environment first
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# Reinstall dependencies
pip install -r requirements.txt
```

### Issue 2: "GEMINI_API_KEY not configured"

**Solution:**
1. Check that `.env` file exists in project folder
2. Verify the API key format:
   ```
   GEMINI_API_KEY=AIzaSyDx-xxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```
3. Make sure there are no extra spaces or quotes

### Issue 3: API Key Error "400: Invalid API Key"

**Solution:**
1. Verify API key is correct (copy from Google AI Studio)
2. Check if API is enabled in Google Cloud Console
3. Regenerate a new API key

### Issue 4: "413 Request Entity Too Large"

**Solution:**
- Your PDF files are too large (max 10MB each)
- Try uploading smaller PDF files
- You can split large PDFs using online tools

### Issue 5: "Could not extract text from PDF"

**Solution:**
- The PDF might be scanned images (no extractable text)
- Try a different PDF file with actual text content
- Ensure PDF is not encrypted

### Issue 6: Port 5000 already in use

**Solution:**
Open `.env` file and change the port:
```env
PORT=5001
```

Then restart the application.

### Issue 7: Application won't start

**Solution:**
1. Close the terminal and reopen it
2. Navigate to project folder
3. Activate virtual environment
4. Run: `python -m flask run --debug`

---

## Production Deployment

To deploy this application to production:

1. **Change SECRET_KEY** in `config.py`
2. **Set FLASK_ENV=production** in `.env`
3. **Use a production WSGI server** like Gunicorn:
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

4. **Use environment variables** instead of .env file
5. **Enable HTTPS** with SSL certificates
6. **Set up a reverse proxy** (Nginx, Apache)

---

## File Descriptions

| File | Purpose |
|------|---------|
| `app.py` | Main Flask application |
| `config.py` | Flask configuration settings |
| `requirements.txt` | Python dependencies |
| `.env` | Environment variables (API keys) |
| `.gitignore` | Files to ignore in Git |
| `templates/` | HTML templates |
| `static/` | CSS and static files |
| `uploads/` | Temporary PDF storage |

---

## Security Notes

⚠️ **Important:**

- Never share your API key in public repositories
- Don't commit `.env` file to version control (it's in `.gitignore`)
- Use environment variables in production
- Regularly rotate API keys
- Monitor API usage in Google Cloud Console
- Keep dependencies updated: `pip install --upgrade -r requirements.txt`

---

## Support & Resources

### Documentation
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Google Generative AI](https://ai.google.dev/tutorials/python_quickstart)
- [Scikit-learn Documentation](https://scikit-learn.org/)

### Community Help
- Check the README.md file
- Review error messages carefully
- Check browser console (F12) for errors
- Review application logs in terminal

### Contact
For issues or questions, review the troubleshooting section above.

---

## Next Steps

1. ✅ Setup and configuration complete
2. ✅ Application is running
3. 🎯 Start analyzing documents!

**Happy plagiarism checking!**

---

*Last updated: 2024*
*Version: 1.0.0*
