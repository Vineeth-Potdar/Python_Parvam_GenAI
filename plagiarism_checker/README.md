# 🔍 AI-Powered Plagiarism Checker

A modern, full-stack Flask web application that detects plagiarism using TF-IDF similarity analysis and Google's Gemini AI for semantic comparison.

## 📋 Features

✅ **PDF File Upload** - Upload two PDF documents for comparison
✅ **TF-IDF Analysis** - Machine learning-based similarity detection
✅ **Gemini AI Integration** - Advanced semantic analysis with explanations
✅ **User-Friendly Interface** - Clean Bootstrap 5 UI with responsive design
✅ **Real-time Results** - Instant plagiarism reports with detailed insights
✅ **Error Handling** - Graceful handling of invalid files and API errors
✅ **Print Support** - Export results as PDF

## 🏗️ Project Structure

```
plagiarism_checker/
├── app.py                    # Flask backend application
├── requirements.txt          # Python dependencies
├── .env                      # Environment variables (API key)
├── README.md                 # This file
│
├── templates/
│   ├── base.html            # Base template with navbar
│   ├── index.html           # Upload page
│   └── result.html          # Results display page
│
├── static/
│   └── style.css            # Custom styling
│
└── uploads/                 # Temporary PDF uploads (auto-created)
```

## 📦 Requirements

- Python 3.8+
- Flask 3.0.0
- PyPDF2 4.0.1
- pdfplumber 0.10.3
- scikit-learn 1.3.2
- google-generativeai 0.3.0
- python-dotenv 1.0.0

## 🚀 Quick Start

### 1. Clone or Navigate to Project

```bash
cd plagiarism_checker
```

### 2. Create Virtual Environment

#### Windows
```bash
python -m venv venv
venv\Scripts\activate
```

#### macOS/Linux
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Gemini API Key

#### Option A: Get Your API Key
1. Visit [Google AI Studio](https://ai.google.dev/)
2. Click "Get API Key"
3. Create a new API key in Google Cloud Console

#### Option B: Set Environment Variable

Edit `.env` file and add your API key:
```
GEMINI_API_KEY=your_api_key_here
```

### 5. Run Application

```bash
python app.py
```

The application will start at `http://localhost:5000`

## 🎯 Usage Guide

### Step 1: Upload PDFs
1. Navigate to the home page
2. Click on "Upload PDF 1" and select your first document
3. Click on "Upload PDF 2" and select your second document
4. Click "Analyze Plagiarism"

### Step 2: View Results
The results page will show:
- **TF-IDF Similarity Score** - Percentage match using machine learning
- **Gemini AI Analysis** - Semantic similarity level and explanation
- **Text Preview** - First 500 characters from each PDF
- **Recommendations** - Next steps based on similarity level

### Step 3: Interpret Results

| Similarity | Assessment | Action |
|-----------|-----------|--------|
| 0-30% | Low | Document is likely original |
| 30-70% | Moderate | Review for proper citations |
| 70-100% | High | Investigate potential plagiarism |

## 🔑 Environment Variables

```env
# Gemini API Configuration
GEMINI_API_KEY=your_key_here

# Flask Configuration (optional)
FLASK_ENV=development
FLASK_DEBUG=True
```

## 🎨 Frontend Features

- **Bootstrap 5** - Responsive and modern UI
- **Custom CSS** - Gradient backgrounds and smooth animations
- **Form Validation** - Client-side file type and size checks
- **Loading States** - Visual feedback during processing
- **FAQs** - Built-in help section

## ⚙️ Backend Architecture

### Flask Routes

| Route | Method | Purpose |
|-------|--------|---------|
| `/` | GET | Upload page |
| `/check` | POST | Process PDFs and return results |

### Key Functions

- `extract_text_from_pdf()` - Extract text using pdfplumber/PyPDF2
- `preprocess_text()` - Clean and normalize text
- `calculate_tfidf_similarity()` - ML-based similarity calculation
- `get_gemini_analysis()` - Call Gemini API for AI analysis

## 🔒 Security Features

- ✅ Secure filename handling with `werkzeug.utils.secure_filename`
- ✅ File type validation (PDF only)
- ✅ File size limits (10MB max)
- ✅ Temporary file cleanup
- ✅ Error handling for malformed PDFs
- ✅ Environment variable protection

## 🐛 Troubleshooting

### Issue: "ModuleNotFoundError"
**Solution:** Ensure virtual environment is activated and dependencies installed
```bash
pip install -r requirements.txt
```

### Issue: "GEMINI_API_KEY not found"
**Solution:** Check `.env` file has correct API key and format
```
GEMINI_API_KEY=your_actual_key_here
```

### Issue: "PDF extraction failed"
**Solution:** Ensure PDF is valid and not encrypted/password-protected

### Issue: "413 Request Entity Too Large"
**Solution:** Maximum file size is 10MB. Use smaller PDFs or split documents

## 📊 API Integration

### Google Gemini API

The application uses Google's Generative AI API for semantic analysis.

**Request:**
- Model: `gemini-pro`
- Prompt: Comparative analysis of two documents
- Max Input: ~5000 characters per document

**Response:**
- Similarity Level: Low/Moderate/High
- Detailed Explanation
- Key Overlapping Ideas

## 🔄 Workflow

```
1. User uploads 2 PDFs
   ↓
2. Extract text from both PDFs
   ↓
3. Calculate TF-IDF similarity (SKLearn)
   ↓
4. Send to Gemini API for semantic analysis
   ↓
5. Display results with recommendations
   ↓
6. Clean up temporary files
```

## 📈 Performance

- **PDF Processing:** < 2 seconds per document
- **TF-IDF Calculation:** < 1 second
- **Gemini API Call:** 2-10 seconds (depends on content length)
- **Total Processing:** ~5-15 seconds

## 🎓 Learning Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Scikit-learn TF-IDF](https://scikit-learn.org/stable/modules/feature_extraction.html#tfidf-term-weighting)
- [PyPDF2 Documentation](https://pypdf2.readthedocs.io/)
- [Google Generative AI](https://ai.google.dev/tutorials/python_quickstart)

## 📝 License

This project is open source and available for educational purposes.

## 🤝 Contributing

Feel free to fork, modify, and improve this project!

### Potential Enhancements
- [ ] Support for more file formats (DOCX, TXT)
- [ ] Batch processing of multiple documents
- [ ] Plagiarism report export (PDF/Excel)
- [ ] Database integration for history tracking
- [ ] Advanced visualization of similarity metrics
- [ ] User authentication and document management
- [ ] Custom plagiarism thresholds
- [ ] Multiple language support

## ❓ FAQ

**Q: Is my data safe?**
A: Yes! Files are processed in-memory and automatically deleted after analysis. No data is stored.

**Q: Can I analyze documents from the web?**
A: Currently, only PDF uploads are supported. Future versions may add URL support.

**Q: What's the maximum file size?**
A: Maximum 10MB per PDF file.

**Q: Do I need an API key?**
A: Yes, for Gemini AI features. TF-IDF analysis works without an API key.

**Q: How accurate is the plagiarism detection?**
A: Results combine two methods (TF-IDF + Gemini AI) for comprehensive analysis. No system is 100% accurate.

## 📞 Support

For issues or questions:
1. Check the FAQs above
2. Review error messages in the browser console
3. Check `.env` configuration
4. Ensure all dependencies are installed

---

**Built with ❤️ using Flask and Gemini AI**

Happy plagiarism checking! 🎯
