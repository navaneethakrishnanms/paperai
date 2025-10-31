# 🎨 System Architecture & Visual Guide

## 📊 Complete System Overview

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃        AI-Powered Answer Evaluation System                ┃
┃     Using DeepSeek-OCR for Handwritten Recognition        ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

┌────────────────────────────────────────────────────────────┐
│                    USER INTERFACE                          │
│          Web Browser (http://localhost:5000)               │
│                                                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐   │
│  │   Upload     │  │   Upload     │  │   Evaluate   │   │
│  │  Question    │  │   Answer     │  │   Student    │   │
│  │   Paper      │  │     Key      │  │    Paper     │   │
│  └──────────────┘  └──────────────┘  └──────────────┘   │
└────────────────────────────────────────────────────────────┘
                          │
                          │ HTTP Requests (POST/GET)
                          ▼
┌────────────────────────────────────────────────────────────┐
│                   FLASK WEB SERVER                         │
│                      (app.py)                              │
│                                                            │
│  Routes:                                                   │
│  • /                          → Home page                  │
│  • /upload_question_paper     → Process questions         │
│  • /upload_answer_key         → Process answers           │
│  • /evaluate_student_paper    → Evaluate & generate       │
│  • /download_result/<file>    → Download PDF              │
│  • /get_status                → Check system status       │
└────────────────────────────────────────────────────────────┘
             │              │              │              │
             │              │              │              │
    ┌────────▼────────┐    │              │              │
    │  PDF Processor  │    │              │              │
    │ pdf_processor.py│◄───┴──────────────┘              │
    │                 │                                    │
    │ Functions:      │                                    │
    │ • Extract text  │                                    │
    │ • Parse Q&A     │                                    │
    │ • Generate PDF  │                                    │
    └────────┬────────┘                                    │
             │                                              │
             │ Uses                                         │
             ▼                                              │
    ┌────────────────┐                                     │
    │  DeepSeek-OCR  │                                     │
    │ deepseek_ocr.py│                                     │
    │                │                                     │
    │ • Load model   │                                     │
    │ • Extract text │                                     │
    │ • OCR images   │                                     │
    │ • GPU accel.   │                                     │
    └────────┬───────┘                                     │
             │                                              │
             │ Stores/Retrieves                            │
             ▼                                              │
    ┌────────────────────┐                          ┌──────▼────────┐
    │  Vector Database   │                          │    Answer     │
    │vector_db_manager.py│◄─────────────────────────│  Evaluator    │
    │                    │    Retrieves Q&A         │answer_eval.py │
    │ • ChromaDB         │                          │               │
    │ • Store Q&A        │                          │ • Compare     │
    │ • Embeddings       │                          │ • Calculate   │
    │ • Semantic search  │                          │ • Score       │
    └────────────────────┘                          └───────────────┘

┌────────────────────────────────────────────────────────────┐
│                   FILE SYSTEM STORAGE                      │
│                                                            │
│  uploads/          results/          vector_db/           │
│  └─ PDFs          └─ Result PDFs    └─ ChromaDB data     │
│                                                            │
│  output/          templates/         static/              │
│  └─ Temp OCR      └─ HTML           └─ CSS/JS            │
└────────────────────────────────────────────────────────────┘
```

---

## 🔄 Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    QUESTION PAPER UPLOAD                    │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
         ┌────────────────────────────────┐
         │   PDF File (Question Paper)    │
         │   Format: Q1. Text? (5 marks)  │
         └────────────────┬───────────────┘
                          │
                          ▼
         ┌────────────────────────────────┐
         │      PDF Text Extraction       │
         │    (PyPDF2 or DeepSeek-OCR)    │
         └────────────────┬───────────────┘
                          │
                          ▼
         ┌────────────────────────────────┐
         │     Question Parser (Regex)    │
         │   Extract: Q#, Text, Marks     │
         └────────────────┬───────────────┘
                          │
                          ▼
         ┌────────────────────────────────┐
         │      Vector DB Storage         │
         │    ChromaDB Collection         │
         └────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                     ANSWER KEY UPLOAD                       │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
         ┌────────────────────────────────┐
         │   PDF File (Answer Key)        │
         │   Format: Answer 1: Text...    │
         └────────────────┬───────────────┘
                          │
                          ▼
         ┌────────────────────────────────┐
         │      PDF Text Extraction       │
         │    (PyPDF2 or DeepSeek-OCR)    │
         └────────────────┬───────────────┘
                          │
                          ▼
         ┌────────────────────────────────┐
         │     Answer Parser (Regex)      │
         │   Extract: Q#, Answer Text     │
         └────────────────┬───────────────┘
                          │
                          ▼
         ┌────────────────────────────────┐
         │      Vector DB Storage         │
         │  Link with Questions in DB     │
         └────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│                   STUDENT PAPER EVALUATION                  │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
         ┌────────────────────────────────┐
         │   PDF File (Student Answers)   │
         │     Handwritten/Typed          │
         └────────────────┬───────────────┘
                          │
                          ▼
         ┌────────────────────────────────┐
         │    PDF to Images (pdf2image)   │
         │       Convert each page        │
         └────────────────┬───────────────┘
                          │
                          ▼
         ┌────────────────────────────────┐
         │      DeepSeek-OCR Model        │
         │   Extract Handwritten Text     │
         │      (GPU Accelerated)         │
         └────────────────┬───────────────┘
                          │
                          ▼
         ┌────────────────────────────────┐
         │   Student Answer Parser        │
         │ Extract: Q#, Student Answer    │
         └────────────────┬───────────────┘
                          │
                          ▼
         ┌────────────────────────────────┐
         │   Retrieve Correct Answers     │
         │      from Vector DB            │
         └────────────────┬───────────────┘
                          │
                          ▼
         ┌────────────────────────────────┐
         │    Answer Comparison           │
         │  • TF-IDF + Cosine (35%)       │
         │  • Sequence Match (25%)        │
         │  • Word Overlap (25%)          │
         │  • Keywords (15%)              │
         └────────────────┬───────────────┘
                          │
                          ▼
         ┌────────────────────────────────┐
         │   Calculate Similarity Score   │
         │      (0.0 to 1.0 scale)        │
         └────────────────┬───────────────┘
                          │
                          ▼
         ┌────────────────────────────────┐
         │      Apply Grading Curve       │
         │   Similarity → Marks %         │
         │   90%+ → 100% marks            │
         │   80-90% → 95% marks           │
         │   ... (graduated scale)        │
         └────────────────┬───────────────┘
                          │
                          ▼
         ┌────────────────────────────────┐
         │   Calculate Final Marks        │
         │  For each question + Total     │
         └────────────────┬───────────────┘
                          │
                          ▼
         ┌────────────────────────────────┐
         │   Generate PDF Report          │
         │    • Summary                   │
         │    • Q-wise breakdown          │
         │    • Grade & remarks           │
         └────────────────┬───────────────┘
                          │
                          ▼
         ┌────────────────────────────────┐
         │    Display Results & Download  │
         │      Save to results/          │
         └────────────────────────────────┘
```

---

## 🧠 AI Evaluation Process

```
┌─────────────────────────────────────────────────────────────┐
│              SIMILARITY CALCULATION PROCESS                 │
└─────────────────────────────────────────────────────────────┘

Input:
┌──────────────────────┐         ┌──────────────────────┐
│  Student Answer      │         │  Correct Answer      │
│ "Photosynthesis is   │         │ "Photosynthesis is   │
│  the process where   │         │  the process by which│
│  plants make food"   │         │  green plants convert│
└──────────┬───────────┘         │  light energy..."    │
           │                     └──────────┬───────────┘
           │                                │
           └────────────┬───────────────────┘
                        │
                        ▼
         ┌──────────────────────────────────┐
         │      Text Preprocessing          │
         │  • Lowercase                     │
         │  • Remove special chars          │
         │  • Normalize whitespace          │
         └──────────────┬───────────────────┘
                        │
           ┌────────────┴────────────┐
           │                         │
           ▼                         ▼
┌─────────────────────┐   ┌─────────────────────┐
│   Clean Student     │   │   Clean Correct     │
│      Answer         │   │      Answer         │
└──────────┬──────────┘   └──────────┬──────────┘
           │                         │
           └────────────┬────────────┘
                        │
        ┌───────────────┼───────────────┐
        │               │               │
        ▼               ▼               ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│  TF-IDF +   │ │  Sequence   │ │    Word     │
│  Cosine     │ │  Matcher    │ │   Overlap   │
│ Similarity  │ │  (difflib)  │ │  Analysis   │
│   (35%)     │ │   (25%)     │ │   (25%)     │
└──────┬──────┘ └──────┬──────┘ └──────┬──────┘
       │               │               │
       │               │               └────────┐
       │               │                        │
       └───────────────┴────────────┐           │
                                    │           │
                          ┌─────────▼───────────▼──┐
                          │     Keyword Match      │
                          │      Analysis          │
                          │       (15%)            │
                          └─────────┬──────────────┘
                                    │
                          ┌─────────▼──────────────┐
                          │  Weighted Combination  │
                          │  Final Score: 0.0-1.0  │
                          └─────────┬──────────────┘
                                    │
                          ┌─────────▼──────────────┐
                          │   Grading Curve        │
                          │  Score → Marks %       │
                          └─────────┬──────────────┘
                                    │
                          ┌─────────▼──────────────┐
                          │   Final Marks          │
                          │   (0 to Max Marks)     │
                          └────────────────────────┘
```

---

## 🏗️ Directory Structure

```
answer_evaluation_app/
│
├── 📄 Core Application Files
│   ├── app.py                    # Flask web server (main entry)
│   ├── pdf_processor.py          # PDF & OCR processing
│   ├── deepseek_ocr.py          # DeepSeek-OCR wrapper
│   ├── vector_db_manager.py     # ChromaDB management
│   ├── answer_evaluator.py      # AI evaluation logic
│   └── config.py                # Configuration settings
│
├── 🌐 Frontend Files
│   ├── templates/
│   │   └── index.html           # Web interface
│   └── static/
│       ├── style.css            # Styling
│       └── script.js            # JavaScript
│
├── 📦 Installation & Setup
│   ├── setup.bat                # Windows setup
│   ├── setup.sh                 # Linux/Mac setup
│   ├── start.bat                # Windows start
│   ├── start.sh                 # Linux/Mac start
│   ├── requirements.txt         # Dependencies
│   └── test_setup.py            # Verification test
│
├── 📚 Documentation
│   ├── README.md                # Overview
│   ├── INSTALLATION.md          # Setup guide
│   ├── USER_GUIDE.md            # User manual
│   ├── QUICKSTART.md            # Quick reference
│   ├── PROJECT_SUMMARY.md       # Project summary
│   └── ARCHITECTURE.md          # This file
│
├── 📁 Data Directories
│   ├── uploads/                 # Uploaded PDFs
│   ├── results/                 # Generated reports
│   ├── vector_db/               # ChromaDB storage
│   └── output/                  # Temporary OCR files
│
└── 🔧 Configuration
    └── .gitignore               # Git ignore rules
```

---

## 🔌 Component Interactions

```
┌───────────────────────────────────────────────────────────┐
│                   Component Diagram                        │
└───────────────────────────────────────────────────────────┘

        ┌─────────────────────────────────────┐
        │         Flask App (app.py)          │
        │  • Route handling                   │
        │  • File upload management           │
        │  • Response generation              │
        └─────────────┬───────────────────────┘
                      │
        ┌─────────────┼─────────────┐
        │             │             │
        ▼             ▼             ▼
┌──────────────┐ ┌──────────┐ ┌──────────────┐
│ PDFProcessor │ │ VectorDB │ │   Evaluator  │
│              │ │          │ │              │
│ • Extract    │ │ • Store  │ │ • Compare    │
│ • Parse      │ │ • Fetch  │ │ • Score      │
│ • Generate   │ │ • Search │ │ • Grade      │
└──────┬───────┘ └────┬─────┘ └──────┬───────┘
       │              │              │
       │   ┌──────────┴──────┐      │
       │   │                 │      │
       ▼   ▼                 ▼      ▼
┌────────────────┐    ┌─────────────────┐
│  DeepSeek-OCR  │    │   ChromaDB      │
│  • Model       │    │   • Collections │
│  • Inference   │    │   • Embeddings  │
│  • GPU Accel.  │    │   • Retrieval   │
└────────────────┘    └─────────────────┘
```

---

## 🎯 Use Case Diagram

```
                    ┌─────────────────┐
                    │                 │
                    │     Teacher     │
                    │                 │
                    └────────┬────────┘
                             │
       ┌─────────────────────┼─────────────────────┐
       │                     │                     │
       ▼                     ▼                     ▼
┌─────────────┐      ┌──────────────┐     ┌──────────────┐
│   Upload    │      │    Upload    │     │   Evaluate   │
│  Question   │      │    Answer    │     │   Student    │
│   Paper     │      │     Key      │     │    Paper     │
└─────────────┘      └──────────────┘     └──────────────┘
                                                  │
                                                  │
                              ┌───────────────────┴───────────────┐
                              │                                   │
                              ▼                                   ▼
                       ┌──────────────┐                   ┌──────────────┐
                       │     View     │                   │   Download   │
                       │   Results    │                   │   PDF Report │
                       └──────────────┘                   └──────────────┘
```

---

## 📊 Sequence Diagram

```
User          Browser      Flask       PDF Proc    DeepSeek    VectorDB    Evaluator
 │               │           │             │           │           │           │
 │ Upload Q.Paper│           │             │           │           │           │
 │──────────────>│           │             │           │           │           │
 │               │──POST────>│             │           │           │           │
 │               │           │──process──>│           │           │           │
 │               │           │             │──extract─>│           │           │
 │               │           │             │           │           │           │
 │               │           │             │<─text────│           │           │
 │               │           │             │           │           │           │
 │               │           │<─questions─│           │           │           │
 │               │           │──────store─────────────────────>│           │
 │               │           │             │           │           │           │
 │               │<─success─│             │           │           │           │
 │<─────────────│           │             │           │           │           │
 │               │           │             │           │           │           │
 │ Upload Answer │           │             │           │           │           │
 │──────────────>│           │             │           │           │           │
 │               │──POST────>│             │           │           │           │
 │               │           │──process──>│           │           │           │
 │               │           │             │           │           │           │
 │               │           │<──answers──│           │           │           │
 │               │           │──────store─────────────────────>│           │
 │               │<─success─│             │           │           │           │
 │<─────────────│           │             │           │           │           │
 │               │           │             │           │           │           │
 │ Upload Student│           │             │           │           │           │
 │──────────────>│           │             │           │           │           │
 │               │──POST────>│             │           │           │           │
 │               │           │──process──>│           │           │           │
 │               │           │             │──OCR────>│           │           │
 │               │           │             │           │           │           │
 │               │           │             │<─text────│           │           │
 │               │           │             │           │           │           │
 │               │           │<─student_ans│           │           │           │
 │               │           │──get Q&A────────────────────────>│           │
 │               │           │<─────────────────────────────────│           │
 │               │           │──evaluate──────────────────────────────────>│
 │               │           │                                               │
 │               │           │<──────────results─────────────────────────────│
 │               │           │──gen PDF──>│           │           │           │
 │               │           │             │           │           │           │
 │               │<─results─│             │           │           │           │
 │<─────────────│           │             │           │           │           │
```

---

## 🔐 Security Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Security Layers                          │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ Layer 1: Application Security                              │
│  • File type validation (PDF only)                         │
│  • File size limits (50MB max)                             │
│  • Filename sanitization (secure_filename)                 │
│  • Error handling & logging                                │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│ Layer 2: Data Privacy                                      │
│  • Local processing only (no external APIs)                │
│  • No data transmission to internet                        │
│  • Files stored locally only                               │
│  • No user tracking or analytics                           │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│ Layer 3: File System Security                              │
│  • Separate directories for uploads/results                │
│  • Automatic directory creation                            │
│  • Read/write permissions managed                          │
│  • Temporary files cleaned up                              │
└─────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│ Layer 4: Model Security                                    │
│  • Trusted model source (HuggingFace)                      │
│  • Model loaded with trust_remote_code=True                │
│  • GPU isolation                                            │
│  • Memory management                                        │
└─────────────────────────────────────────────────────────────┘
```

---

**This architecture document provides a comprehensive visual understanding of the AI Answer Evaluation System!**

For implementation details, see the code files.  
For usage instructions, see USER_GUIDE.md  
For setup, see INSTALLATION.md
