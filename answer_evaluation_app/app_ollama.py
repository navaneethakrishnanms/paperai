from flask import Flask, render_template, request, jsonify, send_file
import os
from werkzeug.utils import secure_filename
import json
import traceback
from evaluation_pipeline import AnswerEvaluationPipeline

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['RESULT_FOLDER'] = 'results'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size

# Ensure folders exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['RESULT_FOLDER'], exist_ok=True)

# Initialize pipeline (will be created on first use to save startup time)
pipeline = None
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "llama3-gpu:latest")

def get_pipeline():
    """Lazy initialization of pipeline"""
    global pipeline
    if pipeline is None:
        pipeline = AnswerEvaluationPipeline(ollama_model=OLLAMA_MODEL)
    return pipeline

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
            
            # Process question paper
            p = get_pipeline()
            questions = p.process_question_paper(filepath)
            
            return jsonify({
                'success': True, 
                'message': 'Question paper uploaded and processed successfully',
                'questions_count': len(questions),
                'questions': [
                    {
                        'number': q['question_number'],
                        'marks': q['max_marks'],
                        'text': q['question_text'][:100] + '...' if len(q['question_text']) > 100 else q['question_text']
                    } for q in questions
                ]
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
            
            # Process answer key
            p = get_pipeline()
            answers = p.process_answer_key(filepath)
            
            return jsonify({
                'success': True, 
                'message': 'Answer key uploaded and processed successfully',
                'answers_count': len(answers)
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
            
            # Get pipeline
            p = get_pipeline()
            
            # Process student answer (with OCR if needed)
            text_pdf_name = f"text_{filename}"
            text_pdf_path = os.path.join(app.config['RESULT_FOLDER'], text_pdf_name)
            p.process_student_answer(filepath, text_pdf_path, use_ocr=True)
            
            # Evaluate answers using Ollama
            print("\n🎓 Starting AI-based evaluation...")
            evaluation_result = p.evaluate_answers()
            
            # Generate result PDF
            result_filename = f"result_{filename}"
            result_path = os.path.join(app.config['RESULT_FOLDER'], result_filename)
            p.generate_result_pdf(
                evaluation_result=evaluation_result,
                output_path=result_path,
                student_name="Student"
            )
            
            # Save JSON
            json_filename = f"eval_{filename.replace('.pdf', '.json')}"
            json_path = os.path.join(app.config['RESULT_FOLDER'], json_filename)
            p.save_evaluation_json(evaluation_result, json_path)
            
            return jsonify({
                'success': True,
                'message': 'Paper evaluated successfully using AI concept matching',
                'result_file': result_filename,
                'text_pdf_file': text_pdf_name,
                'json_file': json_filename,
                'total_marks': evaluation_result['total_marks'],
                'obtained_marks': evaluation_result['obtained_marks'],
                'percentage': evaluation_result['percentage'],
                'grade': evaluation_result['grade'],
                'evaluation_method': evaluation_result.get('evaluation_method', 'Concept-Based (Ollama)'),
                'question_wise_results': evaluation_result['question_wise_results']
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
        p = get_pipeline() if pipeline else None
        status = {
            'question_paper_loaded': len(p.questions) > 0 if p else False,
            'answer_key_loaded': len(p.answer_key) > 0 if p else False,
            'pipeline_ready': pipeline is not None
        }
        return jsonify({'success': True, 'status': status})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/test_ollama')
def test_ollama():
    """Test endpoint to check if Ollama is working"""
    try:
        p = get_pipeline()
        return jsonify({
            'success': True,
            'message': 'Ollama is ready',
            'model': p.ollama_evaluator.model_name
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Ollama not available. Please install from https://ollama.ai'
        }), 500

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 AI Answer Evaluation System")
    print("="*60)
    print("📝 Features:")
    print("   - DeepSeek OCR for handwritten text extraction")
    print("   - Ollama LLM for concept-based evaluation")
    print("   - Automatic PDF report generation")
    print("="*60)
    print("🌐 Starting server on http://localhost:5000")
    print("="*60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
