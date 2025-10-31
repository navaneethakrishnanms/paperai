# Troubleshooting Guide: 0 Questions/0 Answers Issue

## Problem
The system shows "0 questions" and "0 answers" after uploading PDFs.

## Common Causes

### 1. **Scanned/Image PDFs** (Most Likely)
If your PDFs are images or scans, PyPDF2 cannot extract text from them.

**Solution:**
- The PDFs need OCR (Optical Character Recognition)
- Use Tesseract OCR or DeepSeek-OCR

### 2. **Wrong Format** 
Your PDFs might not match the expected format patterns.

**Expected Formats:**

#### Question Paper Format:
```
Q1. What is Python? (5 marks)
Q2. Explain machine learning? (10 marks)

OR

1. What is Python? (5 marks)
2. Explain machine learning? (10 marks)
```

#### Answer Key Format:
```
Answer 1: Python is a programming language...
Answer 2: Machine learning is a subset of AI...

OR

Q1. Answer: Python is a programming language...
Q2. Answer: Machine learning is a subset of AI...
```

### 3. **ChromaDB Not Storing Data**
Data extraction works but storage fails.

## Diagnostic Steps

### Step 1: View PDF Contents
Run this command:
```bash
python view_pdf_content.py
```

This will show:
- ✅ If text can be extracted from PDFs
- ❌ If PDFs are images/scans (no embedded text)

### Step 2: Check Database
Run this command:
```bash
python debug_db.py
```

This will show:
- How many questions/answers are stored
- The actual content stored in ChromaDB

### Step 3: Test Extraction Patterns
Run this command:
```bash
python test_extraction.py
```

This will show:
- Raw text extracted
- Questions/answers parsed
- Which patterns matched

### Step 4: All-in-One Diagnosis
Run this command:
```bash
diagnose.bat
```

Runs all diagnostic tests in sequence.

## Quick Fixes

### Fix 1: If PDFs are Scanned (No Text Found)

**Option A: Install Tesseract OCR**
1. Download from: https://github.com/UB-Mannheim/tesseract/wiki
2. Install it
3. Add to PATH
4. Restart the app

**Option B: Use DeepSeek-OCR** (for handwriting)
Already integrated in the app but requires GPU.

### Fix 2: If Format Doesn't Match

**Modify the PDF format to match expected patterns:**

**Question Paper:**
```
Q1. [Question text here] (5 marks)
Q2. [Question text here] (10 marks)
```

**Answer Key:**
```
Answer 1: [Answer text here]
Answer 2: [Answer text here]
```

**OR** modify regex patterns in `pdf_processor.py`:

```python
# Around line 87 in pdf_processor.py
patterns = [
    r'Q[\s]*(\d+)[\.\):\s]+(.*?)\s*[\(\[](\d+)\s*marks?[\)\]]',
    # Add your custom pattern here
]
```

### Fix 3: Clear and Reload

If you uploaded wrong files:

```python
# Run this in Python console
from vector_db_manager import VectorDBManager
db = VectorDBManager()
db.clear_all_data()
```

Then re-upload correct PDFs.

## Testing Your PDFs

### Manual Pattern Check

For **question.pdf**, check if it contains:
- Question numbers (Q1, Q2, or 1., 2.)
- Question text
- Marks in parentheses: (5 marks), [10 marks]

For **Ans.pdf**, check if it contains:
- Answer numbers (Answer 1, Ans 1, Q1)
- Answer text

## Still Not Working?

### Debug Output

When you upload PDFs, check the console output for:
```
✅ Extracted N questions from question paper
✅ Extracted N answers from answer key
```

If you see:
```
✅ Extracted 0 questions from question paper
```

The extraction patterns didn't match. You need to:
1. View the actual PDF text (Step 1)
2. Adjust the regex patterns
3. Or reformat your PDFs

## Contact Pattern Examples

Share the first few lines of your PDF text so patterns can be adjusted:

**Good Question Paper Example:**
```
Q1. What is AI? (5 marks)
Q2. Explain neural networks? (10 marks)
```

**Good Answer Key Example:**
```
Answer 1: AI stands for Artificial Intelligence...
Answer 2: Neural networks are computing systems...
```

## Quick Reference Commands

```bash
# View PDF contents
python view_pdf_content.py

# Check database
python debug_db.py

# Test extraction
python test_extraction.py

# Full diagnosis
diagnose.bat
```

## Files Created for Debugging

1. `view_pdf_content.py` - Shows actual PDF text
2. `debug_db.py` - Shows database contents
3. `test_extraction.py` - Tests extraction with patterns
4. `diagnose.bat` - Runs all tests

---

**Next Step:** Run `python view_pdf_content.py` to see what's in your PDFs!
