# ✅ Quick Start Checklist

## Before You Start

### 1. Install Ollama
- [ ] Download from: https://ollama.ai
- [ ] Install for your OS (Windows/Mac/Linux)
- [ ] Open terminal and run: `ollama pull llama3.1:latest`
- [ ] Verify: `ollama list` (should show llama3.1)

### 2. Install Python Dependencies
```bash
pip install -r requirements_complete.txt
```

- [ ] Flask installed
- [ ] PyPDF2 installed
- [ ] FPDF2 installed
- [ ] DeepSeek OCR dependencies installed
- [ ] ReportLab installed

### 3. Test the System
```bash
python test_complete_system_new.py
```

- [ ] All 8 tests passed
- [ ] Ollama working
- [ ] OCR ready
- [ ] PDF generation working

## Running the System

### Option 1: Windows Batch File
```bash
start_complete_system.bat
```

### Option 2: Direct Python
```bash
python app_ollama_complete.py
```

- [ ] Server started successfully
- [ ] No errors in console
- [ ] Can access http://localhost:5000

## Using the System

### Step 1: Upload Question Paper
- [ ] Click "Upload Question Paper"
- [ ] Select your question PDF
- [ ] Wait for "✅ Uploaded successfully"
- [ ] Check console for extracted questions

### Step 2: Upload Answer Key
- [ ] Click "Upload Answer Key"
- [ ] Select your answer key PDF
- [ ] Wait for "✅ Uploaded successfully"
- [ ] Check console for extracted answers

### Step 3: Evaluate Student Paper
- [ ] Click "Evaluate Student Paper"
- [ ] Select handwritten student PDF (from phone camera)
- [ ] Wait for processing (may take 1-3 minutes)
- [ ] Watch console for progress:
  - OCR extraction
  - Text PDF creation
  - Text extraction
  - Ollama evaluation
  - Result PDF generation

### Step 4: Download Results
- [ ] Click "Download Result PDF"
- [ ] Open the PDF
- [ ] Check marks, grades, and feedback

## Common Issues & Solutions

### ❌ "Ollama is not installed"
**Solution:**
```bash
# Install from https://ollama.ai
ollama pull llama3.1:latest
```

### ❌ "No text extracted from student paper"
**Possible causes:**
- Handwriting too messy
- Image quality too low
- PDF corrupted

**Solutions:**
- Re-scan with better lighting
- Use 300+ DPI
- Ensure good contrast

### ❌ "Import Error: No module named 'fpdf'"
**Solution:**
```bash
pip install fpdf2
```

### ❌ "CUDA not available"
**Impact:** Slower OCR (but still works)
**Optional fix:**
```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

### ❌ Evaluation is very slow
**Solutions:**
1. Use lighter model: Edit `app_ollama_complete.py`
   ```python
   ollama_evaluator = OllamaEvaluator(model_name="phi3:latest")
   ```
2. Reduce question count for testing
3. Enable GPU for Ollama (automatic if available)

## Verification Checklist

### Files Created After Running:
- [ ] `uploads/` directory exists
- [ ] `results/` directory exists
- [ ] PDFs appear in `uploads/` after upload
- [ ] Result PDFs appear in `results/` after evaluation

### Console Output Should Show:
- [ ] "✅ System initialized successfully"
- [ ] "✅ Ollama ready with model: llama3.1"
- [ ] "📝 Extracting handwritten text from..."
- [ ] "📄 Creating text-based PDF..."
- [ ] "🎓 Starting Concept-Based Evaluation..."
- [ ] "✅ Result PDF generated successfully"

## Performance Expectations

### OCR Processing Time:
- **With GPU:** 2-5 seconds per page
- **With CPU:** 10-20 seconds per page

### Evaluation Time (per question):
- **llama3.1:** 5-10 seconds
- **phi3:** 2-3 seconds
- **mistral:** 3-5 seconds

### Total Time (10 questions):
- **OCR (3 pages):** 30-60 seconds
- **Evaluation (10 questions):** 50-100 seconds
- **Total:** ~2-3 minutes

## Tips for Best Results

### Question Paper Format:
```
Q1. What is photosynthesis? (5 marks)
Q2. Explain Newton's laws. (10 marks)
```

### Answer Key Format:
```
Answer 1: Photosynthesis is the process...
Answer 2: Newton's laws state that...
```

### Student Paper:
- Clear handwriting
- Numbered answers (1, 2, 3 or Q1, Q2, Q3)
- Good lighting when photographing
- Flat paper (no wrinkles)

## Final Check

Before evaluation, ensure:
- [x] Ollama is running (`ollama list` works)
- [x] Question paper uploaded (shows question count)
- [x] Answer key uploaded (shows answer count)
- [x] Student paper is clear and readable
- [x] Internet connection stable (for model downloads)

## Success Indicators

✅ **System Working Correctly If:**
1. Question paper shows extracted questions with marks
2. Answer key shows extracted answers
3. Student paper creates text-based PDF in uploads/
4. Evaluation completes without errors
5. Result PDF shows marks, grades, and feedback
6. Console shows no error messages

## Need Help?

1. Check `COMPLETE_SYSTEM_GUIDE.md` for detailed instructions
2. Run `python test_complete_system_new.py` to diagnose issues
3. Check console output for error messages
4. Verify all dependencies are installed
5. Ensure Ollama is running properly

---

**You're all set! Start evaluating papers with AI! 🚀**
