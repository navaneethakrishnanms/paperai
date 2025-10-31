"""
Flask App with Ollama Integration and OCR-to-Text Pipeline
Complete handwritten answer evaluation system
"""

from flask import Flask, render_template, request, jsonify, send_file
import os
from werkzeug.utils import secure_filename
import traceback
from pdf_processor_ollama import PDFProcessorOllama
from ollama_evaluator import OllamaEvaluator

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['RESULT_FOLDER'] = 'results'
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB for image PDFs

# Ensure folders exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['RESULT_FOLDER'], exist_ok=True)

# Initialize components
print("\n" + "="*70)
print("🚀 INITIALIZING AI-POWERED ANSWER EVALUATION SYSTEM")
print("="*70 + "\n")

pdf_processor = PDFProcessorOllama()
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "llama3-gpu:latest")
ollama_evaluator = OllamaEvaluator(model_name=OLLAMA_MODEL)  # Change model via env if needed

print("\n✅ System initialized successfully!")
print("="*70 + "\n")

# In-memory storage for questions and answers
questions_storage = []
answer_key_storage = []

ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload_question_paper', methods=['POST'])
def upload_question_paper():
    """Upload and process question paper"""
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
            
            print(f"\n📥 Processing question paper: {filename}")
            
            # Extract questions with marks
            global questions_storage
            questions_storage = pdf_processor.extract_questions_with_marks(filepath)
            
            if not questions_storage:
                return jsonify({
                    'success': False, 
                    'error': 'No questions found in the uploaded PDF. Please check the format.'
                }), 400
            
            return jsonify({
                'success': True, 
                'message': f'Question paper uploaded successfully! Found {len(questions_storage)} questions.',
                'questions_count': len(questions_storage),
                'questions': [{'number': q['question_number'], 'marks': q['max_marks']} for q in questions_storage]
            })
        
        return jsonify({'success': False, 'error': 'Invalid file format. Only PDF allowed'}), 400
    
    except Exception as e:
        print(f"❌ Error uploading question paper: {str(e)}")
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/upload_answer_key', methods=['POST'])
def upload_answer_key():
    """Upload and process answer key"""
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
            
            print(f"\n📥 Processing answer key: {filename}")
            
            # Extract answers
            global answer_key_storage
            answer_key_storage = pdf_processor.extract_answers(filepath)
            
            if not answer_key_storage:
                return jsonify({
                    'success': False, 
                    'error': 'No answers found in the uploaded PDF. Please check the format.'
                }), 400
            
            return jsonify({
                'success': True, 
                'message': f'Answer key uploaded successfully! Found {len(answer_key_storage)} answers.',
                'answers_count': len(answer_key_storage)
            })
        
        return jsonify({'success': False, 'error': 'Invalid file format. Only PDF allowed'}), 400
    
    except Exception as e:
        print(f"❌ Error uploading answer key: {str(e)}")
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/evaluate_student_paper', methods=['POST'])
def evaluate_student_paper():
    """Evaluate student's handwritten answer paper using Ollama"""
    try:
        # Check if question paper and answer key are uploaded
        if not questions_storage:
            return jsonify({
                'success': False, 
                'error': 'Please upload question paper first'
            }), 400
        
        if not answer_key_storage:
            return jsonify({
                'success': False, 
                'error': 'Please upload answer key first'
            }), 400
        
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'}), 400
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'student_' + filename)
            file.save(filepath)
            
            print(f"\n📥 Processing student paper: {filename}")
            
            # STEP 1: Extract student answers (OCR -> Text PDF -> Extract)
            print("\n" + "="*70)
            print("STEP 1: EXTRACTING STUDENT ANSWERS")
            print("="*70)
            student_answers = pdf_processor.extract_student_answers(filepath)
            
            if not student_answers:
                return jsonify({
                    'success': False, 
                    'error': 'Could not extract answers from student paper. Please ensure the handwriting is clear.'
                }), 400
            
            print(f"✅ Extracted {len(student_answers)} student answers\n")
            
            # STEP 2: Evaluate using Ollama
            print("="*70)
            print("STEP 2: EVALUATING WITH OLLAMA LLM (CONCEPT-BASED)")
            print("="*70 + "\n")
            
            evaluation_result = ollama_evaluator.evaluate_all_answers(
                questions=questions_storage,
                answer_key=answer_key_storage,
                student_answers=student_answers
            )
            
            # STEP 3: Generate result PDF
            print("="*70)
            print("STEP 3: GENERATING RESULT PDF")
            print("="*70 + "\n")
            
            result_filename = f"result_{filename}"
            result_path = os.path.join(app.config['RESULT_FOLDER'], result_filename)
            pdf_processor.generate_result_pdf(evaluation_result, result_path)
            
            print("\n" + "="*70)
            print("✅ EVALUATION COMPLETE!")
            print("="*70 + "\n")
            
            # Prepare response
            question_wise_results = []
            for q_result in evaluation_result['question_wise_results']:
                question_wise_results.append({
                    'question_number': q_result['Question_Number'],
                    'max_marks': q_result['Max_Marks'],
                    'marks_obtained': q_result['Awarded_Marks'],
                    'concept_match': f"{q_result['Concept_Match_Score']*100:.1f}%",
                    'feedback': q_result['Feedback']
                })
            
            return jsonify({
                'success': True,
                'message': 'Student paper evaluated successfully!',
                'result_file': result_filename,
                'total_marks': evaluation_result['total_marks'],
                'obtained_marks': evaluation_result['obtained_marks'],
                'percentage': evaluation_result['percentage'],
                'grade': evaluation_result['grade'],
                'question_wise_marks': question_wise_results
            })
        
        return jsonify({'success': False, 'error': 'Invalid file format. Only PDF allowed'}), 400
    
    except Exception as e:
        print(f"\n❌ Error evaluating student paper: {str(e)}")
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/download_result/<filename>')
def download_result(filename):
    """Download the result PDF"""
    try:
        result_path = os.path.join(app.config['RESULT_FOLDER'], filename)
        if os.path.exists(result_path):
            return send_file(result_path, as_attachment=True)
        return jsonify({'success': False, 'error': 'Result file not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/get_status')
def get_status():
    """Get system status"""
    try:
        status = {
            'question_paper_loaded': len(questions_storage) > 0,
            'answer_key_loaded': len(answer_key_storage) > 0,
            'questions_count': len(questions_storage),
            'answers_count': len(answer_key_storage),
            'ollama_model': ollama_evaluator.model_name
        }
        return jsonify({'success': True, 'status': status})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    print("\n" + "="*70)
    print("🌐 Starting Flask Server")
    print("="*70)
    print("📡 Access the app at: http://localhost:5000")
    print("="*70 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
