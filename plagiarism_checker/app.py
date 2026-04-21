from flask import Flask, render_template, request, redirect, url_for
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

def preprocess_text(text):
    # Convert to lowercase and remove punctuation
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    return text

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check', methods=['POST'])
def check():
    text1 = request.form.get('text1')
    text2 = request.form.get('text2')
    
    if not text1 or not text2:
        return redirect(url_for('index'))
    
    # Preprocess texts
    processed_text1 = preprocess_text(text1)
    processed_text2 = preprocess_text(text2)
    
    # Create TF-IDF vectors
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([processed_text1, processed_text2])
    
    # Compute cosine similarity
    similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
    similarity_percentage = round(similarity * 100, 2)
    
    # Determine label
    if similarity_percentage <= 30:
        label = "Low"
    elif similarity_percentage <= 70:
        label = "Moderate"
    else:
        label = "High"
    
    return render_template('result.html', 
                         text1=text1, 
                         text2=text2, 
                         similarity=similarity_percentage, 
                         label=label)

if __name__ == '__main__':
    app.run(debug=True)