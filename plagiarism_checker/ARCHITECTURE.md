# 🏗️ Technical Architecture - AI Plagiarism Checker

## System Overview

The AI-Powered Plagiarism Checker is a full-stack web application that combines machine learning and AI to detect text plagiarism across PDF documents.

```
┌─────────────────────────────────────────────────────────────┐
│                    CLIENT LAYER (Frontend)                   │
│                     Browser (HTML/CSS/JS)                    │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                   APPLICATION LAYER (Flask)                  │
│           Routes: /, /check → file upload & processing       │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                   PROCESSING LAYER                           │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────┐   │
│  │  PDF Text    │  │  TF-IDF      │  │  Gemini AI      │   │
│  │  Extraction  │  │  Similarity  │  │  Semantic       │   │
│  │  (pdfplumber)│  │  (sklearn)   │  │  Analysis       │   │
│  └──────────────┘  └──────────────┘  └─────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                   DATA LAYER                                 │
│         .env (Config) | uploads/ (Temp files)               │
└─────────────────────────────────────────────────────────────┘
```

---

## Architecture Components

### 1. Frontend Layer

**Technologies:**
- HTML5
- Bootstrap 5 (CSS Framework)
- Vanilla JavaScript
- Responsive Design

**Key Features:**
- File upload interface with drag-and-drop (future enhancement)
- Real-time validation
- Progress indicators
- Results display with detailed analysis
- Print functionality

**Files:**
- `templates/base.html` - Base template with navigation
- `templates/index.html` - Upload page
- `templates/result.html` - Results display
- `static/style.css` - Custom styling

### 2. Application Layer (Flask Backend)

**Framework:** Flask 3.0.0

**Key Components:**

```python
app = Flask(__name__)
    │
    ├── Route: /
    │   └── index() → Display upload page
    │
    ├── Route: /check (POST)
    │   └── check() → Process PDFs and return results
    │
    └── Error Handlers
        ├── 413 → File too large
        ├── 404 → Not found
        └── 500 → Internal server error
```

**Key Functions:**
- `allowed_file()` - Validates file extensions
- `extract_text_from_pdf()` - Extracts text with fallback logic
- `preprocess_text()` - Cleans and normalizes text
- `calculate_tfidf_similarity()` - ML-based similarity
- `get_gemini_analysis()` - AI semantic analysis

### 3. Processing Layer

#### A. PDF Text Extraction

```
PDF File → pdfplumber (Primary) 
         → PyPDF2 (Fallback)
         → Extract Text
         → Clean & Return
```

**Tools:**
- **pdfplumber**: Modern, reliable PDF text extraction
- **PyPDF2**: Fallback for compatibility

**Process:**
1. Load PDF file
2. Iterate through pages
3. Extract text from each page
4. Concatenate and clean text
5. Return processed text

#### B. TF-IDF Similarity Analysis

```
Text1 + Text2 → Preprocess → Vectorize → TF-IDF Matrix
                                            ↓
                                     Cosine Similarity
                                            ↓
                                     Similarity Score (%)
```

**Algorithm:**
1. **Preprocessing:**
   - Convert to lowercase
   - Remove special characters
   - Remove extra whitespace
   
2. **Vectorization:**
   - Create TF-IDF vectors using sklearn
   - Max features: 500
   - Stop words: English
   
3. **Similarity Calculation:**
   - Compute cosine similarity
   - Scale to percentage (0-100%)
   - Round to 2 decimal places

**Formula:**
```
Similarity = (Dot Product of Vectors) / (Magnitude1 × Magnitude2)
Percentage = Similarity × 100
```

**Scikit-learn Components:**
```python
TfidfVectorizer(
    max_features=500,      # Limit features to top 500
    stop_words='english',  # Remove common words
    min_df=1,              # Min document frequency
    max_df=0.95            # Max document frequency
)
```

#### C. Gemini AI Semantic Analysis

```
Text1 + Text2 → Format Prompt → Call Gemini API
                                      ↓
                           Generate Analysis
                                      ↓
                         Parse & Extract Level
                                      ↓
                        Return Results Object
```

**API Configuration:**
- **Model:** `gemini-pro`
- **Timeout:** 30 seconds
- **Max Input:** ~5000 characters per document (token limit)
- **Response:** Detailed text analysis

**Prompt Structure:**
```
1. Context (5000 chars each)
2. Task (Analyze for plagiarism)
3. Required Output Format
4. Analysis Type (Semantic + Contextual)
```

**Response Parsing:**
- Extract similarity level (Low/Moderate/High)
- Parse detailed explanation
- Identify key overlapping ideas
- Provide recommendations

---

## Data Flow

### File Upload & Processing Flow

```
1. User Uploads Files
   ├── PDF 1 → Validate → Save → Extract Text → Process
   ├── PDF 2 → Validate → Save → Extract Text → Process
   │
2. Text Extraction
   ├── Attempt pdfplumber
   ├── Fallback to PyPDF2
   ├── Verify text length (>50 chars)
   │
3. Parallel Analysis
   ├── TF-IDF Calculation
   │   └── Return similarity %
   │
   └── Gemini Analysis
       └── Return level + explanation
   │
4. Results Compilation
   ├── Combine metrics
   ├── Generate recommendations
   │
5. Cleanup
   ├── Delete temporary files
   ├── Return results to frontend
```

### Request/Response Cycle

```
POST /check
├── Request
│   ├── pdf1 (file)
│   └── pdf2 (file)
│
├── Processing
│   ├── Validation
│   ├── Text Extraction
│   ├── Analysis (TF-IDF + Gemini)
│   └── Report Generation
│
└── Response
    └── render_template('result.html', results=...)
```

---

## Configuration Management

### Environment Variables (.env)

```env
# API Configuration
GEMINI_API_KEY=AIzaSyDx...     # Required for Gemini features

# Flask Configuration
FLASK_ENV=development           # development/production
FLASK_DEBUG=True               # Debug mode toggle
SECRET_KEY=...                 # Session encryption key
PORT=5000                      # Server port
```

### Application Configuration (config.py)

```python
class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default')
    UPLOAD_FOLDER = 'uploads'
    MAX_UPLOAD_SIZE = 10 * 1024 * 1024      # 10MB
    MAX_TEXT_LENGTH = 5000                  # For Gemini
    ALLOWED_EXTENSIONS = {'pdf'}
    PERMANENT_SESSION_LIFETIME = 3600       # 1 hour
```

---

## Error Handling Strategy

### Layer 1: Validation

```
File Upload
    ├── File exists?
    ├── Is PDF format?
    ├── Size < 10MB?
    └── Both files provided?
```

### Layer 2: Processing

```
PDF Extraction
    ├── File readable?
    ├── Extract successful?
    ├── Text length > 50 chars?
    └── Retry with fallback?
```

### Layer 3: Analysis

```
Gemini API Call
    ├── API key configured?
    ├── Connection established?
    ├── Response valid?
    └── Timeout handling?
```

### Layer 4: HTTP

```
@app.errorhandler(413)  # File too large
@app.errorhandler(404)  # Not found
@app.errorhandler(500)  # Server error
```

---

## Security Architecture

### File Security

```
Uploaded File
    ├── Validate extension
    ├── Use secure_filename()
    ├── Add timestamp to filename
    ├── Store in isolated folder
    └── Delete after processing
```

### API Security

```
API Key
    ├── Store in .env (not in code)
    ├── Load via python-dotenv
    ├── Never expose in response
    └── Use environment variables in production
```

### Session Security

```
Session Management
    ├── Secret key for signing
    ├── HTTP-only cookies
    ├── CSRF protection (future)
    └── Timeout handling
```

---

## Performance Optimization

### 1. Text Extraction Optimization

```python
# Use pdfplumber (faster) with PyPDF2 fallback
try:
    # Try pdfplumber first (modern, fast)
except:
    # Fallback to PyPDF2 (slower, compatible)
```

**Expected Times:**
- Small PDF (< 5 pages): 0.5-1 second
- Medium PDF (5-20 pages): 1-3 seconds
- Large PDF (> 20 pages): 3-5 seconds

### 2. TF-IDF Optimization

```python
TfidfVectorizer(
    max_features=500,      # Limit to top 500 features
    stop_words='english',  # Remove common words
    min_df=1,              # Minimum document frequency
    max_df=0.95            # Maximum document frequency
)
```

**Expected Time:** < 1 second

### 3. API Call Optimization

```python
# Limit text to avoid token overflow
MAX_TEXT_LENGTH = 5000  # ~1500-2000 tokens
```

**Expected Time:** 2-10 seconds (API dependent)

---

## Scalability Considerations

### Current Architecture (Single User)

```
1 Flask Process → 1 User → Sequential Processing
```

### Future Scaling Options

```
1. Load Balancing
   ├── Multiple Flask processes
   ├── Nginx reverse proxy
   └── Session management (Redis)

2. Asynchronous Processing
   ├── Celery for background jobs
   ├── Redis message queue
   └── Websocket for real-time updates

3. Database Integration
   ├── Store analysis history
   ├── User authentication
   └── Results caching

4. Microservices
   ├── PDF extraction service
   ├── Analysis service
   └── API gateway
```

---

## Technology Stack Summary

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| Web Framework | Flask | 3.0.0 | Backend routing |
| Frontend | Bootstrap 5 | 5.3.0 | UI framework |
| PDF Processing | PyPDF2/pdfplumber | 4.0.1/0.10.3 | Text extraction |
| ML Library | scikit-learn | 1.3.2 | TF-IDF analysis |
| AI API | google-generativeai | 0.3.0 | Gemini integration |
| Environment | python-dotenv | 1.0.0 | Config management |
| Server | Werkzeug | 3.0.1 | WSGI application |
| Language | Python | 3.8+ | Backend language |
| Database | None (future) | - | In-memory only |

---

## API Specifications

### Gemini API Request

```python
model = genai.GenerativeModel('gemini-pro')
response = model.generate_content(
    prompt,           # Analysis prompt
    timeout=30        # 30 second timeout
)
```

### Request Format

```
Prompt: Analyze plagiarism between texts
Input: TEXT 1 (up to 5000 chars) + TEXT 2 (up to 5000 chars)
Output: Similarity level + Detailed explanation + Overlapping ideas
```

### Response Format

```
SIMILARITY LEVEL: [Low/Moderate/High]

DETAILED ANALYSIS:
[2-3 paragraphs of analysis]

KEY OVERLAPPING IDEAS:
- [Idea 1]
- [Idea 2]
- [Idea 3]

RECOMMENDATIONS:
[Next steps based on findings]
```

---

## Deployment Architecture

### Development

```
localhost:5000 → Flask dev server → file:// ← Files
                                   ↓
                            Gemini API (cloud)
```

### Production

```
User Browser → HTTPS → Nginx (reverse proxy)
                            ↓
                      Gunicorn (4 workers)
                      Flask Application
                            ↓
                      Google Cloud APIs
```

---

## Monitoring & Logging

### Current Implementation

```python
print(f"Error message")  # Basic logging
```

### Future Enhancements

```
├── Structured Logging (json)
├── Log Levels (DEBUG, INFO, WARNING, ERROR)
├── File Rotation
├── Monitoring Dashboard
├── Error Alerts
└── Performance Metrics
```

---

## Conclusion

The AI-Powered Plagiarism Checker uses a modern, scalable architecture combining:

- **Frontend:** Responsive Bootstrap UI
- **Backend:** Flask with Python
- **Analysis:** TF-IDF ML + Gemini AI
- **Processing:** Robust PDF extraction
- **Security:** Environment-based config
- **Error Handling:** Comprehensive validation

This architecture ensures reliability, security, and ease of maintenance while providing room for future enhancements.

---

*For more information, see README.md and SETUP_GUIDE.md*
