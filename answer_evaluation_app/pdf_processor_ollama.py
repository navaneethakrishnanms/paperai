"""
Enhanced PDF Processor with Ollama Integration
Handles handwritten PDFs by converting to text-based PDF first
"""

import PyPDF2
import re
from PIL import Image
import io
import os
from datetime import datetime
from ocr_to_text_pdf_converter import get_converter

try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
    from reportlab.lib.units import inch
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False
    print("⚠️ reportlab not available - PDF generation will be limited")


class PDFProcessorOllama:
    """Enhanced PDF Processor that converts handwritten PDFs to text-based PDFs"""
    
    def __init__(self):
        if REPORTLAB_AVAILABLE:
            self.styles = getSampleStyleSheet()
        else:
            self.styles = None
        
        self.ocr_converter = get_converter()
        print("✅ PDF Processor initialized with OCR-to-Text conversion")
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text from PDF using PyPDF2"""
        try:
            text = ""
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
            return text
        except Exception as e:
            print(f"Error extracting text from PDF: {str(e)}")
            return ""
    
    def extract_questions_with_marks(self, pdf_path: str):
        """Extract questions from question paper with their marks"""
        print(f"\n{'='*70}")
        print(f"📋 EXTRACTING QUESTIONS FROM QUESTION PAPER")
        print(f"{'='*70}\n")
        
        # Try regular text extraction first
        text = self.extract_text_from_pdf(pdf_path)
        
        # If no text or very little text, it might be scanned
        if not text.strip() or len(text) < 50:
            print("⚠️  Question paper appears to be scanned/handwritten")
            print("🔄 Converting to text-based PDF first...\n")
            
            # Create temporary text-based PDF
            temp_text_pdf = pdf_path.replace('.pdf', '_text.pdf')
            self.ocr_converter.convert_handwritten_to_text_pdf(pdf_path, temp_text_pdf)
            
            # Extract from text-based PDF
            text = self.extract_text_from_pdf(temp_text_pdf)
            
            # Clean up temp file
            if os.path.exists(temp_text_pdf):
                os.remove(temp_text_pdf)
        
        questions_data = []
        
        # Clean text
        clean_text = re.sub(r'<[^>]+>', ' ', text)
        clean_text = re.sub(r'\s+', ' ', clean_text)
        
        print("🔍 Searching for questions with marks...")
        
        # Multiple pattern strategies
        patterns = [
            # Pattern 1: Q1. question text (5 marks)
            r'Q\.?\s*(\d+)[\.\):\s]+(.*?)\((\d+)\s*[Mm]ark',
            # Pattern 2: 1. question text [5 marks]
            r'(\d+)[\.\):\s]+(.*?)\[(\d+)\s*[Mm]ark',
            # Pattern 3: Question 1 question text (5 marks)
            r'Question[\s]+(\d+)[\.\):\s]+(.*?)\((\d+)\s*[Mm]ark',
            # Pattern 4: (i), (ii) format
            r'\(([ivxIVX]+)\)\s*(.*?)\((\d+)\s*[Mm]ark',
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, clean_text, re.IGNORECASE | re.DOTALL)
            for match in matches:
                try:
                    # Handle roman numerals
                    q_num_str = match.group(1)
                    if q_num_str.lower() in ['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x']:
                        roman_map = {'i': 1, 'ii': 2, 'iii': 3, 'iv': 4, 'v': 5, 
                                   'vi': 6, 'vii': 7, 'viii': 8, 'ix': 9, 'x': 10}
                        q_num = roman_map.get(q_num_str.lower(), len(questions_data) + 1)
                    else:
                        q_num = int(q_num_str)
                    
                    q_text = match.group(2).strip()
                    marks = int(match.group(3))
                    
                    # Clean question text
                    q_text = re.sub(r'\s+', ' ', q_text)
                    q_text = q_text[:1000]
                    
                    if q_text and len(q_text) > 10 and marks > 0:
                        questions_data.append({
                            'question_number': q_num,
                            'question_text': q_text,
                            'max_marks': marks
                        })
                        print(f"  ✓ Found Q{q_num}: {marks} marks - {q_text[:60]}...")
                except Exception as e:
                    continue
        
        # Remove duplicates
        unique_questions = {}
        for q in questions_data:
            q_num = q['question_number']
            if q_num not in unique_questions or len(q['question_text']) > len(unique_questions[q_num]['question_text']):
                unique_questions[q_num] = q
        
        questions_data = sorted(unique_questions.values(), key=lambda x: x['question_number'])
        
        print(f"\n✅ Extracted {len(questions_data)} questions")
        print(f"{'='*70}\n")
        
        return questions_data
    
    def extract_answers(self, pdf_path: str):
        """Extract answers from answer key PDF"""
        print(f"\n{'='*70}")
        print(f"🔑 EXTRACTING ANSWERS FROM ANSWER KEY")
        print(f"{'='*70}\n")
        
        # Try regular text extraction
        text = self.extract_text_from_pdf(pdf_path)
        
        # If no text, convert first
        if not text.strip() or len(text) < 50:
            print("⚠️  Answer key appears to be scanned/handwritten")
            print("🔄 Converting to text-based PDF first...\n")
            
            temp_text_pdf = pdf_path.replace('.pdf', '_text.pdf')
            self.ocr_converter.convert_handwritten_to_text_pdf(pdf_path, temp_text_pdf)
            text = self.extract_text_from_pdf(temp_text_pdf)
            
            if os.path.exists(temp_text_pdf):
                os.remove(temp_text_pdf)
        
        # Clean text
        clean_text = re.sub(r'<[^>]+>', ' ', text)
        clean_text = re.sub(r'\s+', ' ', clean_text)
        
        answers_data = []
        
        print("🔍 Searching for answers...")
        
        patterns = [
            r'(?:Answer|Ans|A)[\s]*(\d+)[\.\):\s]+(.*?)(?=(?:Answer|Ans|A)[\s]*\d+|\Z)',
            r'Q\.?\s*(\d+)[\.\):\s]+(?:Answer|Ans)?[\s]*(.*?)(?=Q\.?\s*\d+|\Z)',
            r'(\d+)[\.\):\s]+(.*?)(?=\d+[\.\)]|\Z)',
            r'\(([ivxIVX]+)\)\s*(.*?)(?=\([ivxIVX]+\)|\Z)',
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, clean_text, re.IGNORECASE | re.DOTALL)
            for match in matches:
                try:
                    q_num_str = match.group(1)
                    if q_num_str.lower() in ['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x']:
                        roman_map = {'i': 1, 'ii': 2, 'iii': 3, 'iv': 4, 'v': 5,
                                   'vi': 6, 'vii': 7, 'viii': 8, 'ix': 9, 'x': 10}
                        q_num = roman_map.get(q_num_str.lower(), len(answers_data) + 1)
                    else:
                        q_num = int(q_num_str)
                    
                    answer_text = match.group(2).strip()
                    answer_text = re.sub(r'\s+', ' ', answer_text)
                    
                    if answer_text and len(answer_text) > 15:
                        answers_data.append({
                            'question_number': q_num,
                            'answer_text': answer_text
                        })
                        print(f"  ✓ Found A{q_num} - {answer_text[:60]}...")
                except:
                    continue
        
        # Remove duplicates
        unique_answers = {}
        for a in answers_data:
            q_num = a['question_number']
            if q_num not in unique_answers or len(a['answer_text']) > len(unique_answers[q_num]['answer_text']):
                unique_answers[q_num] = a
        
        answers_data = sorted(unique_answers.values(), key=lambda x: x['question_number'])
        
        print(f"\n✅ Extracted {len(answers_data)} answers")
        print(f"{'='*70}\n")
        
        return answers_data
    
    def extract_student_answers(self, pdf_path: str):
        """
        Extract student answers from handwritten PDF
        KEY CHANGE: Always converts to text-based PDF first
        """
        print(f"\n{'='*70}")
        print(f"📝 EXTRACTING STUDENT ANSWERS FROM HANDWRITTEN PDF")
        print(f"{'='*70}\n")
        print(f"📥 Input: {os.path.basename(pdf_path)}\n")
        
        try:
            # ALWAYS convert handwritten student paper to text-based PDF
            print("STEP 1: Converting handwritten PDF to text-based PDF")
            print("-" * 70)
            
            # Create text-based PDF in the same directory
            text_pdf_path = pdf_path.replace('.pdf', '_text_based.pdf')
            self.ocr_converter.convert_handwritten_to_text_pdf(pdf_path, text_pdf_path)
            
            # STEP 2: Extract text from the text-based PDF
            print("\nSTEP 2: Extracting text from text-based PDF")
            print("-" * 70)
            text = self.extract_text_from_pdf(text_pdf_path)
            
            if not text or len(text) < 20:
                raise Exception("Very little text extracted from student paper")
            
            print(f"✅ Extracted {len(text)} characters\n")
            
            # STEP 3: Parse student answers
            print("STEP 3: Parsing student answers")
            print("-" * 70)
            
            # Clean text
            clean_text = re.sub(r'<[^>]+>', ' ', text)
            clean_text = re.sub(r'\s+', ' ', clean_text)
            
            student_answers = []
            
            patterns = [
                r'(?:Answer|Ans|A)[\s]*(\d+)[\.\):\s]+(.*?)(?=(?:Answer|Ans|A)[\s]*\d+|\Z)',
                r'Q\.?\s*(\d+)[\.\):\s]+(.*?)(?=Q\.?\s*\d+|\Z)',
                r'(\d+)[\.\):\s]+(.*?)(?=\d+[\.\)]|\Z)',
                r'\(([ivxIVX]+)\)\s*(.*?)(?=\([ivxIVX]+\)|\Z)',
            ]
            
            for pattern in patterns:
                matches = re.finditer(pattern, clean_text, re.IGNORECASE | re.DOTALL)
                for match in matches:
                    try:
                        q_num_str = match.group(1)
                        if q_num_str.lower() in ['i', 'ii', 'iii', 'iv', 'v', 'vi', 'vii', 'viii', 'ix', 'x']:
                            roman_map = {'i': 1, 'ii': 2, 'iii': 3, 'iv': 4, 'v': 5,
                                       'vi': 6, 'vii': 7, 'viii': 8, 'ix': 9, 'x': 10}
                            q_num = roman_map.get(q_num_str.lower(), len(student_answers) + 1)
                        else:
                            q_num = int(q_num_str)
                        
                        answer_text = match.group(2).strip()
                        answer_text = re.sub(r'\s+', ' ', answer_text)
                        
                        if answer_text and len(answer_text) > 10:
                            student_answers.append({
                                'question_number': q_num,
                                'student_answer': answer_text
                            })
                            print(f"  ✓ Found Student Answer {q_num} - {answer_text[:60]}...")
                    except:
                        continue
            
            # Remove duplicates
            unique_answers = {}
            for a in student_answers:
                q_num = a['question_number']
                if q_num not in unique_answers or len(a['student_answer']) > len(unique_answers[q_num]['student_answer']):
                    unique_answers[q_num] = a
            
            student_answers = sorted(unique_answers.values(), key=lambda x: x['question_number'])
            
            print(f"\n✅ Successfully extracted {len(student_answers)} student answers")
            print(f"📄 Text-based PDF saved at: {text_pdf_path}")
            print(f"{'='*70}\n")
            
            return student_answers
            
        except Exception as e:
            print(f"\n❌ Error extracting student answers: {str(e)}")
            import traceback
            traceback.print_exc()
            return []
    
    def generate_result_pdf(self, evaluation_result, output_path):
        """Generate detailed result PDF with Ollama evaluation"""
        if not REPORTLAB_AVAILABLE:
            print("❌ reportlab not available - cannot generate PDF")
            self._generate_text_report(evaluation_result, output_path.replace('.pdf', '.txt'))
            return
        
        try:
            doc = SimpleDocTemplate(output_path, pagesize=A4,
                                   rightMargin=0.5*inch, leftMargin=0.5*inch,
                                   topMargin=0.75*inch, bottomMargin=0.5*inch)
            
            story = []
            
            # Title
            title_style = ParagraphStyle('CustomTitle', parent=self.styles['Heading1'],
                fontSize=20, textColor=colors.HexColor('#1a237e'), spaceAfter=20, alignment=1)
            title = Paragraph("📝 AI-Powered Answer Evaluation Report", title_style)
            story.append(title)
            story.append(Spacer(1, 0.2*inch))
            
            # Evaluation method
            method_style = ParagraphStyle('Method', parent=self.styles['Normal'],
                fontSize=10, textColor=colors.HexColor('#666666'), alignment=1, spaceAfter=15)
            method_text = evaluation_result.get('evaluation_method', 'Concept-Based Evaluation')
            method = Paragraph(f"<i>Evaluation Method: {method_text}</i>", method_style)
            story.append(method)
            story.append(Spacer(1, 0.2*inch))
            
            # Summary table
            summary_data = [
                ['Evaluation Date', datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
                ['Total Marks', str(evaluation_result['total_marks'])],
                ['Obtained Marks', f"{evaluation_result['obtained_marks']:.2f}"],
                ['Percentage', f"{evaluation_result['percentage']:.2f}%"],
                ['Grade', evaluation_result.get('grade', self._calculate_grade(evaluation_result['percentage']))]
            ]
            
            summary_table = Table(summary_data, colWidths=[2.5*inch, 3*inch])
            summary_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e3f2fd')),
                ('BACKGROUND', (1, 0), (1, -1), colors.white),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 11),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#90caf9')),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('LEFTPADDING', (0, 0), (-1, -1), 12),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ]))
            
            story.append(summary_table)
            story.append(Spacer(1, 0.4*inch))
            
            # Question-wise results heading
            heading_style = ParagraphStyle('CustomHeading', parent=self.styles['Heading2'],
                fontSize=14, textColor=colors.HexColor('#1a237e'), spaceAfter=15)
            heading = Paragraph("Question-wise Evaluation Details", heading_style)
            story.append(heading)
            
            # Question-wise table
            question_data = [['Q.No.', 'Max Marks', 'Obtained', 'Concept Match', 'Remarks']]
            
            results_key = 'question_wise_results' if 'question_wise_results' in evaluation_result else 'question_wise_marks'
            
            for q in evaluation_result[results_key]:
                q_num = q.get('Question_Number', q.get('question_number'))
                max_marks = q.get('Max_Marks', q.get('max_marks'))
                obtained = q.get('Awarded_Marks', q.get('marks_obtained', 0))
                
                # Get concept match score if available (from Ollama)
                concept_score = q.get('Concept_Match_Score', None)
                if concept_score is not None:
                    concept_text = f"{concept_score*100:.1f}%"
                else:
                    concept_text = "N/A"
                
                percentage = (obtained / max_marks * 100) if max_marks > 0 else 0
                remarks = q.get('Feedback', self._get_remarks(percentage))
                
                question_data.append([
                    str(q_num), 
                    str(max_marks), 
                    f"{obtained:.2f}",
                    concept_text,
                    remarks[:50] + "..." if len(remarks) > 50 else remarks
                ])
            
            question_table = Table(question_data, colWidths=[0.6*inch, 1*inch, 1*inch, 1.1*inch, 2.8*inch])
            question_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a237e')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#90caf9')),
                ('FONTSIZE', (0, 1), (-1, -1), 9),
                ('TOPPADDING', (0, 1), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ]))
            
            # Alternate row colors
            for i in range(1, len(question_data)):
                if i % 2 == 0:
                    question_table.setStyle(TableStyle([
                        ('BACKGROUND', (0, i), (-1, i), colors.HexColor('#f5f5f5'))
                    ]))
            
            story.append(question_table)
            story.append(Spacer(1, 0.3*inch))
            
            # Footer
            footer_style = ParagraphStyle('Footer', parent=self.styles['Normal'],
                fontSize=9, textColor=colors.grey, alignment=1)
            footer_text = "Generated by AI-Powered Answer Evaluation System<br/>DeepSeek-OCR + Ollama LLM (Concept-Based Evaluation)"
            footer = Paragraph(footer_text, footer_style)
            story.append(footer)
            
            doc.build(story)
            print(f"✅ Result PDF generated: {output_path}")
            
        except Exception as e:
            print(f"❌ Error generating result PDF: {e}")
            import traceback
            traceback.print_exc()
    
    def _calculate_grade(self, percentage):
        """Calculate grade from percentage"""
        if percentage >= 90: return 'A+'
        elif percentage >= 80: return 'A'
        elif percentage >= 70: return 'B+'
        elif percentage >= 60: return 'B'
        elif percentage >= 50: return 'C'
        elif percentage >= 40: return 'D'
        else: return 'F'
    
    def _get_remarks(self, percentage):
        """Get remarks based on percentage"""
        if percentage >= 90: return 'Excellent'
        elif percentage >= 75: return 'Very Good'
        elif percentage >= 60: return 'Good'
        elif percentage >= 50: return 'Average'
        else: return 'Needs Improvement'
    
    def _generate_text_report(self, evaluation_result, output_path):
        """Generate text report as fallback"""
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write("="*70 + "\n")
                f.write("AI-POWERED ANSWER EVALUATION REPORT\n")
                f.write("="*70 + "\n\n")
                
                f.write(f"Evaluation Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Evaluation Method: {evaluation_result.get('evaluation_method', 'Concept-Based')}\n")
                f.write(f"Total Marks: {evaluation_result['total_marks']}\n")
                f.write(f"Obtained Marks: {evaluation_result['obtained_marks']:.2f}\n")
                f.write(f"Percentage: {evaluation_result['percentage']:.2f}%\n")
                f.write(f"Grade: {evaluation_result.get('grade', self._calculate_grade(evaluation_result['percentage']))}\n")
                f.write("\n" + "-"*70 + "\n")
                f.write("QUESTION-WISE EVALUATION\n")
                f.write("-"*70 + "\n\n")
                
                results_key = 'question_wise_results' if 'question_wise_results' in evaluation_result else 'question_wise_marks'
                
                for q in evaluation_result[results_key]:
                    q_num = q.get('Question_Number', q.get('question_number'))
                    max_marks = q.get('Max_Marks', q.get('max_marks'))
                    obtained = q.get('Awarded_Marks', q.get('marks_obtained', 0))
                    feedback = q.get('Feedback', '')
                    
                    f.write(f"Question {q_num}:\n")
                    f.write(f"  Max Marks: {max_marks}\n")
                    f.write(f"  Obtained: {obtained:.2f}\n")
                    if 'Concept_Match_Score' in q:
                        f.write(f"  Concept Match: {q['Concept_Match_Score']*100:.1f}%\n")
                    if feedback:
                        f.write(f"  Feedback: {feedback}\n")
                    f.write("\n")
                
                f.write("="*70 + "\n")
                f.write("Generated by AI-Powered Answer Evaluation System\n")
                f.write("DeepSeek-OCR + Ollama LLM\n")
            
            print(f"✅ Text report generated: {output_path}")
        except Exception as e:
            print(f"❌ Error generating text report: {e}")
