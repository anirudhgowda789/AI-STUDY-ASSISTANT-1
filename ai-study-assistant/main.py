from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
from pdf import extract_text_from_pdf
from ai import generate_summary, generate_quiz

app = Flask(__name__)
# Enable CORS so the Netlify frontend can talk to this backend
CORS(app, origins=[
    'https://anixpress.online', 
    'https://www.anixpress.online', 
    'http://localhost:3000', 
    'http://localhost:5000', 
    'http://127.0.0.1:5000',
    'https://aistudyassistant420.netlify.app'
])

# Configure the upload folder
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and file.filename.endswith('.pdf'):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            # Extract text using your pdf.py module
            text = extract_text_from_pdf(filepath)
            if not text or not text.strip():
                return jsonify({'error': 'No readable text found. The PDF might be empty or a scanned image.'}), 400
            return jsonify({'text': text})
        except Exception as e:
            return jsonify({'error': f'Failed to process PDF: {str(e)}'}), 500
        finally:
            # Clean up the file after reading it to save space safely
            if os.path.exists(filepath):
                os.remove(filepath)
    
    return jsonify({'error': 'Invalid format. Please upload a PDF.'}), 400

@app.route('/process', methods=['POST'])
def process_text():
    data = request.json
    text = data.get('text', '')
    action = data.get('action', '')
    
    if not text:
        return jsonify({'error': 'No text available to process'}), 400
        
    try:
        # Route to the correct AI function based on user choice
        if action == 'summary':
            result = generate_summary(text)
        elif action == 'quiz':
            result = generate_quiz(text)
        else:
            return jsonify({'error': 'Invalid action selected'}), 400
            
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': f'AI generation failed: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)