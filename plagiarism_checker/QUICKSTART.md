# ⚡ Quick Reference Guide

## 🚀 Quick Start (30 seconds)

### Windows Users
```bash
# Double-click these files in order:
1. setup.bat      # First time only
2. run.bat        # Every time you want to use app
3. Open: http://localhost:5000
```

### macOS/Linux Users
```bash
# In terminal:
bash setup.sh      # First time only
bash run.sh        # Every time you want to use app
# Open: http://localhost:5000
```

---

## 📋 Checklist

- [ ] Python 3.8+ installed
- [ ] Project folder downloaded
- [ ] `setup.bat` (Windows) or `setup.sh` (macOS/Linux) executed
- [ ] `.env` file updated with Gemini API key
- [ ] Application running at http://localhost:5000
- [ ] Upload two PDFs and analyze

---

## 🔑 API Key Setup (2 minutes)

### Step 1: Get API Key
- Visit: https://ai.google.dev/
- Click: "Get API Key"
- Copy: Your API key

### Step 2: Add to .env
- Edit: `.env` file
- Find: `GEMINI_API_KEY=your_gemini_api_key_here`
- Replace: With your actual key
- Save: File

### Step 3: Restart App
- Stop: Flask server (Ctrl+C)
- Run: `python app.py` again

---

## 📁 Project Structure

```
plagiarism_checker/
├── app.py                ← Main application
├── config.py             ← Configuration
├── requirements.txt      ← Dependencies
├── .env                  ← API key (edit this!)
├── README.md             ← Full documentation
├── SETUP_GUIDE.md        ← Detailed setup
├── ARCHITECTURE.md       ← Technical details
│
├── templates/
│   ├── base.html         ← Navigation
│   ├── index.html        ← Upload page
│   └── result.html       ← Results page
│
└── static/
    └── style.css         ← Styling
```

---

## 🛠️ Common Commands

### Activate Virtual Environment
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### Run Application
```bash
python app.py
# Visit: http://localhost:5000
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Update Dependencies
```bash
pip install --upgrade -r requirements.txt
```

### Deactivate Virtual Environment
```bash
deactivate
```

---

## 🐛 Common Issues & Fixes

| Issue | Fix |
|-------|-----|
| "Module not found" | Run: `pip install -r requirements.txt` |
| "API key error" | Check `.env` file and API key |
| "Port 5000 in use" | Edit `.env`, change PORT to 5001 |
| "PDF extraction failed" | Use PDF with readable text (not scanned) |
| "File too large" | Maximum file size is 10MB |

---

## 📊 Similarity Levels

| Score | Level | Meaning |
|-------|-------|---------|
| 0-30% | Low | Likely original |
| 30-70% | Moderate | Some overlap - check citations |
| 70-100% | High | Significant overlap - investigate |

---

## 🎯 Usage Steps

1. **Open browser** → http://localhost:5000
2. **Upload PDF 1** → Click upload field
3. **Upload PDF 2** → Click upload field
4. **Click Analyze** → Wait for results
5. **Review Results** → See TF-IDF & AI analysis
6. **Print Report** → Optional: save as PDF

---

## 🔒 Security Tips

✅ **DO:**
- Keep `.env` file private
- Never share API key
- Use HTTPS in production
- Update dependencies regularly

❌ **DON'T:**
- Commit `.env` to Git
- Expose API key in code
- Use in production mode without HTTPS
- Store sensitive data in uploads folder

---

## 📱 Features

✅ PDF file upload (max 10MB)
✅ Text extraction from PDFs
✅ TF-IDF similarity analysis (ML)
✅ Gemini AI semantic analysis
✅ Detailed plagiarism report
✅ Print-friendly results
✅ Responsive design (mobile-friendly)
✅ Error handling
✅ Fast processing (5-15 seconds)

---

## 🌐 Browser Compatibility

| Browser | Status |
|---------|--------|
| Chrome | ✅ Full support |
| Firefox | ✅ Full support |
| Safari | ✅ Full support |
| Edge | ✅ Full support |
| IE 11 | ⚠️ Partial support |

---

## 📞 Help Resources

1. **README.md** - Full documentation
2. **SETUP_GUIDE.md** - Detailed setup steps
3. **ARCHITECTURE.md** - Technical details
4. **Error Messages** - Read carefully!
5. **Browser Console** - Press F12 for errors

---

## 🚪 File Size Limits

| Item | Limit |
|------|-------|
| PDF 1 | 10 MB |
| PDF 2 | 10 MB |
| Total | 20 MB |
| Processing | ~5-15 seconds |

---

## 💾 Storage Info

- **Temporary files:** Auto-deleted after analysis
- **No permanent storage:** Files not saved
- **No database:** In-memory processing only
- **Privacy:** Your documents are not stored

---

## 🔧 Configuration Options

Edit `.env` file to configure:

```env
# Required
GEMINI_API_KEY=your_key_here

# Optional
FLASK_ENV=development        # or production
FLASK_DEBUG=True            # or False
PORT=5000                   # Change port if needed
SECRET_KEY=your_secret      # For production
```

---

## 📈 Performance Tips

1. **Use smaller PDFs** if possible
2. **Close other apps** for faster processing
3. **Check internet connection** for API calls
4. **Use modern browser** for best experience
5. **Avoid very large documents** (>20 pages)

---

## 🎓 Learning Resources

- **Flask:** https://flask.palletsprojects.com/
- **Google Gemini:** https://ai.google.dev/
- **scikit-learn:** https://scikit-learn.org/
- **Python:** https://python.org/

---

## 📝 Notes

- Application runs locally (not cloud-based)
- Requires internet for Gemini API calls
- No data is permanently stored
- Free tier API has rate limits
- Check Google Cloud Console for usage

---

## ✨ Tips & Tricks

1. **Print results:** Click "Print Report" button
2. **Check analysis:** Scroll down for full explanation
3. **Compare PDFs:** Use text previews for reference
4. **Fast processing:** Keep PDFs under 50 pages
5. **Test feature:** Try with sample PDFs first

---

## 🎯 Next Steps

1. ✅ Setup complete? Run `python app.py`
2. 🌐 Visit http://localhost:5000
3. 📄 Upload two PDFs
4. ✨ Get instant plagiarism analysis
5. 📊 Review results

---

**Questions? Check README.md or SETUP_GUIDE.md**

**Happy analyzing! 🚀**
