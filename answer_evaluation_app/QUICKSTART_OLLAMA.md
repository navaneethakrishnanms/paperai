# 🚀 Quick Start Guide - Ollama Integrated Answer Evaluation

## What This System Does

✅ Extracts handwritten text from student answer papers (using **DeepSeek-OCR**)  
✅ Evaluates answers based on **concept understanding** (using **Ollama LLM**)  
✅ Generates detailed PDF reports with marks and feedback  

---

## 📥 Installation (One-Time Setup)

### 1. Install Ollama
```bash
# Visit https://ollama.ai and download for your OS
# After installation:
ollama pull llama3.1:latest
```

### 2. Install Python Dependencies
```bash
# Install PyTorch with CUDA (for GPU)
pip install torch==2.1.1 torchvision==0.16.1 --index-url https://download.pytorch.org/whl/cu118

# Install all other dependencies
pip install -r requirements_ollama_full.txt
```

### 3. Install Poppler (for PDF processing)
```bash
# Windows: Run this script
fix_poppler.bat

# Linux:
sudo apt-get install poppler-utils

# Mac:
brew install poppler
```

---

## 🚀 Running the Application

### Windows
```bash
start_ollama_integrated.bat
```

### Linux/Mac
```bash
python app_ollama_integrated.py
```

Access at: **http://localhost:5000**

---

## 📝 Usage Workflow

### Step 1: Upload Question Paper
- Click "Upload Question Paper"
- Select PDF (typed or scanned)
- System extracts questions with marks

### Step 2: Upload Answer Key
- Click "Upload Answer Key"  
- Select PDF with correct answers
- System stores answers

### Step 3: Evaluate Student Paper
- Click "Evaluate Student Paper"
- Enter student name
- Upload handwritten answer PDF (from phone/scanner)
- System:
  1. Extracts handwritten text using DeepSeek-OCR
  2. Evaluates using Ollama LLM (concept-based)
  3. Generates detailed PDF report

### Step 4: Download Results
- View results on screen
- Download PDF report
- Download OCR-extracted text PDF

---

## 🧪 Testing the System

```bash
# Run system test
python test_complete_system.py

# Should show:
# ✅ Python Packages
# ✅ CUDA/GPU
# ✅ Ollama
# ✅ Poppler
# ✅ DeepSeek-OCR
# ✅ Vector Database
# ✅ Ollama Evaluator
# ✅ PDF Generation
```

---

## 📋 Question Paper Format Examples

**Good formats:**
```
Q1. Explain photosynthesis. (5 marks)
Question 2: Describe DNA structure. (10 marks)
(i) Define energy. (3 marks)
```

**Answer Key format:**
```
Answer 1: Photosynthesis is the process by which...
A2: DNA has a double helix structure...
(i) Energy is the capacity to do work...
```

---

## ⚙️ Configuration

### Change Ollama Model
Edit `app_ollama_integrated.py`:
```python
ollama_evaluator = OllamaEvaluator(model_name="mistral")  # or "phi", "codellama"
```

### Available Models
- `llama3.1:latest` - Best quality (slower)
- `mistral` - Good balance
- `phi` - Fastest (smaller model)

---

## 🔧 Troubleshooting

### Ollama not found
```bash
# Install from: https://ollama.ai
ollama pull llama3.1:latest
```

### Poppler error
```bash
# Windows:
fix_poppler.bat

# Linux:
sudo apt-get install poppler-utils
```

### Poor OCR results
- Ensure good image quality
- Use 300+ DPI
- Clear handwriting
- Good lighting

### Slow evaluation
- Use smaller model: `phi`
- Check GPU is being used
- Reduce OCR quality settings

---

## 📚 Detailed Documentation

- **Complete Guide**: `COMPLETE_GUIDE_OLLAMA.md`
- **Troubleshooting**: `TROUBLESHOOTING.md`
- **Architecture**: `ARCHITECTURE.md`

---

## 🎯 Key Files

- `app_ollama_integrated.py` - Main Flask application
- `deepseek_ocr.py` - Handwritten text extraction
- `ollama_evaluator.py` - Concept-based evaluation
- `pdf_generator.py` - Result PDF generation
- `vector_db_manager.py` - Question/Answer storage

---

## ✅ System Requirements

- **Python**: 3.9+
- **GPU**: NVIDIA GPU with 6GB+ VRAM (optional but recommended)
- **RAM**: 16GB+
- **Storage**: 10GB+ (for models)
- **OS**: Windows/Linux/Mac

---

## 🎓 How It Works

```
Student Paper (Handwritten PDF)
         ↓
DeepSeek-OCR (Extract Text)
         ↓
Parse Student Answers
         ↓
For each question:
  → Question + Answer Key + Student Answer
  → Send to Ollama LLM
  → Get: Marks + Feedback + Concept Score
         ↓
Generate Result PDF
         ↓
Download & Review
```

---

## 🔐 Privacy

- ✅ All processing is local
- ✅ No data sent to external servers
- ✅ Student data stays private

---

## 💡 Tips

1. Test with sample papers first
2. Ensure good quality scans/photos
3. Review AI results before final grading
4. Customize grading scale as needed
5. Use GPU for faster processing

---

## 📞 Need Help?

1. Read `COMPLETE_GUIDE_OLLAMA.md`
2. Run `python test_complete_system.py`
3. Check console logs for errors
4. Verify all dependencies installed

---

**Ready to start? Run `start_ollama_integrated.bat` and access http://localhost:5000**
