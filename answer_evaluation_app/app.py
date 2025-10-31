from flask import Flask, render_template, request, jsonify, send_file
import os
from werkzeug.utils import secure_filename
import json
from pdf_processor_fast import PDFProcessor  # Using FAST version
from vector_db_manager import VectorDBManager
from answer_evaluator import AnswerEvaluator
import traceback

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['RESULT_FOLDER'] = 'results'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size

# Ensure folders exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['RESULT_FOLDER'], exist_ok=True)
os.makedirs('vector_db', exist_ok=True)

# Initialize components
pdf_processor = PDFProcessor()
vector_db = VectorDBManager()
evaluator = AnswerEvaluator(vector_db)

ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload_question_paper', methods=['POST'])
def upload_question_paper():
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'}), 400
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'question_paper_' + filename)
            file.save(filepath)
            
            # Process and extract questions with marks
            questions_data = pdf_processor.extract_questions_with_marks(filepath)
            
            # Store in vector DB
            vector_db.store_question_paper(questions_data)
            
            return jsonify({
                'success': True, 
                'message': 'Question paper uploaded and processed successfully',
                'questions_count': len(questions_data)
            })
        
        return jsonify({'success': False, 'error': 'Invalid file format. Only PDF allowed'}), 400
    
    except Exception as e:
        print(f"Error uploading question paper: {str(e)}")
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/upload_answer_key', methods=['POST'])
def upload_answer_key():
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'}), 400
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'answer_key_' + filename)
            file.save(filepath)
            
            # Process and extract answers
            answers_data = pdf_processor.extract_answers(filepath)
            
            # Store in vector DB
            vector_db.store_answer_key(answers_data)
            
            return jsonify({
                'success': True, 
                'message': 'Answer key uploaded and processed successfully',
                'answers_count': len(answers_data)
            })
        
        return jsonify({'success': False, 'error': 'Invalid file format. Only PDF allowed'}), 400
    
    except Exception as e:
        print(f"Error uploading answer key: {str(e)}")
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/evaluate_student_paper', methods=['POST'])
def evaluate_student_paper():
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'}), 400
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'student_' + filename)
            file.save(filepath)
            
            # Extract student answers from handwritten paper
            student_answers = pdf_processor.extract_student_answers(filepath)
            
            # Evaluate against answer key
            evaluation_result = evaluator.evaluate_answers(student_answers)
            
            # Generate result PDF
            result_filename = f"result_{filename}"
            result_path = os.path.join(app.config['RESULT_FOLDER'], result_filename)
            pdf_processor.generate_result_pdf(evaluation_result, result_path)
            
            return jsonify({
                'success': True,
                'message': 'Paper evaluated successfully',
                'result_file': result_filename,
                'total_marks': evaluation_result['total_marks'],
                'obtained_marks': evaluation_result['obtained_marks'],
                'percentage': evaluation_result['percentage'],
                'question_wise_marks': evaluation_result['question_wise_marks']
            })
        
        return jsonify({'success': False, 'error': 'Invalid file format. Only PDF allowed'}), 400
    
    except Exception as e:
        print(f"Error evaluating student paper: {str(e)}")
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/download_result/<filename>')
def download_result(filename):
    try:
        result_path = os.path.join(app.config['RESULT_FOLDER'], filename)
        if os.path.exists(result_path):
            return send_file(result_path, as_attachment=True)
        return jsonify({'success': False, 'error': 'Result file not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/get_status')
def get_status():
    try:
        status = {
            'question_paper_loaded': vector_db.has_question_paper(),
            'answer_key_loaded': vector_db.has_answer_key()
        }
        return jsonify({'success': True, 'status': status})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
