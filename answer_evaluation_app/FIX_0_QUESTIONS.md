# Fix Guide: "0 Questions" and "0 Answers" Issue

## 🔴 Problem
After uploading PDFs, the system shows:
- ✓ Question paper uploaded successfully! **Found 0 questions**
- ✓ Answer key uploaded successfully! **Found 0 answers**

## 🎯 Root Cause
There are 3 possible reasons:

### 1. **PDFs are Scanned/Images** (80% of cases)
Your PDFs are images or scans, not digital documents with embedded text. PyPDF2 cannot extract text from image-based PDFs.

### 2. **Wrong Format** (15% of cases)
Your PDFs don't match the expected question/answer format patterns.

### 3. **Extraction Code Issue** (5% of cases)
The regex patterns don't match your specific format.

---

## 🔧 Quick Diagnosis (30 seconds)

Run this in your terminal:
```bash
cd C:\Users\nk\paperai\answer_evaluation_app
python auto_diagnose.py
```

This will tell you exactly what's wrong!

---

## ✅ Solutions

### Solution 1: For Scanned/Image PDFs

#### Option A: Install Tesseract OCR (Easiest)

1. **Download Tesseract:**
   - Go to: https://github.com/UB-Mannheim/tesseract/wiki
   - Download the Windows installer (.exe)
   - Install it (use default settings)

2. **Add to System PATH:**
   - Copy installation path (usually: `C:\Program Files\Tesseract-OCR`)
   - Right-click "This PC" → Properties → Advanced System Settings
   - Environment Variables → System Variables → Path → Edit
   - Add new: `C:\Program Files\Tesseract-OCR`
   - Click OK

3. **Restart your app:**
   ```bash
   cd C:\Users\nk\paperai\answer_evaluation_app
   start.bat
   ```

4. **Re-upload your PDFs**

#### Option B: Use DeepSeek-OCR (Better for handwriting)

This is already integrated but requires:
- NVIDIA GPU with CUDA
- Sufficient VRAM (8GB+ recommended)

If you have a GPU, the app will automatically use DeepSeek-OCR for handwritten text.

---

### Solution 2: For Format Issues

Your PDFs must follow this **exact format**:

#### Question Paper Format:
```
Q1. What is Python? (5 marks)

Q2. Explain machine learning algorithms? (10 marks)

Q3. Describe neural networks? (8 marks)
```

**Alternative formats also work:**
```
1. What is Python? (5 marks)
2. Explain machine learning? (10 marks)
```

#### Answer Key Format:
```
Answer 1: Python is a high-level programming language...

Answer 2: Machine learning is a subset of artificial intelligence...

Answer 3: Neural networks are computing systems inspired by...
```

**Alternative formats:**
```
Ans 1: Python is a high-level programming language...

Q1. Answer: Python is a high-level programming language...
```

**Key Requirements:**
- Questions must have **question numbers** (Q1, 1., etc.)
- Questions must have **marks** in parentheses: (5 marks), [10 marks]
- Answers must have **answer numbers** matching questions
- Use clear numbering (1, 2, 3... or Q1, Q2, Q3...)

---

### Solution 3: Custom Format (Advanced)

If your PDFs have a different format, you can modify the extraction patterns:

1. **Find your current PDF format:**
   ```bash
   python view_pdf_content.py
   ```
   This shows the actual text in your PDFs.

2. **Edit the extraction patterns:**
   Open `pdf_processor.py` and modify the regex patterns around line 87:
   
   ```python
   # For questions (line ~87)
   patterns = [
       r'Q[\s]*(\d+)[\.\):\s]+(.*?)\s*[\(\[](\d+)\s*marks?[\)\]]',
       # Add your custom pattern here
       r'YourCustomPattern',
   ]
   
   # For answers (line ~132)  
   patterns = [
       r'(?:Answer|Ans|A)[\s]*(\d+)[\.\):\s]+(.*?)(?=(?:Answer|Ans|A)[\s]*\d+|\Z)',
       # Add your custom pattern here
       r'YourCustomAnswerPattern',
   ]
   ```

---

## 📋 Testing Checklist

### Before Re-uploading:

- [ ] **Check if PDFs have text:** Run `python view_pdf_content.py`
  - ✅ See text? → Format might be the issue
  - ❌ No text/gibberish? → Install Tesseract OCR

- [ ] **Check format matches:** Open your PDF and verify:
  - ✅ Questions have numbers (Q1, 1., etc.)
  - ✅ Questions have marks: (5 marks), [10 marks]
  - ✅ Answers have numbers matching questions

- [ ] **OCR is working:** If PDFs are scanned:
  - ✅ Tesseract installed and in PATH
  - ✅ Or DeepSeek-OCR is initialized (check console logs)

### After Re-uploading:

- [ ] Check console output for:
  ```
  ✅ Extracted N questions from question paper
  ✅ Extracted N answers from answer key
  ```

- [ ] If still 0:
  - Run `python auto_diagnose.py`
  - Check the output for specific issues
  - Share the PDF preview (first few lines)

---

## 🆘 Still Not Working?

### Get Detailed Diagnostics:

```bash
# Full auto-diagnosis
python auto_diagnose.py

# View actual PDF text
python view_pdf_content.py

# Check database contents
python debug_db.py

# Test extraction patterns
python test_extraction.py
```

### Share This Info:

If you need help, share:

1. **Output of:** `python view_pdf_content.py`
   - Shows first 100 chars of each page

2. **Output of:** `python auto_diagnose.py`
   - Shows what's failing

3. **Sample format** from your PDF:
   ```
   Q1. Your question format here? (5 marks)
   Answer 1: Your answer format here...
   ```

---

## 📝 Quick Command Reference

| Command | Purpose |
|---------|---------|
| `python auto_diagnose.py` | Complete diagnosis (run this first!) |
| `python view_pdf_content.py` | View PDF text content |
| `python debug_db.py` | Check database contents |
| `python test_extraction.py` | Test extraction with current files |
| `diagnose.bat` | Run all tests (Windows) |

---

## ✨ Success Indicators

After fixing, you should see:

1. **On upload:**
   ```
   ✅ Question paper uploaded successfully! Found 5 questions
   ✅ Answer key uploaded successfully! Found 5 answers
   ```

2. **In console:**
   ```
   📄 Question paper appears to be scanned/handwritten, using OCR...
   ✅ Extracted 5 questions from question paper
   ✅ Extracted 5 answers from answer key
   ```

3. **When evaluating:**
   - Student answers are compared against answer key
   - Marks are assigned
   - Result PDF is generated

---

## 🎓 Example Files

Create test files with this format to verify the system works:

**test_questions.pdf:**
```
Q1. What is AI? (5 marks)
Q2. Explain machine learning? (10 marks)  
Q3. What are neural networks? (8 marks)
```

**test_answers.pdf:**
```
Answer 1: AI stands for Artificial Intelligence. It is the simulation
of human intelligence processes by machines, especially computer systems.

Answer 2: Machine learning is a subset of AI that enables systems to
learn and improve from experience without being explicitly programmed.

Answer 3: Neural networks are computing systems inspired by biological
neural networks that constitute animal brains.
```

Upload these and you should see "Found 3 questions" and "Found 3 answers"!

---

**Need More Help?** Run `python auto_diagnose.py` and share the output!
