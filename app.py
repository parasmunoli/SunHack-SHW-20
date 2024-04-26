from flask import Flask, request, jsonify
import PyPDF2
from collections import Counter
import math
import os
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

def extract_text_from_pdf(pdf_file_path):
    with open(pdf_file_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        extracted_text_list = []
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            extracted_text_list.append(page.extract_text())
    return ' '.join(extracted_text_list)

def cosine_similarity(s1, s2):
    words1 = s1.split()
    words2 = s2.split()
    all_words = set(words1 + words2)
    vec1 = Counter(words1)
    vec2 = Counter(words2)
    dot_product = sum(vec1[word] * vec2[word] for word in all_words)
    magnitude1 = math.sqrt(sum(vec1[word] ** 2 for word in all_words))
    magnitude2 = math.sqrt(sum(vec2[word] ** 2 for word in all_words))
    if magnitude1 == 0 or magnitude2 == 0:
        return 0
    else:
        return dot_product / (magnitude1 * magnitude2)

@app.route('/analyze_resume', methods=['POST'])
def analyze_resume():
    job_description = request.form['job_description']
    resume_pdf = request.files['resume']
    
    # Save the resume PDF to a temporary file
    resume_pdf_path = 'resume_pdf'
    resume_pdf.save(resume_pdf_path)
    
    # Extract text from the resume PDF
    resume_text = extract_text_from_pdf(resume_pdf_path)
    
    # Calculate similarity between job description and resume
    similarity_score = cosine_similarity(job_description, resume_text)
    
    # Delete the temporary resume file
    os.remove(resume_pdf_path)
    
    return jsonify({'similarity_score': similarity_score})

if __name__ == '__main__':
    app.run(debug=True, port=5001)
