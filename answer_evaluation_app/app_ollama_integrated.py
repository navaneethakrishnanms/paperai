"""
Flask Application for Answer Evaluation with Ollama Integration
Combines DeepSeek-OCR for handwritten text extraction with Ollama LLM for concept-based evaluation
"""

from flask import Flask, render_template, request, jsonify, send_file
import os
from werkzeug.utils import secure_filename
import json
from pdf_processor import PDFProcessor
from vector_db_manager import VectorDBManager
from ollama_evaluator import OllamaEvaluator
from pdf_generator import ResultPDFGenerator, OCRtoPDFConverter
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
print("🔧 Initializing components...")
pdf_processor = PDFProcessor(use_deepseek=True)  # Enable DeepSeek-OCR
vector_db = VectorDBManager()

# Initialize Ollama evaluator with desired model
# Default to environment variable OLLAMA_MODEL or llama3-gpu:latest
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "llama3-gpu:latest")
try:
    ollama_evaluator = OllamaEvaluator(model_name=OLLAMA_MODEL)
    print("✅ Ollama evaluator initialized")
except Exception as e:
    print(f"⚠️ Warning: Ollama not available: {e}")
    print("   Please install Ollama from https://ollama.ai")
    ollama_evaluator = None

result_pdf_generator = ResultPDFGenerator()
ocr_pdf_converter = OCRtoPDFConverter()

ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload_question_paper', methods=['POST'])
def upload_question_paper():
    """Upload and process question paper PDF"""
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
            
            print(f"\n{'='*60}")
            print(f"📋 Processing Question Paper: {filename}")
            print(f"{'='*60}")
            
            # Extract questions with marks using DeepSeek-OCR if needed
            questions_data = pdf_processor.extract_questions_with_marks(filepath)
            
            if not questions_data:
                return jsonify({
                    'success': False, 
                    'error': 'No questions found in PDF. Please check the format.'
                }), 400
            
            # Store in vector DB
            vector_db.store_question_paper(questions_data)
            
            print(f"✅ Question paper processed successfully")
            print(f"   Total questions: {len(questions_data)}")
            print(f"   Total marks: {sum(q['max_marks'] for q in questions_data)}")
            
            return jsonify({
                'success': True, 
                'message': 'Question paper uploaded and processed successfully',
                'questions_count': len(questions_data),
                'total_marks': sum(q['max_marks'] for q in questions_data),
                'questions': [
                    {
                        'number': q['question_number'],
                        'marks': q['max_marks'],
                        'preview': q['question_text'][:100] + '...' if len(q['question_text']) > 100 else q['question_text']
                    }
                    for q in questions_data
                ]
            })
        
        return jsonify({'success': False, 'error': 'Invalid file format. Only PDF allowed'}), 400
    
    except Exception as e:
        print(f"❌ Error uploading question paper: {str(e)}")
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/upload_answer_key', methods=['POST'])
def upload_answer_key():
    """Upload and process answer key PDF"""
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
            
            print(f"\n{'='*60}")
            print(f"✅ Processing Answer Key: {filename}")
            print(f"{'='*60}")
            
            # Extract answers using DeepSeek-OCR if needed
            answers_data = pdf_processor.extract_answers(filepath)
            
            if not answers_data:
                return jsonify({
                    'success': False, 
                    'error': 'No answers found in PDF. Please check the format.'
                }), 400
            
            # Store in vector DB
            vector_db.store_answer_key(answers_data)
            
            print(f"✅ Answer key processed successfully")
            print(f"   Total answers: {len(answers_data)}")
            
            return jsonify({
                'success': True, 
                'message': 'Answer key uploaded and processed successfully',
                'answers_count': len(answers_data),
                'answers': [
                    {
                        'number': a['question_number'],
                        'preview': a['answer_text'][:100] + '...' if len(a['answer_text']) > 100 else a['answer_text']
                    }
                    for a in answers_data
                ]
            })
        
        return jsonify({'success': False, 'error': 'Invalid file format. Only PDF allowed'}), 400
    
    except Exception as e:
        print(f"❌ Error uploading answer key: {str(e)}")
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/evaluate_student_paper', methods=['POST'])
def evaluate_student_paper():
    """Evaluate student's handwritten answer paper using Ollama LLM"""
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'}), 400
        
        # Get student name from form (optional)
        student_name = request.form.get('student_name', 'Student')
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'student_' + filename)
            file.save(filepath)
            
            print(f"\n{'='*60}")
            print(f"📝 Evaluating Student Paper: {filename}")
            print(f"   Student: {student_name}")
            print(f"{'='*60}\n")
            
            # Step 1: Extract handwritten text using DeepSeek-OCR
            print("🔍 Step 1: Extracting handwritten text using DeepSeek-OCR...")
            extracted_text = pdf_processor.deepseek_ocr.extract_text_from_pdf(filepath)

            # Clean the extracted text and check actual content (remove XML tags, normalize whitespace)
            import re
            cleaned_text = re.sub(r'<[^>]+>', '', extracted_text) if extracted_text else ""
            cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()
            
            print(f"📝 OCR extracted {len(cleaned_text)} characters of text")
            print(f"📝 Preview: {cleaned_text[:300]}...")

            # Only fail if we have almost nothing
            if not cleaned_text or len(cleaned_text) < 20:
                return jsonify({
                    'success': False,
                    'error': f'Failed to extract sufficient text from PDF (only {len(cleaned_text)} chars). Please ensure the PDF contains clear, readable content.'
                }), 400
            
            # Step 2: Convert OCR text to searchable PDF (optional but useful)
            print("📄 Step 2: Creating searchable PDF from OCR text...")
            ocr_pdf_path = os.path.join(
                app.config['UPLOAD_FOLDER'], 
                f'student_ocr_{filename}'
            )
            ocr_pdf_converter.create_text_pdf(
                extracted_text=extracted_text,
                output_path=ocr_pdf_path,
                title=f"Student Answer Sheet - {student_name} (OCR Extracted)"
            )
            
            # Step 3: Parse student answers from extracted text
            print("📋 Step 3: Parsing student answers from extracted text...")
            student_answers = pdf_processor.extract_student_answers(extracted_text)

            # Fallback: try parsing directly from PDF if needed
            if not student_answers:
                print("⚠️ No answers detected from OCR text. Retrying using PDF path...")
                student_answers = pdf_processor.extract_student_answers(filepath)
            
            if not student_answers:
                return jsonify({
                    'success': False,
                    'error': 'No student answers detected. Please make sure answers are clearly numbered or separated.'
                }), 400
            
            print(f"✅ Found {len(student_answers)} student answers")
            
            # Step 4: Check if question paper and answer key are loaded
            questions = vector_db.get_all_questions()
            answer_key = vector_db.get_all_answers()
            
            if not questions:
                return jsonify({
                    'success': False,
                    'error': 'No question paper loaded. Please upload question paper first.'
                }), 400
            
            if not answer_key:
                return jsonify({
                    'success': False,
                    'error': 'No answer key loaded. Please upload answer key first.'
                }), 400
            
            # Step 5: Evaluate using Ollama LLM (concept-based evaluation)
            if ollama_evaluator:
                print("🧠 Step 4: Evaluating answers using Ollama LLM (concept-based)...")
                evaluation_result = ollama_evaluator.evaluate_all_answers(
                    questions=questions,
                    answer_key=answer_key,
                    student_answers=student_answers
                )
            else:
                return jsonify({
                    'success': False,
                    'error': 'Ollama not available. Please install Ollama from https://ollama.ai'
                }), 500
            
            # Step 6: Generate result PDF
            print("📊 Step 5: Generating detailed result PDF...")
            result_filename = f"result_{student_name.replace(' ', '_')}_{filename}"
            result_path = os.path.join(app.config['RESULT_FOLDER'], result_filename)
            
            result_pdf_generator.generate_result_pdf(
                evaluation_result=evaluation_result,
                student_name=student_name,
                output_path=result_path
            )
            
            print(f"\n{'='*60}")
            print(f"✅ Evaluation Complete!")
            print(f"{'='*60}")
            print(f"Student: {student_name}")
            print(f"Marks: {evaluation_result['obtained_marks']:.2f}/{evaluation_result['total_marks']}")
            print(f"Percentage: {evaluation_result['percentage']:.2f}%")
            print(f"Grade: {evaluation_result['grade']}")
            print(f"Result PDF: {result_filename}")
            print(f"{'='*60}\n")
            
            # Prepare response with question-wise details
            question_wise_summary = []
            for result in evaluation_result['question_wise_results']:
                question_wise_summary.append({
                    'question_number': result['Question_Number'],
                    'max_marks': result['Max_Marks'],
                    'obtained_marks': result['Awarded_Marks'],
                    'concept_match_score': result['Concept_Match_Score'],
                    'feedback': result['Feedback']
                })
            
            return jsonify({
                'success': True,
                'message': 'Paper evaluated successfully using AI concept analysis',
                'result_file': result_filename,
                'ocr_pdf_file': f'student_ocr_{filename}',
                'student_name': student_name,
                'total_marks': evaluation_result['total_marks'],
                'obtained_marks': evaluation_result['obtained_marks'],
                'percentage': evaluation_result['percentage'],
                'grade': evaluation_result['grade'],
                'evaluation_method': evaluation_result['evaluation_method'],
                'question_wise_summary': question_wise_summary
            })
        
        return jsonify({'success': False, 'error': 'Invalid file format. Only PDF allowed'}), 400
    
    except Exception as e:
        print(f"❌ Error evaluating student paper: {str(e)}")
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/download_result/<filename>')
def download_result(filename):
    """Download result PDF"""
    try:
        result_path = os.path.join(app.config['RESULT_FOLDER'], filename)
        if os.path.exists(result_path):
            return send_file(result_path, as_attachment=True)
        return jsonify({'success': False, 'error': 'Result file not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/download_ocr_pdf/<filename>')
def download_ocr_pdf(filename):
    """Download OCR-extracted text PDF"""
    try:
        ocr_pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(ocr_pdf_path):
            return send_file(ocr_pdf_path, as_attachment=True)
        return jsonify({'success': False, 'error': 'OCR PDF not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/get_status')
def get_status():
    """Get system status"""
    try:
        status = {
            'question_paper_loaded': vector_db.has_question_paper(),
            'answer_key_loaded': vector_db.has_answer_key(),
            'ollama_available': ollama_evaluator is not None,
            'deepseek_available': pdf_processor.deepseek_ocr is not None,
            'questions_count': len(vector_db.get_all_questions()) if vector_db.has_question_paper() else 0,
            'answers_count': len(vector_db.get_all_answers()) if vector_db.has_answer_key() else 0
        }
        return jsonify({'success': True, 'status': status})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/reset_database', methods=['POST'])
def reset_database():
    """Clear all data from vector database"""
    try:
        vector_db.clear_all_data()
        return jsonify({
            'success': True, 
            'message': 'Database cleared successfully'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 AI-Powered Answer Evaluation System")
    print("="*60)
    print("📝 Features:")
    print("  ✓ DeepSeek-OCR for handwritten text extraction")
    print("  ✓ Ollama LLM for concept-based evaluation")
    print("  ✓ Automated question & answer key processing")
    print("  ✓ Detailed PDF reports with feedback")
    print("="*60)
    print("🌐 Server starting on http://localhost:5000")
    print("="*60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
