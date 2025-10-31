# 📖 User Guide - AI Answer Evaluation System

## Table of Contents
1. [Getting Started](#getting-started)
2. [Preparing Documents](#preparing-documents)
3. [Using the Web Interface](#using-the-web-interface)
4. [Understanding Results](#understanding-results)
5. [Tips for Best Results](#tips-for-best-results)
6. [Frequently Asked Questions](#frequently-asked-questions)

---

## Getting Started

### First Time Setup

1. **Run Setup Script**
   ```bash
   # Windows
   setup.bat
   
   # Linux/Mac
   chmod +x setup.sh
   ./setup.sh
   ```

2. **Wait for Installation**
   - Python packages will be installed
   - DeepSeek-OCR model will be downloaded (~6.7GB)
   - This may take 10-30 minutes depending on internet speed

3. **Start the Application**
   ```bash
   # Windows
   start.bat
   
   # Linux/Mac
   ./start.sh
   ```

4. **Access Web Interface**
   - Open browser: http://localhost:5000
   - You should see the main dashboard

---

## Preparing Documents

### 1. Question Paper Format

**Required Format:**
```
Q1. What is photosynthesis? (5 marks)

Q2. Explain the water cycle with a diagram. (10 marks)

Q3. List five renewable energy sources. (5 marks)
```

**Important Points:**
- ✅ Each question must have a number: Q1, Q2, etc.
- ✅ Marks must be in parentheses: (5 marks) or [5 marks]
- ✅ Can be typed or printed PDF
- ❌ Don't use inconsistent numbering
- ❌ Don't forget to include marks

**Acceptable Variations:**
```
Q1. Question text? (5 marks)
1. Question text? (5 marks)
Question 1. Question text? (5 marks)
Q1: Question text? (5 M)
```

### 2. Answer Key Format

**Required Format:**
```
Answer 1: Photosynthesis is the process by which green plants 
convert light energy into chemical energy. It occurs in 
chloroplasts using chlorophyll...

Answer 2: The water cycle is the continuous movement of water 
on, above, and below the Earth's surface. It includes 
evaporation, condensation, precipitation, and collection...

Answer 3: Five types of renewable energy sources are:
1) Solar energy
2) Wind energy
3) Hydroelectric power
4) Geothermal energy
5) Biomass energy
```

**Important Points:**
- ✅ Number answers to match questions
- ✅ Provide complete, detailed answers
- ✅ Can be typed or printed PDF
- ✅ More detailed = better evaluation accuracy
- ❌ Don't skip answers
- ❌ Don't use vague or incomplete answers

**Acceptable Variations:**
```
Answer 1: Answer text...
Ans 1: Answer text...
A1: Answer text...
Q1. Answer: Answer text...
1. Answer text...
```

### 3. Student Answer Paper Format

**Requirements:**
- ✅ Can be handwritten or typed
- ✅ PDF format required
- ✅ Clear, legible handwriting
- ✅ Number answers to match questions
- ✅ Good scan quality (300 DPI recommended)

**For Best OCR Results:**
- Use dark ink (black or blue)
- Write clearly and avoid cursive if possible
- Ensure good lighting when scanning
- Avoid shadows or glare
- Keep pages straight (not skewed)

---

## Using the Web Interface

### Step 1: Upload Question Paper 📋

1. **Click on "Upload Question Paper" card**
2. **Select your question paper PDF**
   - Click the upload area OR
   - Drag and drop the PDF file
3. **Click "Upload Question Paper" button**
4. **Wait for processing**
   - System extracts questions and marks
   - Status will show "Loaded ✓" when complete
5. **Verify**
   - Check message showing number of questions found
   - Example: "✓ Question paper uploaded successfully! Found 10 questions."

**Troubleshooting:**
- If extraction fails, check PDF format
- Ensure marks are clearly indicated
- Try re-scanning if PDF quality is poor

### Step 2: Upload Answer Key ✅

1. **Click on "Upload Answer Key" card**
2. **Select your answer key PDF**
3. **Click "Upload Answer Key" button**
4. **Wait for processing**
   - System extracts correct answers
   - Status will show "Loaded ✓" when complete
5. **Verify**
   - Check message showing number of answers found
   - Should match number of questions

**Troubleshooting:**
- If fewer answers extracted than expected, check format
- Ensure all answers are clearly numbered
- Provide more detailed answers for better comparison

### Step 3: Evaluate Student Paper ✍️

1. **Ensure both question paper and answer key are loaded**
   - Both status indicators should show "Loaded ✓"
   - Evaluate button will be enabled
2. **Click on "Evaluate Student Paper" card**
3. **Select student's answer script PDF**
4. **Click "Evaluate Paper" button**
5. **Wait for evaluation**
   - This may take 1-5 minutes depending on:
     - Number of pages
     - GPU availability
     - Handwriting complexity
6. **View results**
   - Results will appear below
   - Scroll down to see detailed breakdown

**Progress Messages:**
```
📄 Converting PDF to images...
📄 Processing page 1/5...
🧠 Using DeepSeek-OCR for handwritten text extraction...
✅ Successfully extracted text from 5 pages
🔍 Comparing with answer key...
✅ Evaluation completed successfully!
```

---

## Understanding Results

### Summary Section

**Display:**
```
Total Marks: 50
Obtained Marks: 42.5
Percentage: 85.0%
Grade: A
```

**Grade Scale:**
- A+ : 90-100%
- A  : 80-89%
- B+ : 70-79%
- B  : 60-69%
- C  : 50-59%
- D  : 40-49%
- F  : Below 40%

### Question-wise Breakdown

**Table Columns:**

1. **Q. No.**: Question number
2. **Max Marks**: Total marks for this question
3. **Obtained**: Marks awarded to student
4. **Percentage**: (Obtained / Max) × 100
5. **Remarks**: Performance feedback

**Remarks Categories:**
- **Excellent** (90-100%): Perfect or near-perfect answer
- **Very Good** (75-89%): Most key points covered
- **Good** (60-74%): Major points covered
- **Average** (50-59%): Basic understanding shown
- **Needs Improvement** (Below 50%): Significant gaps

**Color Coding:**
- 🟢 Green (80%+): Good performance
- 🟡 Yellow (60-79%): Satisfactory
- 🔴 Red (Below 50%): Needs improvement

### Downloading Results

1. **Click "Download Result PDF" button**
2. **PDF will download automatically**
3. **Find it in your Downloads folder**

**PDF Contents:**
- Evaluation date and time
- Summary statistics
- Grade
- Question-wise breakdown table
- Professional formatting

---

## Tips for Best Results

### For Teachers/Evaluators

1. **Question Paper:**
   - Be clear with marks allocation
   - Use consistent question numbering
   - Ensure PDF is searchable or well-scanned

2. **Answer Key:**
   - Provide comprehensive answers
   - Include all key points
   - Use clear language
   - More detail = better evaluation

3. **First Use:**
   - Test with a sample paper first
   - Verify extraction accuracy
   - Adjust if needed

### For Students

1. **Handwriting:**
   - Write clearly and legibly
   - Use dark ink (black or blue)
   - Avoid extremely cursive writing
   - Maintain consistent letter size

2. **Answers:**
   - Number answers clearly
   - Match question numbers
   - Write complete answers
   - Organize your thoughts

3. **Scanning:**
   - Use 300 DPI or higher
   - Ensure good lighting
   - Avoid shadows and glare
   - Keep pages straight
   - Use scanner or high-quality phone camera

### For Best OCR Accuracy

1. **PDF Quality:**
   - Higher resolution = better recognition
   - Clean, clear scans
   - No coffee stains or creases
   - Proper contrast

2. **Text:**
   - Dark text on white background
   - Avoid very light pencil
   - No multi-color highlighting over text
   - Clean margins

3. **Format:**
   - Portrait orientation
   - Standard paper size (A4/Letter)
   - All text within page margins
   - No cut-off text

---

## Frequently Asked Questions

### General Questions

**Q: How long does evaluation take?**
A: Typically 1-5 minutes per paper, depending on:
- Number of pages (1 page ≈ 5-10 seconds with GPU)
- GPU availability (CPU is much slower)
- Handwriting complexity

**Q: Can I evaluate multiple papers at once?**
A: Currently, papers are evaluated one at a time. Upload and evaluate each paper individually.

**Q: How accurate is the evaluation?**
A: Accuracy depends on:
- Answer key quality (more detailed = more accurate)
- Handwriting legibility (clear = better)
- Question-answer match
- Typical accuracy: 80-95% correlation with human grading

**Q: Can I use this for math or equations?**
A: DeepSeek-OCR can recognize mathematical symbols, but complex equations may have lower accuracy. Best for text-based answers.

### Technical Questions

**Q: Do I need GPU?**
A: GPU is highly recommended but not required:
- With GPU: 5-10 seconds per page
- Without GPU: 30-60 seconds per page

**Q: How much storage is needed?**
A: Approximately:
- Model: 6.7 GB (one-time download)
- Per evaluation: 5-50 MB
- Total recommended: 10+ GB free space

**Q: Can I run this offline?**
A: Yes! After initial model download, everything runs locally. No internet needed.

**Q: What if GPU memory is insufficient?**
A: Edit `deepseek_ocr.py`:
```python
base_size=640,  # Reduce from 1024
crop_mode=False  # Disable tiling
```

### Usage Questions

**Q: Can I edit the grading scale?**
A: Yes! Edit `config.py` to modify:
- Similarity thresholds
- Grade boundaries
- Marking percentages
- Feedback messages

**Q: What if questions aren't detected?**
A: Check that:
- Questions are numbered clearly
- Marks are in parentheses
- PDF is not corrupted
- Text is readable

**Q: What if student answers aren't detected?**
A: Ensure:
- Answers are numbered
- Handwriting is legible
- Good scan quality
- Proper lighting and contrast

**Q: Can I customize the evaluation algorithm?**
A: Yes! Modify weights in `config.py`:
```python
SIMILARITY_WEIGHTS = {
    'cosine': 0.35,
    'sequence': 0.25,
    'word_overlap': 0.25,
    'keyword': 0.15
}
```

### Error Handling

**Q: What if OCR fails?**
A: System automatically falls back to Tesseract OCR. If both fail:
- Check PDF quality
- Verify handwriting legibility
- Try re-scanning at higher DPI

**Q: What if evaluation seems incorrect?**
A: Check:
- Answer key completeness
- Question-answer numbering match
- Review detailed similarity scores
- Adjust grading scale if needed

**Q: Can I contest the marks?**
A: This is an AI-assisted tool. Final decisions should involve human review. Use results as guidance, not absolute truth.

---

## Best Practices

### Before Evaluation

✅ Test with sample papers first
✅ Verify question and answer extraction
✅ Ensure good PDF quality
✅ Check GPU availability
✅ Clear browser cache if issues occur

### During Evaluation

✅ Upload papers in order (Question → Answer → Student)
✅ Wait for each upload to complete
✅ Monitor console for any errors
✅ Don't refresh page during processing

### After Evaluation

✅ Review results carefully
✅ Download PDF reports
✅ Keep original papers for reference
✅ Use results as guidance with human judgment

---

## Support & Contact

For issues or questions:

1. **Check documentation:**
   - README.md
   - INSTALLATION.md
   - This User Guide

2. **Common issues:**
   - See Troubleshooting sections
   - Check FAQ above

3. **Technical problems:**
   - Verify all dependencies installed
   - Run test_setup.py
   - Check console for error messages

---

**Remember:** This is an AI-assisted evaluation tool. Always apply human judgment and review results before final grading!

**Happy Evaluating! 📝✨**
