# 🎯 Quick Start Guide

## One-Minute Setup

### Windows
```bash
# 1. Run setup (first time only)
setup.bat

# 2. Start application
start.bat

# 3. Open browser
http://localhost:5000
```

### Linux/Mac
```bash
# 1. Make scripts executable
chmod +x setup.sh start.sh

# 2. Run setup (first time only)
./setup.sh

# 3. Start application
./start.sh

# 4. Open browser
http://localhost:5000
```

---

## Three-Step Usage

### 1️⃣ Upload Question Paper
- Click "Upload Question Paper"
- Select PDF with format: `Q1. Question? (5 marks)`
- Wait for processing

### 2️⃣ Upload Answer Key
- Click "Upload Answer Key"
- Select PDF with format: `Answer 1: Text...`
- Wait for processing

### 3️⃣ Evaluate Student Paper
- Click "Evaluate Student Paper"
- Select student's handwritten/typed PDF
- Wait 1-5 minutes for results
- Download PDF report

---

## System Requirements

### Minimum
- Python 3.9+
- 16GB RAM
- 10GB disk space
- Windows 10/Linux/macOS

### Recommended
- Python 3.11
- NVIDIA GPU (6GB+ VRAM)
- CUDA 11.8 or 12.1
- 16GB+ RAM
- 20GB disk space

---

## Key Features

✅ **Handwritten Text Recognition** - DeepSeek-OCR
✅ **Automated Marking** - AI similarity matching
✅ **PDF Reports** - Detailed question-wise breakdown
✅ **Vector Database** - Efficient answer storage
✅ **Web Interface** - Easy to use
✅ **Offline Operation** - No internet needed after setup

---

## What You Need

### Question Paper PDF
```
Q1. What is photosynthesis? (5 marks)
Q2. Explain water cycle. (10 marks)
```

### Answer Key PDF
```
Answer 1: Photosynthesis is...
Answer 2: Water cycle is...
```

### Student Answer PDF
- Handwritten or typed
- Numbered answers
- Clear, legible text
- Good scan quality (300 DPI)

---

## Evaluation Process

1. **Text Extraction**
   - DeepSeek-OCR recognizes handwriting
   - Extracts text from all pages
   - ~5-10 seconds per page with GPU

2. **Answer Comparison**
   - TF-IDF + Cosine Similarity
   - Sequence Matching
   - Word Overlap Analysis
   - Keyword Matching

3. **Marking**
   - 90%+ similarity → Full marks
   - 80-90% → 95% marks
   - Graduated scale down to 10%

4. **Report Generation**
   - Summary: Total, Obtained, Percentage, Grade
   - Question-wise breakdown
   - Performance remarks
   - Professional PDF format

---

## Grading Scale

| Percentage | Grade | Remarks |
|-----------|-------|---------|
| 90-100% | A+ | Excellent |
| 80-89% | A | Very Good |
| 70-79% | B+ | Good |
| 60-69% | B | Satisfactory |
| 50-59% | C | Average |
| 40-49% | D | Below Average |
| 0-39% | F | Needs Improvement |

---

## File Locations

```
answer_evaluation_app/
├── uploads/          # Uploaded PDFs stored here
├── results/          # Generated reports saved here
├── vector_db/        # Answer database
└── output/           # OCR temporary files
```

---

## Common Issues & Solutions

### GPU Not Found
```bash
# Check GPU
nvidia-smi

# Reinstall PyTorch with CUDA
pip install torch --index-url https://download.pytorch.org/whl/cu118
```

### Poppler Not Found
```bash
# Windows: Add to PATH
C:\Program Files\poppler\Library\bin

# Linux
sudo apt-get install poppler-utils
```

### Port 5000 In Use
```python
# Edit app.py
app.run(port=5001)  # Change port
```

### Slow Processing
- Verify GPU is being used
- Reduce PDF resolution
- Close other GPU apps
- Check `nvidia-smi` for utilization

---

## Performance Tips

### For Best OCR Results
- Use 300+ DPI scans
- Dark ink on white paper
- Clear, legible handwriting
- Good lighting, no shadows
- Straight pages (not skewed)

### For Better Accuracy
- Detailed answer keys
- Complete student answers
- Consistent numbering
- Match question-answer numbers
- Clean PDF quality

---

## Documentation

- **README.md** - Overview and features
- **INSTALLATION.md** - Detailed setup instructions
- **USER_GUIDE.md** - Complete usage guide
- **config.py** - Customization options

---

## Test Your Setup

```bash
# Run verification test
python test_setup.py

# Should show all tests passing:
# ✅ Package Imports: PASSED
# ✅ GPU Setup: PASSED
# ✅ System Dependencies: PASSED
# ✅ Directory Structure: PASSED
# ✅ Required Files: PASSED
# ✅ DeepSeek-OCR Model: PASSED
```

---

## Customization

### Modify Grading Scale
Edit `config.py`:
```python
GRADING_SCALE = {
    0.90: 1.00,   # 90%+ similarity → 100% marks
    0.80: 0.95,   # 80-90% → 95% marks
    # ... customize as needed
}
```

### Adjust Similarity Weights
```python
SIMILARITY_WEIGHTS = {
    'cosine': 0.35,
    'sequence': 0.25,
    'word_overlap': 0.25,
    'keyword': 0.15
}
```

### Change Grade Thresholds
```python
GRADE_THRESHOLDS = {
    90: 'A+',
    80: 'A',
    # ... customize as needed
}
```

---

## Support

### Getting Help
1. Check documentation (README, INSTALLATION, USER_GUIDE)
2. Run test_setup.py to verify installation
3. Check console output for errors
4. Review FAQ in USER_GUIDE.md

### Common Questions
- **Takes too long?** Check GPU availability
- **Wrong marks?** Review answer key quality
- **Nothing extracted?** Check PDF format and quality
- **Crashes?** Check GPU memory and system resources

---

## Important Notes

⚠️ **This is an AI-assisted tool**
- Not 100% accurate
- Use as guidance with human review
- Always verify important evaluations
- Best for screening and preliminary marking

✅ **Privacy**
- All processing is local
- No data sent to external servers
- PDFs stored only on your machine
- Delete old files manually if needed

🚀 **Performance**
- GPU highly recommended
- First run downloads 6.7GB model
- Subsequent runs are fast
- Cache cleared automatically

---

## Quick Commands

```bash
# Windows
setup.bat          # First-time setup
start.bat          # Start application
python test_setup.py  # Verify installation

# Linux/Mac
./setup.sh         # First-time setup
./start.sh         # Start application
python test_setup.py  # Verify installation
```

---

## What's Next?

1. ✅ Complete installation (setup.bat or setup.sh)
2. ✅ Run test (python test_setup.py)
3. ✅ Start application (start.bat or start.sh)
4. ✅ Prepare your PDFs
5. ✅ Upload and evaluate
6. ✅ Download results

---

**Ready to evaluate? Start the app and open http://localhost:5000**

**Good Luck! 📝✨**
