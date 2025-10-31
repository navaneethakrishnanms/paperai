# 🎨 System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                     AI-POWERED ANSWER EVALUATION SYSTEM                             │
│                   (DeepSeek-OCR + Ollama LLM Integration)                          │
└─────────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────────┐
│                              PHASE 1: QUESTION PAPER UPLOAD                         │
└─────────────────────────────────────────────────────────────────────────────────────┘

    📄 Question Paper PDF (Typed or Scanned)
              │
              ↓
    ┌─────────────────────┐
    │  PDF Processor      │ 
    │  (pdf_processor.py) │ ───→ If Typed: PyPDF2 extract text
    └─────────────────────┘ ───→ If Scanned: DeepSeek-OCR
              │
              ↓
    📋 Extracted Text:
       "Q1. What is photosynthesis? (5 marks)
        Q2. Describe DNA structure. (10 marks)
        Q3. Calculate force. (3 marks)"
              │
              ↓
    ┌─────────────────────┐
    │  Pattern Matching   │
    │  (Regex Patterns)   │ ───→ Extract: Question No. + Text + Marks
    └─────────────────────┘
              │
              ↓
    ┌─────────────────────────────────┐
    │  Vector Database (ChromaDB)     │
    │  Questions Collection:          │
    │  [                              │
    │    {q_num: 1, text: "...",      │
    │     max_marks: 5},              │
    │    {q_num: 2, text: "...",      │
    │     max_marks: 10},             │
    │  ]                              │
    └─────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────────┐
│                              PHASE 2: ANSWER KEY UPLOAD                             │
└─────────────────────────────────────────────────────────────────────────────────────┘

    📄 Answer Key PDF (Typed or Scanned)
              │
              ↓
    ┌─────────────────────┐
    │  PDF Processor      │
    │  (pdf_processor.py) │ ───→ Extract text (PyPDF2 or DeepSeek-OCR)
    └─────────────────────┘
              │
              ↓
    📋 Extracted Text:
       "Answer 1: Photosynthesis is...
        Answer 2: DNA has double helix...
        Answer 3: F = ma, F = 50N"
              │
              ↓
    ┌─────────────────────┐
    │  Pattern Matching   │
    │  (Regex Patterns)   │ ───→ Extract: Question No. + Answer Text
    └─────────────────────┘
              │
              ↓
    ┌─────────────────────────────────┐
    │  Vector Database (ChromaDB)     │
    │  Answers Collection:            │
    │  [                              │
    │    {q_num: 1, text: "Photo..."},│
    │    {q_num: 2, text: "DNA..."},  │
    │  ]                              │
    └─────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────────┐
│                    PHASE 3: STUDENT ANSWER EVALUATION (MAIN)                        │
└─────────────────────────────────────────────────────────────────────────────────────┘

    📱 Student's Handwritten Answer PDF (Phone Camera / Scanned)
              │
              ↓
    ┌─────────────────────────────────────────────┐
    │ STEP 1: HANDWRITTEN TEXT EXTRACTION         │
    │                                             │
    │  PDF → Images (pdf2image + Poppler)         │
    │        ↓                                    │
    │  DeepSeek-OCR Model                         │
    │  (deepseek_ocr.py)                          │
    │  - Transformer-based OCR                    │
    │  - base_size: 1024                          │
    │  - image_size: 640                          │
    │  - crop_mode: True (tiling)                 │
    │        ↓                                    │
    │  Extracted Text Per Page                    │
    │        ↓                                    │
    │  Combined Text from All Pages               │
    │        ↓                                    │
    │  Create Searchable PDF (FPDF2)              │
    └─────────────────────────────────────────────┘
              │
              ↓
    📝 OCR Output:
       "Answer 1: Plants use sunlight to make food...
        Answer 2: DNA is a molecule...
        Answer 3: Force = 10 x 5 = 50N"
              │
              ↓
    ┌─────────────────────────────────────────────┐
    │ STEP 2: PARSE STUDENT ANSWERS               │
    │                                             │
    │  Pattern Matching (Regex)                   │
    │  - Identify question numbers                │
    │  - Extract answer text per question         │
    │  - Create structured data                   │
    └─────────────────────────────────────────────┘
              │
              ↓
    📊 Parsed Student Answers:
       [
         {q_num: 1, answer: "Plants use sunlight..."},
         {q_num: 2, answer: "DNA is a molecule..."},
         {q_num: 3, answer: "Force = 50N"}
       ]
              │
              ↓
    ┌─────────────────────────────────────────────────────────────────────┐
    │ STEP 3: CONCEPT-BASED EVALUATION USING OLLAMA LLM                   │
    │                                                                     │
    │  FOR EACH STUDENT ANSWER:                                           │
    │                                                                     │
    │  ┌────────────────────────────────────────────────────┐            │
    │  │ 1. Fetch from Vector DB:                           │            │
    │  │    - Question Text                                 │            │
    │  │    - Maximum Marks                                 │            │
    │  │    - Correct Answer (from Answer Key)              │            │
    │  └────────────────────────────────────────────────────┘            │
    │              ↓                                                      │
    │  ┌────────────────────────────────────────────────────┐            │
    │  │ 2. Create Evaluation Prompt:                       │            │
    │  │                                                    │            │
    │  │    "Question: {question_text}                     │            │
    │  │     Max Marks: {max_marks}                        │            │
    │  │     Correct Answer: {correct_answer}              │            │
    │  │     Student Answer: {student_answer}              │            │
    │  │                                                    │            │
    │  │     Evaluate based on CONCEPT UNDERSTANDING.      │            │
    │  │     Return JSON:                                  │            │
    │  │     {                                             │            │
    │  │       'concept_match_score': float (0-1),        │            │
    │  │       'awarded_marks': float (0-max),            │            │
    │  │       'feedback': str (1-2 sentences)            │            │
    │  │     }"                                            │            │
    │  └────────────────────────────────────────────────────┘            │
    │              ↓                                                      │
    │  ┌────────────────────────────────────────────────────┐            │
    │  │ 3. Send to Ollama LLM:                             │            │
    │  │    (ollama_evaluator.py)                           │            │
    │  │                                                    │            │
    │  │    subprocess.run(["ollama", "run",               │            │
    │  │                   "llama3.1:latest"],             │            │
    │  │                   input=prompt)                    │            │
    │  └────────────────────────────────────────────────────┘            │
    │              ↓                                                      │
    │  ┌────────────────────────────────────────────────────┐            │
    │  │ 4. Parse JSON Response:                            │            │
    │  │                                                    │            │
    │  │    {                                              │            │
    │  │      "concept_match_score": 0.85,                │            │
    │  │      "awarded_marks": 4.25,                      │            │
    │  │      "feedback": "Good understanding of basic     │            │
    │  │                  concept, but could include more  │            │
    │  │                  details about chloroplasts."     │            │
    │  │    }                                              │            │
    │  └────────────────────────────────────────────────────┘            │
    │              ↓                                                      │
    │  ┌────────────────────────────────────────────────────┐            │
    │  │ 5. Store Evaluation Result                         │            │
    │  └────────────────────────────────────────────────────┘            │
    │                                                                     │
    │  REPEAT FOR ALL QUESTIONS                                          │
    └─────────────────────────────────────────────────────────────────────┘
              │
              ↓
    📊 Evaluation Results:
       [
         {q_num: 1, max: 5, awarded: 4.25, concept: 0.85, feedback: "..."},
         {q_num: 2, max: 10, awarded: 7.5, concept: 0.75, feedback: "..."},
         {q_num: 3, max: 3, awarded: 3.0, concept: 1.0, feedback: "..."}
       ]
              │
              ↓
    ┌─────────────────────────────────────────────┐
    │ STEP 4: CALCULATE OVERALL RESULTS           │
    │                                             │
    │  Total Marks: 5 + 10 + 3 = 18              │
    │  Obtained: 4.25 + 7.5 + 3.0 = 14.75        │
    │  Percentage: 14.75/18 = 81.94%             │
    │  Grade: A (based on grading scale)          │
    └─────────────────────────────────────────────┘
              │
              ↓
    ┌─────────────────────────────────────────────────────────┐
    │ STEP 5: GENERATE RESULT PDF (ReportLab)                │
    │                                                         │
    │  ┌─────────────────────────────────────────────┐       │
    │  │ 📊 EVALUATION REPORT                        │       │
    │  │                                             │       │
    │  │ Student: John Doe                           │       │
    │  │ Date: 2025-10-31                            │       │
    │  │                                             │       │
    │  │ ════════════════════════════════════════     │       │
    │  │ SUMMARY                                     │       │
    │  │ ════════════════════════════════════════     │       │
    │  │ Total Marks:      14.75 / 18                │       │
    │  │ Percentage:       81.94%                    │       │
    │  │ Grade:            A                         │       │
    │  │ Method:           Concept-Based (Ollama)    │       │
    │  │                                             │       │
    │  │ ════════════════════════════════════════     │       │
    │  │ QUESTION-WISE BREAKDOWN                     │       │
    │  │ ════════════════════════════════════════     │       │
    │  │                                             │       │
    │  │ Question 1:                                 │       │
    │  │ Marks: 4.25 / 5 (85%)                       │       │
    │  │ Concept Match: 85%                          │       │
    │  │ Feedback: Good understanding of basic...    │       │
    │  │                                             │       │
    │  │ Question 2:                                 │       │
    │  │ Marks: 7.5 / 10 (75%)                       │       │
    │  │ Concept Match: 75%                          │       │
    │  │ Feedback: Covered main points but...        │       │
    │  │                                             │       │
    │  │ Question 3:                                 │       │
    │  │ Marks: 3.0 / 3 (100%)                       │       │
    │  │ Concept Match: 100%                         │       │
    │  │ Feedback: Perfect answer with correct...    │       │
    │  │                                             │       │
    │  │ ════════════════════════════════════════     │       │
    │  │ Overall: Very good work! Strong grasp       │       │
    │  │ of core concepts.                           │       │
    │  └─────────────────────────────────────────────┘       │
    └─────────────────────────────────────────────────────────┘
              │
              ↓
    💾 Result PDF Saved to: results/result_john_doe.pdf
              │
              ↓
    ⬇️ User Downloads PDF

┌─────────────────────────────────────────────────────────────────────────────────────┐
│                              SYSTEM COMPONENTS                                      │
└─────────────────────────────────────────────────────────────────────────────────────┘

┌──────────────────────┐   ┌──────────────────────┐   ┌──────────────────────┐
│  Flask Web App       │   │  DeepSeek-OCR        │   │  Ollama LLM          │
│  (app_ollama_        │   │  (deepseek_ocr.py)   │   │  (ollama_evaluator   │
│   integrated.py)     │   │                      │   │   .py)               │
│                      │   │  - Transformer OCR   │   │                      │
│  - Upload handlers   │   │  - Handwriting rec.  │   │  - Concept eval      │
│  - Orchestration     │   │  - Image processing  │   │  - Subprocess call   │
│  - Response          │   │  - PDF to images     │   │  - JSON parsing      │
└──────────────────────┘   └──────────────────────┘   └──────────────────────┘

┌──────────────────────┐   ┌──────────────────────┐   ┌──────────────────────┐
│  PDF Processor       │   │  Vector Database     │   │  PDF Generator       │
│  (pdf_processor.py)  │   │  (vector_db_         │   │  (pdf_generator.py)  │
│                      │   │   manager.py)        │   │                      │
│  - Text extraction   │   │                      │   │  - Result PDF        │
│  - Pattern matching  │   │  - ChromaDB          │   │  - OCR PDF           │
│  - Answer parsing    │   │  - Embeddings        │   │  - ReportLab/FPDF2   │
└──────────────────────┘   └──────────────────────┘   └──────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────────┐
│                              DATA FLOW SUMMARY                                      │
└─────────────────────────────────────────────────────────────────────────────────────┘

Question Paper → Extract → Store in DB
Answer Key → Extract → Store in DB
Student Paper → OCR → Parse → Evaluate (Ollama) → Calculate → Generate PDF → Download

┌─────────────────────────────────────────────────────────────────────────────────────┐
│                              TECHNOLOGY STACK                                       │
└─────────────────────────────────────────────────────────────────────────────────────┘

Frontend:        HTML, CSS, JavaScript (templates/index.html)
Backend:         Flask (Python)
OCR:             DeepSeek-OCR (Transformer-based)
LLM:             Ollama (llama3.1, mistral, phi, etc.)
Vector DB:       ChromaDB (with sentence-transformers)
PDF Processing:  PyPDF2, pdf2image, Poppler
PDF Generation:  FPDF2, ReportLab
ML/NLP:          PyTorch, Transformers, scikit-learn

┌─────────────────────────────────────────────────────────────────────────────────────┐
│                              KEY ADVANTAGES                                         │
└─────────────────────────────────────────────────────────────────────────────────────┘

✅ 100% Local Processing (Privacy)
✅ Concept-Based Evaluation (Not keyword matching)
✅ Handwritten Text Support (Phone captures OK)
✅ Detailed Feedback (Constructive comments)
✅ Professional Reports (Color-coded PDFs)
✅ Flexible Question Formats (Multiple regex patterns)
✅ Fair Marking (Semantic understanding)
✅ Time Saving (2-3 min vs 15-20 min per paper)

┌─────────────────────────────────────────────────────────────────────────────────────┐
│                              FILES CREATED                                          │
└─────────────────────────────────────────────────────────────────────────────────────┘

📄 app_ollama_integrated.py       - Main application
📄 COMPLETE_GUIDE_OLLAMA.md       - Full documentation
📄 QUICKSTART_OLLAMA.md           - Quick reference
📄 SYSTEM_PROMPT.md               - Technical docs
📄 PROJECT_SUMMARY_COMPLETE.md    - This summary
📄 VISUAL_ARCHITECTURE.md         - This diagram
📄 start_ollama_integrated.bat    - Startup script
📄 test_complete_system.py        - Validation script
📄 requirements_ollama_full.txt   - Dependencies

Total: 9 new files + utilizing 5+ existing files = Complete system!
```
