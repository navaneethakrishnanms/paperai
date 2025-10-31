# 🎯 COMPLETE SETUP GUIDE - Ollama LLM Answer Evaluation

## What This System Does

This is a complete AI-powered pipeline that:

1. **Reads PDFs** → Question papers, answer keys, student answers
2. **OCR Handwriting** → Uses DeepSeek OCR to read handwritten text
3. **Creates Text PDFs** → Converts scanned PDFs to searchable text
4. **AI Evaluation** → Uses Ollama LLM for intelligent grading
5. **Generates Reports** → Professional PDF reports with feedback

---

## 📦 Installation Steps

### Step 1: Install Ollama (Required)

#### Windows:
1. Go to: https://ollama.ai
2. Download Windows installer
3. Run installer
4. Open terminal and verify:
```bash
ollama --version
```

#### Linux:
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

#### macOS:
```bash
brew install ollama
```

### Step 2: Download AI Model

```bash
# Download llama3.2 (recommended - 2GB)
ollama pull llama3.2

# Alternative models:
ollama pull mistral      # Smaller (4GB), faster
ollama pull llama3       # Larger (8GB), more accurate
```

### Step 3: Setup Python Environment

```bash
# Navigate to project folder
cd C:\Users\nk\paperai\answer_evaluation_app

# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Install PyTorch with GPU support
pip install torch==2.1.1 torchvision==0.16.1 --index-url https://download.pytorch.org/whl/cu118

# Install all dependencies
pip install -r requirements_ollama.txt
```

### Step 4: Install Poppler (for PDF processing)

#### Windows:
1. Download: https://github.com/oschwartz10612/poppler-windows/releases/
2. Extract to `C:\poppler`
3. Add `C:\poppler\Library\bin` to PATH
4. Restart terminal and verify:
```bash
pdfinfo -v
```

#### Linux:
```bash
sudo apt-get install poppler-utils
```

### Step 5: Test Everything

```bash
python test_ollama_system.py
```

You should see all tests pass ✅

---

## 🚀 Running the System

### Quick Start:

**Windows:**
```bash
start_ollama.bat
```

**Manual:**
```bash
python app_ollama.py
```

Open browser: **http://localhost:5000**

---

## 📝 How to Use

### 1. Upload Question Paper

**Format:**
```
Q1. What is photosynthesis? (5 marks)
Q2. Explain the water cycle. (10 marks)
Q3. List 3 types of energy. (5 marks)
```

**What happens:**
- System extracts questions
- Detects marks for each question
- Stores in database

### 2. Upload Answer Key

**Format:**
```
Answer 1: Photosynthesis is the process by which plants convert light energy into chemical energy using chlorophyll.

Answer 2: The water cycle is the continuous movement of water. It includes evaporation, condensation, precipitation, and collection.

Answer 3: Three types of energy are: solar energy, wind energy, and hydroelectric power.
```

**What happens:**
- System extracts correct answers
- Stores alongside questions
- Ready for evaluation

### 3. Upload Student Answer Sheet

**Supported:**
- ✅ Handwritten PDFs (scanned)
- ✅ Typed PDFs
- ✅ Mixed format

**What happens:**
- Detects if image-based or text-based
- If image-based:
  - Uses DeepSeek OCR to extract handwriting
  - Creates `student_text_answer.pdf` (searchable)
- Extracts student answers
- Sends to Ollama LLM for evaluation
- Generates detailed report

### 4. View & Download Results

**Outputs:**
1. **`student_text_answer.pdf`** - Searchable text version
2. **`result_<filename>.pdf`** - Evaluation report with:
   - Total marks
   - Obtained marks
   - Percentage & Grade
   - Question-wise breakdown
   - Detailed feedback
3. **`evaluation_<filename>.json`** - Structured data

---

## 🎯 How Ollama Evaluation Works

### Traditional System (Old):
```
Student Answer → TF-IDF → Cosine Similarity → Score
Problem: Only matches words, not concepts
```

### Ollama System (New):
```
Student Answer → Ollama LLM → Concept Analysis → Score + Feedback
Advantage: Understands concepts, gives feedback
```

### Example:

**Question:** What is photosynthesis? (5 marks)

**Answer Key:** 
"Photosynthesis is the process by which green plants convert light energy into chemical energy using chlorophyll in their leaves."

**Student Answer:** 
"Plants use sunlight to make food with chlorophyll."

**Ollama Evaluation:**
```json
{
  "awarded_marks": 3.5,
  "concept_match_score": 0.70,
  "feedback": "Good basic understanding. Covered: sunlight, chlorophyll, food production. Missing: energy conversion, location in leaves.",
  "key_points_covered": [
    "Use of sunlight",
    "Role of chlorophyll",
    "Food production"
  ],
  "key_points_missed": [
    "Energy conversion concept",
    "Location in leaves"
  ]
}
```

---

## 🔧 Configuration

### Change AI Model

Edit `app_ollama.py` (line 25):
```python
# Change this line:
evaluator = OllamaEvaluator(model_name="llama3.2")

# To any of these:
evaluator = OllamaEvaluator(model_name="mistral")    # Faster
evaluator = OllamaEvaluator(model_name="llama3")      # More accurate
evaluator = OllamaEvaluator(model_name="codellama")   # For technical content
```

### Adjust Grading Strictness

Edit `ollama_evaluator.py` - modify the evaluation prompt to be more/less strict.

---

## 📊 Performance

### With GPU (RTX 3050):
- Question extraction: < 1 second
- Answer key extraction: < 1 second
- Student OCR (5 pages): 30-60 seconds
- LLM evaluation per question: 5-10 seconds
- **Total for 10 questions: ~2-3 minutes**

### Without GPU (CPU only):
- OCR: 3-5 minutes
- LLM evaluation: 10-15 seconds per question
- **Total for 10 questions: ~5-7 minutes**

---

## 🐛 Troubleshooting

### "Ollama not found"
```bash
# Verify installation
ollama --version

# Check if service is running
ollama serve  # Should show "Ollama is running"
```

### "Model not available"
```bash
# List models
ollama list

# Download if missing
ollama pull llama3.2
```

### "CUDA not available"
```bash
# Check PyTorch GPU
python -c "import torch; print(torch.cuda.is_available())"

# If False, reinstall PyTorch with CUDA:
pip uninstall torch torchvision
pip install torch==2.1.1 torchvision==0.16.1 --index-url https://download.pytorch.org/whl/cu118
```

### "Poppler not found"
```bash
# Windows: Add to PATH
# Linux: sudo apt-get install poppler-utils
```

### Slow Evaluation
- Use smaller model: `mistral` instead of `llama3`
- Reduce question count
- Use GPU if available

---

## 📁 File Structure

```
answer_evaluation_app/
├── app_ollama.py              # Main Flask app
├── ollama_evaluator.py        # LLM evaluation logic
├── pdf_processor_ollama.py    # PDF & OCR processing
├── ocr_to_text_pdf.py         # OCR to PDF converter
├── vector_db_manager.py       # Database management
├── deepseek_ocr.py            # DeepSeek OCR wrapper
├── requirements_ollama.txt    # Dependencies
├── start_ollama.bat           # Windows startup script
├── test_ollama_system.py      # Test suite
├── README_OLLAMA.md           # This file
│
├── uploads/                   # Uploaded PDFs
├── output/                    # student_text_answer.pdf
├── results/                   # Evaluation reports
└── vector_db/                 # Question & answer storage
```

---

## 🎓 Best Practices

### For Question Papers:
- ✅ Clear question numbers (Q1, Q2, etc.)
- ✅ Marks clearly indicated (5 marks), [10 marks]
- ✅ One question per number

### For Answer Keys:
- ✅ Match question numbers exactly
- ✅ Complete answers with all key concepts
- ✅ Clear formatting

### For Student Papers:
- ✅ Legible handwriting (for OCR)
- ✅ Clear question numbers
- ✅ High resolution scans (300+ DPI)

---

## 🆘 Need Help?

1. **Run tests:** `python test_ollama_system.py`
2. **Check logs:** See console output for detailed errors
3. **Verify installation:** All components installed?
4. **Read documentation:** README_OLLAMA.md (this file)

---

## ✅ Quick Checklist

Before using:
- [ ] Ollama installed and running
- [ ] llama3.2 model downloaded
- [ ] Python dependencies installed
- [ ] Poppler installed and in PATH
- [ ] GPU drivers updated (if using GPU)
- [ ] Tests pass (`python test_ollama_system.py`)

---

## 🎉 You're Ready!

Run the system:
```bash
start_ollama.bat  # Windows
python app_ollama.py  # Manual
```

Open: **http://localhost:5000**

Happy grading! 🚀
