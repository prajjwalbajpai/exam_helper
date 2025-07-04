import os
import shutil
from flask import Flask, request, render_template, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS
from llm_utils.pipeline import get_answers, get_imp_topics

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'pptx'}

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/process', methods=['POST'])
def process():
    try:
        files = request.files.getlist('documents')
        saved_files = []
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(path)
                saved_files.append(path)

        questions_raw = request.form.get('questions', '')
        questions = [q.strip() for q in questions_raw.strip().split('\n') if q.strip()]
        
        answers = [f"{q} <br> {get_answers(q)} " for q in questions]  
        answer = ""
        for ans in answers: answer+=ans

        shutil.rmtree(UPLOAD_FOLDER)
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        summary = get_imp_topics(answer)
        return jsonify({'answers': answers, 'summary': summary})

    except Exception as e:
        shutil.rmtree(UPLOAD_FOLDER)
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        return jsonify({'error': str(e)}), 500
