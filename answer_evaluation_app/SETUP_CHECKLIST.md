# ✅ Setup & Deployment Checklist

## Pre-Installation Checklist

### System Requirements
- [ ] **Operating System**: Windows 10/11, Ubuntu 20.04+, or macOS 11+
- [ ] **Python**: Version 3.9 or higher installed
  - Check: `python --version`
- [ ] **RAM**: Minimum 16GB (recommended: 32GB)
- [ ] **Storage**: At least 15GB free space (for models)
- [ ] **GPU** (Optional but recommended): NVIDIA GPU with 6GB+ VRAM
  - Check: `nvidia-smi` (Windows/Linux)

---

## Installation Checklist

### 1. Install Ollama
- [ ] Visit https://ollama.ai
- [ ] Download installer for your OS
- [ ] Run installer
- [ ] Verify installation: `ollama --version`
- [ ] Pull model: `ollama pull llama3.1:latest`
- [ ] Verify model: `ollama list` (should show llama3.1)

**Time estimate: 10-15 minutes (depending on internet speed)**

---

### 2. Install Poppler

#### Windows:
- [ ] Download from: https://github.com/oschwartz10612/poppler-windows/releases/
- [ ] Extract to `C:\poppler`
- [ ] Add `C:\poppler\Library\bin` to PATH
- [ ] **Restart terminal/PowerShell**
- [ ] Verify: `pdfinfo -v`

**OR use automated script:**
- [ ] Run: `fix_poppler.bat`
- [ ] Follow prompts
- [ ] Restart terminal
- [ ] Verify: `pdfinfo -v`

#### Linux (Ubuntu/Debian):
- [ ] Run: `sudo apt-get update`
- [ ] Run: `sudo apt-get install poppler-utils`
- [ ] Verify: `pdfinfo -v`

#### macOS:
- [ ] Install Homebrew (if not installed): https://brew.sh
- [ ] Run: `brew install poppler`
- [ ] Verify: `pdfinfo -v`

**Time estimate: 5-10 minutes**

---

### 3. Setup Python Environment

#### Create Virtual Environment (Recommended):
- [ ] Navigate to project: `cd C:\Users\nk\paperai\answer_evaluation_app`
- [ ] Create venv: `python -m venv venv`
- [ ] Activate venv:
  - Windows: `venv\Scripts\activate`
  - Linux/Mac: `source venv/bin/activate`
- [ ] Verify: Command prompt should show `(venv)`

---

### 4. Install PyTorch with CUDA

**For NVIDIA GPU (CUDA 11.8):**
- [ ] Run: 
  ```bash
  pip install torch==2.1.1 torchvision==0.16.1 --index-url https://download.pytorch.org/whl/cu118
  ```
- [ ] Verify CUDA: 
  ```python
  python -c "import torch; print(f'CUDA: {torch.cuda.is_available()}')"
  ```
  Should print: `CUDA: True`

**For CPU only (no GPU):**
- [ ] Run:
  ```bash
  pip install torch==2.1.1 torchvision==0.16.1 --index-url https://download.pytorch.org/whl/cpu
  ```

**Time estimate: 5-10 minutes**

---

### 5. Install Python Dependencies
- [ ] Run: `pip install -r requirements_ollama_full.txt`
- [ ] Wait for installation (this may take 10-15 minutes)
- [ ] Verify: `pip list` (should show all packages)

**Time estimate: 10-15 minutes**

---

## Post-Installation Verification

### Run System Test
- [ ] Run: `python test_complete_system.py`
- [ ] Check results:
  - [ ] ✅ Python Packages - Should be OK
  - [ ] ✅ CUDA/GPU - Should be OK (or warning if CPU only)
  - [ ] ✅ Ollama - Should be OK
  - [ ] ✅ Poppler - Should be OK
  - [ ] ✅ DeepSeek-OCR - Should be OK (first run downloads model)
  - [ ] ✅ Vector Database - Should be OK
  - [ ] ✅ Ollama Evaluator - Should be OK
  - [ ] ✅ PDF Generation - Should be OK

**Expected: 8/8 tests passed** (7/8 is OK if GPU test shows warning but system works)

**Time estimate: 5-10 minutes (first run may take longer due to model download)**

---

## First Run Checklist

### Start the Application
- [ ] Ensure virtual environment is activated
- [ ] Run: `start_ollama_integrated.bat` (Windows) or `python app_ollama_integrated.py` (any OS)
- [ ] Wait for server to start
- [ ] Look for message: "Running on http://127.0.0.1:5000"

**Time estimate: 30 seconds**

---

### Access Web Interface
- [ ] Open browser
- [ ] Navigate to: `http://localhost:5000`
- [ ] Page should load successfully
- [ ] Check status indicators at top (should show "System Ready")

---

## Functional Testing Checklist

### Test 1: Upload Question Paper
- [ ] Click "Upload Question Paper"
- [ ] Select a test PDF with questions
  - Format: "Q1. Question text? (5 marks)"
- [ ] Click Upload
- [ ] Wait for processing
- [ ] Verify: Success message shows extracted questions
- [ ] Check: Number of questions detected
- [ ] Check: Total marks calculated

**Expected: Questions extracted and stored**

---

### Test 2: Upload Answer Key
- [ ] Click "Upload Answer Key"
- [ ] Select a test PDF with answers
  - Format: "Answer 1: Correct answer text..."
- [ ] Click Upload
- [ ] Wait for processing
- [ ] Verify: Success message shows extracted answers
- [ ] Check: Number of answers detected

**Expected: Answers extracted and stored**

---

### Test 3: Evaluate Student Paper
- [ ] Click "Evaluate Student Paper"
- [ ] Enter student name (optional)
- [ ] Select a handwritten answer PDF (can be from phone)
- [ ] Click "Evaluate"
- [ ] Wait for processing (may take 2-5 minutes depending on length)
- [ ] Watch progress messages in UI
- [ ] Verify: Results displayed on screen
- [ ] Check: Marks, percentage, and grade shown
- [ ] Check: Question-wise breakdown available

**Expected: Evaluation completes successfully**

---

### Test 4: Download Result PDF
- [ ] Click "Download Result PDF"
- [ ] Verify: PDF downloads successfully
- [ ] Open PDF
- [ ] Check: Contains all sections:
  - [ ] Header with student name and date
  - [ ] Summary (marks, percentage, grade)
  - [ ] Question-wise breakdown
  - [ ] Individual feedback for each question
  - [ ] Remarks and notes

**Expected: Professional PDF report generated**

---

## Performance Optimization Checklist

### If Evaluation is Slow:
- [ ] Check if GPU is being used:
  ```python
  python -c "import torch; print(torch.cuda.is_available())"
  ```
- [ ] If GPU not detected:
  - [ ] Reinstall CUDA toolkit
  - [ ] Reinstall PyTorch with CUDA
  - [ ] Restart computer
- [ ] Consider using smaller Ollama model:
  - [ ] Change in `app_ollama_integrated.py`: `model_name="phi"`
  - [ ] Pull model: `ollama pull phi`

### If OCR Quality is Poor:
- [ ] Check input PDF quality (should be 300+ DPI)
- [ ] Ensure good lighting in source images
- [ ] Try increasing OCR settings in `deepseek_ocr.py`:
  ```python
  base_size=1536,  # Higher = better quality
  crop_mode=True   # Enable tiling
  ```

### If Out of Memory:
- [ ] Close other GPU applications
- [ ] Reduce batch sizes
- [ ] Use smaller Ollama model
- [ ] Consider CPU-only mode

---

## Troubleshooting Checklist

### Problem: Ollama not found
- [ ] Verify Ollama installed: `ollama --version`
- [ ] If not: Install from https://ollama.ai
- [ ] Restart terminal after installation
- [ ] Verify model: `ollama list`

---

### Problem: Poppler not found
- [ ] Windows: Check PATH includes `C:\poppler\Library\bin`
- [ ] Restart terminal/PowerShell
- [ ] Verify: `pdfinfo -v`
- [ ] If fails: Run `fix_poppler.bat`

---

### Problem: DeepSeek-OCR fails to initialize
- [ ] Check CUDA availability: 
  ```python
  python -c "import torch; print(torch.cuda.is_available())"
  ```
- [ ] Check internet connection (for model download)
- [ ] Check free disk space (need ~7GB)
- [ ] Try clearing cache: Delete `~/.cache/huggingface`

---

### Problem: No questions detected
- [ ] Check PDF format
- [ ] Ensure questions have numbers: "Q1.", "Question 1:", "(i)"
- [ ] Ensure marks specified: "(5 marks)", "[10]", "5M"
- [ ] Try with sample PDF first
- [ ] Check console logs for extraction errors

---

### Problem: Web interface not loading
- [ ] Check if port 5000 is free: `netstat -an | findstr 5000`
- [ ] Try different port:
  ```python
  app.run(debug=True, host='0.0.0.0', port=5001)
  ```
- [ ] Check firewall settings
- [ ] Try: `http://127.0.0.1:5000` instead of `localhost`

---

## Security Checklist

- [ ] All data processing is local ✅
- [ ] No external API calls during evaluation ✅
- [ ] Student data not sent to cloud ✅
- [ ] Results stored locally only ✅
- [ ] Firewall allows localhost:5000 (optional)

---

## Backup & Maintenance Checklist

### Regular Maintenance:
- [ ] Clear old uploads periodically: Delete files in `uploads/`
- [ ] Clear old results: Delete files in `results/`
- [ ] Backup vector database: Copy `vector_db/` folder
- [ ] Update Ollama models: `ollama pull llama3.1:latest`
- [ ] Update Python packages: `pip install --upgrade -r requirements_ollama_full.txt`

### Before Major Updates:
- [ ] Backup current working version
- [ ] Test on sample data first
- [ ] Keep old version until new is verified

---

## Documentation Checklist

Have you read:
- [ ] `QUICKSTART_OLLAMA.md` - Quick start guide
- [ ] `COMPLETE_GUIDE_OLLAMA.md` - Comprehensive documentation
- [ ] `PROJECT_SUMMARY_COMPLETE.md` - Project overview
- [ ] `VISUAL_ARCHITECTURE.md` - System architecture
- [ ] This checklist - Setup steps

---

## Production Deployment Checklist

### Before Going Live:
- [ ] Test with sample data extensively
- [ ] Verify all question formats work
- [ ] Test with various handwriting styles
- [ ] Benchmark evaluation time
- [ ] Set up backup process
- [ ] Document any customizations made
- [ ] Train users on the system
- [ ] Create user manual if needed

### Security for Production:
- [ ] Change default ports if needed
- [ ] Add authentication if exposing to network
- [ ] Set up HTTPS if needed
- [ ] Configure proper file upload limits
- [ ] Set up logging and monitoring
- [ ] Plan for data retention/deletion

---

## Success Metrics

Your system is ready for use when:
- [ ] All tests in `test_complete_system.py` pass
- [ ] Web interface loads successfully
- [ ] Question paper upload works consistently
- [ ] Answer key upload works consistently
- [ ] Student paper evaluation completes successfully
- [ ] Result PDFs are generated correctly
- [ ] Evaluation time is acceptable (< 5 min per paper)
- [ ] Marks and feedback are reasonable
- [ ] Users can access and use the system

---

## Next Steps

After completing this checklist:
1. [ ] Test with real question papers
2. [ ] Test with real answer keys
3. [ ] Test with real student papers
4. [ ] Review AI-generated marks and feedback
5. [ ] Make any necessary adjustments to grading scale
6. [ ] Document any issues or improvements needed
7. [ ] Train users on the system
8. [ ] Deploy for regular use

---

## Quick Reference Commands

```bash
# Start system
start_ollama_integrated.bat

# Test system
python test_complete_system.py

# Check Ollama
ollama list

# Check Poppler
pdfinfo -v

# Check CUDA
python -c "import torch; print(torch.cuda.is_available())"

# Activate venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Update packages
pip install --upgrade -r requirements_ollama_full.txt

# Clear database
python -c "from vector_db_manager import VectorDBManager; VectorDBManager().clear_all_data()"
```

---

## Estimated Total Setup Time

- **Ollama Installation**: 10-15 minutes
- **Poppler Installation**: 5-10 minutes
- **Python Environment**: 5 minutes
- **PyTorch Installation**: 5-10 minutes
- **Dependencies Installation**: 10-15 minutes
- **System Testing**: 5-10 minutes (+ model download time)
- **First Functional Test**: 10-15 minutes

**Total: 50-80 minutes for complete setup**  
*(Not including DeepSeek-OCR model download: ~6.7GB, time depends on internet speed)*

---

## You're Ready! 🎉

Once all checkboxes are ticked, your system is fully functional and ready to evaluate answer papers!

**Start with:** `start_ollama_integrated.bat`

**Access at:** `http://localhost:5000`

**Good luck! 🚀**
