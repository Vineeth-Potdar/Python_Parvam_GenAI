# 🔍 AI-Powered Plagiarism Checker

A modern Flask-based web application that detects plagiarism using a **hybrid approach** combining **TF-IDF (statistical similarity)** and **Google Gemini AI (semantic analysis)** with a weighted final score.

---

## 📋 Features

✅ **PDF File Upload** - Upload two PDF documents for comparison
✅ **TF-IDF Analysis** - Statistical similarity detection using NLP
✅ **Gemini AI (Flash Model)** - Advanced semantic plagiarism detection
✅ **Weighted Final Score** - Combines TF-IDF and AI (90% AI weight)
✅ **Web-Assisted Verification** - Generate Google search queries for manual checking
✅ **Modern UI** - Responsive Bootstrap 5 interface
✅ **Detailed Reports** - Explanation of similarities and overlapping ideas
✅ **Print Support** - Export results easily

---

## 🧠 How It Works

This system uses **two complementary methods**:

### 1. TF-IDF (Lexical Similarity)

* Measures word overlap and frequency
* Uses:

  * Word n-grams
  * Character n-grams
* Good for detecting direct copying

### 2. Gemini AI (Semantic Similarity)

* Understands meaning and context
* Detects:

  * Paraphrasing
  * Reworded plagiarism
  * Structural similarity

---

## 🎯 Final Score Calculation

The final plagiarism score is calculated using a weighted approach:

```python
final_score = (tfidf_score * 0.1) + (gemini_score * 0.9)
```

### Gemini Score Mapping:

| Level    | Score |
| -------- | ----- |
| High     | 95    |
| Moderate | 65    |
| Low      | 30    |

👉 **AI is prioritized**, making the system more accurate for real-world plagiarism detection.

---

## 📊 Result Interpretation

| Final Score | Meaning             |
| ----------- | ------------------- |
| 0 – 50%     | Low similarity      |
| 50 – 75%    | Moderate similarity |
| 75 – 100%   | High plagiarism     |

---

## 🌐 Web-Assisted Verification

The system also:

* Extracts key sentences
* Generates a **Google search query**
* Allows users to manually verify sources

⚠️ Note: This is for **manual verification**, not automatic web plagiarism detection.

---

## 🏗️ Project Structure

```
plagiarism_checker/
├── app.py
├── requirements.txt
├── .env
├── templates/
│   ├── base.html
│   ├── index.html
│   └── result.html
├── static/
│   └── style.css
└── uploads/
```

---

## 📦 Requirements

* Python 3.8+
* Flask
* scikit-learn
* pdfplumber
* PyPDF2
* python-dotenv
* google-genai

---

## 🚀 Setup Instructions

### 1. Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Add API Key

Create `.env` file:

```env
GEMINI_API_KEY=your_api_key_here
```

⚠️ Do NOT hardcode your API key in code.

---

### 4. Run the App

```bash
python app.py
```

Open:

```
http://127.0.0.1:5000
```

---

## 🔧 Backend Workflow

```
1. Upload PDFs
2. Extract text
3. Preprocess text
4. Compute TF-IDF similarity
5. Perform Gemini AI analysis
6. Combine scores (weighted)
7. Display results
8. Provide web verification
```

---

## ⚙️ Key Functions

* `extract_text_from_pdf()`
* `preprocess_text()`
* `calculate_tfidf_similarity()`
* `get_gemini_analysis()`
* `combine_scores()`
* `extract_query()`
* `generate_search_links()`

---

## 🔒 Security

* Secure file handling
* File size limits
* Environment-based API keys
* Temporary file cleanup

---

## 🧪 Test Cases

### ✔ High Similarity

* Near identical content
  → Result: HIGH

### ✔ Moderate Similarity

* Paraphrased content
  → Result: MODERATE

### ✔ Low Similarity

* Different topics
  → Result: LOW

---

## 🎤 Viva Explanation (Important)

> “The system combines lexical similarity (TF-IDF) and semantic similarity (Gemini AI). The final score prioritizes AI analysis, making it more reliable for detecting paraphrased plagiarism.”

---

## ⚠️ Limitations

* TF-IDF may give false positives due to common words
* AI responses depend on API availability
* No automatic web plagiarism detection (manual verification only)

---

## 🚀 Future Improvements

* Highlight matching text sections
* Multi-document comparison
* DOCX/TXT support
* Database storage
* User authentication

---

## 📝 License

Educational use only.

---

**Built using Flask + Gemini AI 🚀**


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
