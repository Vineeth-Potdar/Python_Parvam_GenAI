import os
import re
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import PyPDF2
import pdfplumber
from google import genai
from dotenv import load_dotenv
from config import config

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
# Initialize Flask app with config
app = Flask(__name__)
env = os.getenv('FLASK_ENV', 'development')
app.config.from_object(config[env])

# Create uploads folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
app.config['MAX_CONTENT_LENGTH'] = app.config['MAX_UPLOAD_SIZE']

# Configure Gemini API
client = None
if GEMINI_API_KEY:
    client = genai.Client(api_key=GEMINI_API_KEY)

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF file using pdfplumber with PyPDF2 fallback"""
    try:
        text = ""
        # Try using pdfplumber first (more reliable for modern PDFs)
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + " "
        except Exception as e:
            print(f"pdfplumber failed: {e}, trying PyPDF2...")
            # Fallback to PyPDF2
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page_num, page in enumerate(pdf_reader.pages):
                    try:
                        page_text = page.extract_text()
                        if page_text:
                            text += page_text + " "
                    except Exception as e:
                        print(f"Error reading page {page_num}: {e}")
                        continue
        
        return text.strip()
    except Exception as e:
        raise Exception(f"Failed to extract text from PDF: {str(e)}")

def preprocess_text(text):
    text = text.lower()

    # remove special chars
    text = re.sub(r'[^\w\s]', '', text)

    # normalize spaces
    text = re.sub(r'\s+', ' ', text).strip()

    return text

def calculate_tfidf_similarity(text1, text2):
    try:
        processed_text1 = preprocess_text(text1)
        processed_text2 = preprocess_text(text2)

        if not processed_text1 or not processed_text2:
            return 0.0

        # WORD TF-IDF
        word_vectorizer = TfidfVectorizer(
            max_features=3000,
            ngram_range=(1, 2),
            stop_words=None,
            lowercase=True
        )

        word_matrix = word_vectorizer.fit_transform([processed_text1, processed_text2])
        word_sim = cosine_similarity(word_matrix[0], word_matrix[1])[0][0]

        # CHAR TF-IDF
        char_vectorizer = TfidfVectorizer(
            analyzer='char',
            ngram_range=(3, 5)
        )

        char_matrix = char_vectorizer.fit_transform([processed_text1, processed_text2])
        char_sim = cosine_similarity(char_matrix[0], char_matrix[1])[0][0]

        # FINAL TF-IDF SCORE ONLY
        final_tfidf = (word_sim * 0.7 + char_sim * 0.3) * 100

        return round(final_tfidf, 2)

    except Exception as e:
        print(f"Error calculating TF-IDF similarity: {e}")
        return 0.0
    
def combine_scores(tfidf_score, gemini_level):
    # Convert Gemini level to numeric
    if gemini_level == "High":
        gemini_score = 80
    elif gemini_level == "Moderate":
        gemini_score = 50
    elif gemini_level == "Low":
        gemini_score = 20
    else:
        gemini_score = 0

    # Weighted combination
    final_score = (tfidf_score * 0.2) + (gemini_score * 0.8)

    return round(final_score, 2)

def get_gemini_analysis(text1, text2):
    """Get plagiarism analysis from Gemini API"""
    if not client:
        return {
            'level': 'N/A',
            'explanation': 'Gemini API key not configured.',
            'overlapping_ideas': 'API not available'
        }

    try:
        # Limit text size (VERY important)
        max_length = 3000
        text1_limited = text1[:max_length]
        text2_limited = text2[:max_length]

        prompt = f"""
Compare the following two texts and analyze plagiarism.

TEXT 1:
{text1_limited}

TEXT 2:
{text2_limited}

Give:
1. Similarity Level (Low / Moderate / High)
2. Short explanation (3-4 lines)
3. Key overlapping ideas (bullet points)
"""

        # ✅ NEW Gemini API call
        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=prompt
        )

        analysis_text = response.text

        # Simple level detection
        level = "Moderate"
        text_lower = analysis_text.lower()

        if "high" in text_lower:
            level = "High"
        elif "low" in text_lower:
            level = "Low"

        return {
            'level': level,
            'explanation': analysis_text,
            'overlapping_ideas': 'See explanation above'
        }

    except Exception as e:
        print("Gemini Error:", str(e))  # Debug in terminal

        return {
            'level': 'Unavailable',
            'explanation': 'AI analysis currently unavailable. Please try again.',
            'overlapping_ideas': 'N/A'
        }

@app.route('/')
def index():
    """Upload page"""
    return render_template('index.html')

@app.route('/check', methods=['POST'])
def check():
    """Process PDF uploads and perform plagiarism check"""
    try:
        # Check if files are in request
        if 'pdf1' not in request.files or 'pdf2' not in request.files:
            flash('Please upload both PDF files', 'error')
            return redirect(url_for('index'))
        
        pdf1 = request.files['pdf1']
        pdf2 = request.files['pdf2']
        
        # Check if files are selected
        if pdf1.filename == '' or pdf2.filename == '':
            flash('Please select both PDF files', 'error')
            return redirect(url_for('index'))
        
        # Check if files are PDFs
        if not (allowed_file(pdf1.filename) and allowed_file(pdf2.filename)):
            flash('Only PDF files are allowed', 'error')
            return redirect(url_for('index'))
        
        # Save uploaded files temporarily
        filename1 = secure_filename(pdf1.filename)
        filename2 = secure_filename(pdf2.filename)
        
        # Add timestamp to avoid name conflicts
        import time
        timestamp = int(time.time() * 1000)
        filename1 = f"{timestamp}_1_{filename1}"
        filename2 = f"{timestamp}_2_{filename2}"
        
        filepath1 = os.path.join(app.config['UPLOAD_FOLDER'], filename1)
        filepath2 = os.path.join(app.config['UPLOAD_FOLDER'], filename2)
        
        pdf1.save(filepath1)
        pdf2.save(filepath2)
        
        try:
            # Extract text from PDFs
            text1 = extract_text_from_pdf(filepath1)
            text2 = extract_text_from_pdf(filepath2)
            
            if not text1 or not text2:
                flash('Could not extract text from one or both PDFs. Please ensure PDFs contain extractable text.', 'error')
                return redirect(url_for('index'))
            
            # Check if extracted text is too short
            if len(text1.strip()) < 50 or len(text2.strip()) < 50:
                flash('Extracted text is too short for accurate analysis. Please use PDFs with more content.', 'error')
                return redirect(url_for('index'))
            
            # Calculate TF-IDF similarity
            tfidf_similarity = calculate_tfidf_similarity(text1, text2)
            
            # Get Gemini analysis
            gemini_analysis = get_gemini_analysis(text1, text2)
            
            final_similarity = combine_scores(tfidf_similarity, gemini_analysis['level'])
            # Clean up uploaded files
            try:
                os.remove(filepath1)
                os.remove(filepath2)
            except Exception as e:
                print(f"Warning: Could not delete temporary files: {e}")
            
            # Prepare data for results page
            results = {
                'final_similarity': final_similarity,
                'tfidf_similarity': tfidf_similarity,
                'gemini_level': gemini_analysis['level'],
                'gemini_explanation': gemini_analysis['explanation'],
                'overlapping_ideas': gemini_analysis['overlapping_ideas'],
                'text1_preview': text1[:500] + '...' if len(text1) > 500 else text1,
                'text2_preview': text2[:500] + '...' if len(text2) > 500 else text2,
                'pdf1_name': pdf1.filename,
                'pdf2_name': pdf2.filename,
                'text1_length': len(text1),
                'text2_length': len(text2)
            }
            
            return render_template('result.html', results=results)
        
        except Exception as e:
            flash(f'Error processing PDFs: {str(e)}', 'error')
            # Clean up files
            try:
                if os.path.exists(filepath1):
                    os.remove(filepath1)
                if os.path.exists(filepath2):
                    os.remove(filepath2)
            except:
                pass
            return redirect(url_for('index'))
    
    except Exception as e:
        flash(f'An unexpected error occurred: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.errorhandler(413)
def request_entity_too_large(error):
    """Handle file too large error"""
    flash('File size exceeds maximum allowed size (10MB)', 'error')
    return redirect(url_for('index')), 413

@app.errorhandler(500)
def internal_error(error):
    """Handle internal server error"""
    flash('An internal server error occurred. Please try again.', 'error')
    return redirect(url_for('index')), 500

@app.errorhandler(404)
def not_found_error(error):
    """Handle 404 error"""
    return redirect(url_for('index')), 404

if __name__ == '__main__':
    # Run Flask app
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'False') == 'True'
    app.run(debug=debug, port=port, host='0.0.0.0')