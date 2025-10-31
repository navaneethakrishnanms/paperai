# 📊 VISUAL SYSTEM ARCHITECTURE

## 🎯 Complete Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         USER UPLOADS 3 PDFs                              │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
        ┌───────────────────────────┼───────────────────────────┐
        │                           │                           │
        ▼                           ▼                           ▼
┌───────────────┐          ┌─────────────────┐        ┌─────────────────┐
│   QUESTION    │          │   ANSWER KEY    │        │  STUDENT PAPER  │
│   PAPER PDF   │          │      PDF        │        │   (HANDWRITTEN) │
└───────────────┘          └─────────────────┘        └─────────────────┘
        │                           │                           │
        │ PyPDF2                    │ PyPDF2                    │
        │ (or OCR if scanned)       │ (or OCR if scanned)       │
        │                           │                           │
        ▼                           ▼                           ▼
┌───────────────┐          ┌─────────────────┐        ┌─────────────────┐
│  QUESTIONS    │          │     ANSWERS     │        │   STAGE 1: OCR  │
│  Q1: text (5) │          │  A1: text       │        │  DeepSeek-OCR   │
│  Q2: text (10)│          │  A2: text       │        │  Extract Text   │
│  Q3: text (3) │          │  A3: text       │        └─────────────────┘
└───────────────┘          └─────────────────┘                 │
        │                           │                           │
        │                           │                           ▼
        │                           │                  ┌─────────────────┐
        │                           │                  │   STAGE 2: PDF  │
        │                           │                  │   FPDF2 Create  │
        │                           │                  │  Text-Based PDF │
        │                           │                  └─────────────────┘
        │                           │                           │
        │                           │                           │
        │                           │                           ▼
        │                           │                  ┌─────────────────┐
        │                           │                  │ STAGE 3: EXTRACT│
        │                           │                  │  PyPDF2 Extract │
        │                           │                  │  Clean Text     │
        │                           │                  └─────────────────┘
        │                           │                           │
        │                           │                           ▼
        │                           │                  ┌─────────────────┐
        │                           │                  │ STUDENT ANSWERS │
        │                           │                  │  S1: answer     │
        │                           │                  │  S2: answer     │
        │                           │                  │  S3: answer     │
        └───────────────────────────┴───────────────────────────┘
                                    │
                                    ▼
        ┌───────────────────────────────────────────────────────┐
        │           OLLAMA LLM CONCEPT-BASED EVALUATION         │
        │                                                        │
        │  For each question:                                   │
        │    Input: Question + Correct Answer + Student Answer │
        │    Process: LLM analyzes concept understanding        │
        │    Output: Marks + Concept Score + Feedback          │
        └───────────────────────────────────────────────────────┘
                                    │
                                    ▼
        ┌───────────────────────────────────────────────────────┐
        │              EVALUATION RESULTS                        │
        │                                                        │
        │  Q1: 4.5/5 marks (90% concept) - Excellent            │
        │  Q2: 8.0/10 marks (80% concept) - Good               │
        │  Q3: 2.0/3 marks (67% concept) - Average             │
        │                                                        │
        │  Total: 42.5/50 (85%) - Grade: A                     │
        └───────────────────────────────────────────────────────┘
                                    │
                                    ▼
        ┌───────────────────────────────────────────────────────┐
        │              REPORTLAB PDF GENERATION                  │
        │                                                        │
        │  Creates professional PDF with:                       │
        │    - Summary table (marks, %, grade)                 │
        │    - Question-wise breakdown                          │
        │    - Concept match scores                             │
        │    - AI feedback for each answer                      │
        │    - Color-coded, formatted                           │
        └───────────────────────────────────────────────────────┘
                                    │
                                    ▼
        ┌───────────────────────────────────────────────────────┐
        │                  RESULT PDF DOWNLOAD                   │
        │              Ready for teacher review!                 │
        └───────────────────────────────────────────────────────┘
```

---

## 🔄 Student Paper Processing (Detailed)

```
HANDWRITTEN STUDENT PDF (from phone camera)
        │
        ├─── Contains: Scanned/photographed handwritten answers
        ├─── Format: Image-based PDF (not searchable)
        ├─── Problem: PyPDF2 can't extract text directly
        │
        ▼
╔═══════════════════════════════════════════════════════════╗
║              STAGE 1: DEEPSEEK OCR EXTRACTION             ║
╚═══════════════════════════════════════════════════════════╝
        │
        ├─── Process:
        │    1. Convert PDF pages to images (pdf2image)
        │    2. For each image:
        │       - Load into DeepSeek-OCR model
        │       - Run transformer-based recognition
        │       - Extract handwritten text
        │    3. Combine all pages
        │
        ├─── Output: Raw extracted text
        │    "Answer 1 Photosynthesis is when plants make food
        │     Answer 2 Newton's laws state that..."
        │
        ├─── Challenges handled:
        │    ✓ Various handwriting styles
        │    ✓ Poor image quality
        │    ✓ Skewed/rotated text
        │
        ▼
╔═══════════════════════════════════════════════════════════╗
║           STAGE 2: FPDF2 TEXT PDF CREATION                ║
╚═══════════════════════════════════════════════════════════╝
        │
        ├─── Process:
        │    1. Create new PDF document (FPDF)
        │    2. Add title: "Extracted Student Answers"
        │    3. Parse and format text:
        │       - Detect question numbers
        │       - Bold question headers
        │       - Format paragraphs
        │    4. Save as text-based searchable PDF
        │
        ├─── Output: Clean text-based PDF
        │    Filename: student_xxx_text_based.pdf
        │
        ├─── Benefits:
        │    ✓ Searchable PDF
        │    ✓ Structured format
        │    ✓ PyPDF2 compatible
        │    ✓ Can be archived
        │
        ▼
╔═══════════════════════════════════════════════════════════╗
║          STAGE 3: PYPDF2 TEXT EXTRACTION                  ║
╚═══════════════════════════════════════════════════════════╝
        │
        ├─── Process:
        │    1. Open text-based PDF
        │    2. Extract text page by page (PyPDF2)
        │    3. Parse student answers:
        │       - Find question numbers
        │       - Extract answer text
        │       - Clean and normalize
        │
        ├─── Output: Structured student answers
        │    [
        │      {question_number: 1, student_answer: "..."},
        │      {question_number: 2, student_answer: "..."},
        │      ...
        │    ]
        │
        ├─── Why this stage?
        │    ✓ PyPDF2 is reliable with text PDFs
        │    ✓ Consistent text extraction
        │    ✓ Easy to parse and structure
        │    ✓ No OCR artifacts
        │
        ▼
   READY FOR OLLAMA EVALUATION!
```

---

## 🧠 Ollama Evaluation Process

```
FOR EACH QUESTION:

Input Data:
├─ Question Text: "What is photosynthesis?"
├─ Max Marks: 5
├─ Correct Answer: "Photosynthesis is the process by which..."
└─ Student Answer: "Plants make food using sunlight..."

        │
        ▼

╔═══════════════════════════════════════════════════════════╗
║                PROMPT GENERATION                           ║
╚═══════════════════════════════════════════════════════════╝

System: "You are an expert teacher evaluating students..."

Prompt:
"""
Question: What is photosynthesis?
Max Marks: 5

Correct Answer:
Photosynthesis is the process by which green plants use
sunlight, water, and carbon dioxide to produce glucose
and oxygen.

Student's Answer:
Plants make food using sunlight and release oxygen.

Evaluate based on CONCEPT UNDERSTANDING (not exact wording).
Respond ONLY with JSON:
{
  "concept_match_score": <0 to 1>,
  "awarded_marks": <0 to 5>,
  "feedback": "<constructive feedback>"
}
"""

        │
        ▼

╔═══════════════════════════════════════════════════════════╗
║           OLLAMA LLM PROCESSING                            ║
╚═══════════════════════════════════════════════════════════╝

LLM thinks:
✓ Student mentions "make food" (glucose production)
✓ Student mentions "sunlight" (light energy)
✓ Student mentions "release oxygen" (byproduct)
✗ Missing "water and CO2" (incomplete)
✗ Missing "glucose" specifically

Concept understanding: Good but incomplete

        │
        ▼

╔═══════════════════════════════════════════════════════════╗
║              EVALUATION RESULT                             ║
╚═══════════════════════════════════════════════════════════╝

{
  "question_number": 1,
  "concept_match_score": 0.70,
  "awarded_marks": 3.5,
  "max_marks": 5,
  "feedback": "Good understanding of the concept. You
              correctly identified sunlight as the energy
              source and oxygen as a product. However, you
              should mention water and carbon dioxide as
              inputs, and be more specific about glucose
              production.",
  "error": false
}

        │
        ▼

   Added to evaluation results!
```

---

## 📊 Component Interaction Map

```
┌─────────────────────────────────────────────────────────────┐
│                    FLASK WEB SERVER                          │
│                  (app_ollama_complete.py)                    │
└─────────────────────────────────────────────────────────────┘
    │
    ├─── Endpoints:
    │    ├─ POST /upload_question_paper
    │    ├─ POST /upload_answer_key
    │    ├─ POST /evaluate_student_paper
    │    └─ GET  /download_result/<filename>
    │
    ├─── Uses:
    │    │
    │    ├─► PDFProcessorOllama
    │    │   (pdf_processor_ollama.py)
    │    │   │
    │    │   ├─► OCRToTextPDFConverter
    │    │   │   (ocr_to_text_pdf_converter.py)
    │    │   │   │
    │    │   │   └─► DeepSeekOCR
    │    │   │       (deepseek_ocr.py)
    │    │   │       │
    │    │   │       └─► PyTorch + Transformers
    │    │   │
    │    │   ├─► PyPDF2
    │    │   │   (Text extraction)
    │    │   │
    │    │   ├─► FPDF2
    │    │   │   (Text PDF creation)
    │    │   │
    │    │   └─► ReportLab
    │    │       (Result PDF generation)
    │    │
    │    └─► OllamaEvaluator
    │        (ollama_evaluator.py)
    │        │
    │        └─► Ollama CLI
    │            (subprocess call to ollama)
    │            │
    │            └─► LLM Model (llama3.1)
    │
    └─── Storage:
         ├─ uploads/     (Uploaded PDFs)
         └─ results/     (Generated result PDFs)
```

---

## 🔄 Data Structures

### Question Object:
```python
{
    'question_number': 1,
    'question_text': 'What is photosynthesis?',
    'max_marks': 5
}
```

### Answer Object:
```python
{
    'question_number': 1,
    'answer_text': 'Photosynthesis is the process...'
}
```

### Student Answer Object:
```python
{
    'question_number': 1,
    'student_answer': 'Plants make food using sunlight...'
}
```

### Evaluation Result Object:
```python
{
    'Question_Number': 1,
    'Concept_Match_Score': 0.70,
    'Awarded_Marks': 3.5,
    'Max_Marks': 5.0,
    'Feedback': 'Good understanding but incomplete...',
    'Error': False
}
```

### Complete Evaluation:
```python
{
    'total_marks': 50,
    'obtained_marks': 42.5,
    'percentage': 85.0,
    'grade': 'A',
    'question_wise_results': [
        {...evaluation result...},
        {...evaluation result...},
        ...
    ],
    'evaluation_method': 'Concept-Based (Ollama llama3.1)'
}
```

---

## 📈 Performance Optimization Points

```
┌─────────────────────────────────────────────────────┐
│         PERFORMANCE BOTTLENECKS & SOLUTIONS         │
└─────────────────────────────────────────────────────┘

1. DeepSeek OCR (Slowest - 30-60s per page on CPU)
   ├─ Solution 1: Use GPU (10x faster)
   ├─ Solution 2: Reduce image resolution
   └─ Solution 3: Cache OCR results

2. Ollama Evaluation (Moderate - 5-10s per question)
   ├─ Solution 1: Use lighter model (phi3, mistral)
   ├─ Solution 2: Parallel processing (future)
   └─ Solution 3: GPU acceleration (auto)

3. PDF Generation (Fast - 2-3s)
   └─ No optimization needed

4. Text Extraction (Fast - 1-2s)
   └─ No optimization needed

Total Time for 10 Questions:
├─ OCR (3 pages): 30-60s
├─ Evaluation (10 Q): 50-100s
└─ Generation: 5s
    TOTAL: ~2-3 minutes
```

---

This visual guide shows exactly how data flows through your system! 🎨
