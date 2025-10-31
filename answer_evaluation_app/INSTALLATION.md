# 🚀 Complete Installation Guide

## System Requirements Check

Before installation, verify your system meets these requirements:

### ✅ Checklist
- [ ] Windows 10/11, Linux, or macOS
- [ ] Python 3.9 or higher
- [ ] NVIDIA GPU with 6GB+ VRAM (for DeepSeek-OCR)
- [ ] CUDA Toolkit 11.8 or 12.1
- [ ] 16GB+ RAM
- [ ] 10GB free disk space

---

## Step-by-Step Installation

### 1️⃣ Install Python

#### Windows:
```bash
# Download Python 3.11 from python.org
# During installation, CHECK "Add Python to PATH"

# Verify installation
python --version
pip --version
```

#### Linux (Ubuntu/Debian):
```bash
sudo apt-get update
sudo apt-get install python3.11 python3-pip python3-venv
```

#### macOS:
```bash
brew install python@3.11
```

---

### 2️⃣ Install CUDA Toolkit (for GPU support)

#### Check GPU Compatibility:
```bash
# Windows
nvidia-smi

# Should show your GPU and CUDA version
```

#### Install CUDA Toolkit:

**Windows:**
1. Download CUDA Toolkit from: https://developer.nvidia.com/cuda-downloads
2. Install CUDA 11.8 or 12.1
3. Restart your computer
4. Verify: `nvcc --version`

**Linux:**
```bash
# Ubuntu/Debian
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-ubuntu2204.pin
sudo mv cuda-ubuntu2204.pin /etc/apt/preferences.d/cuda-repository-pin-600
wget https://developer.download.nvidia.com/compute/cuda/12.1.0/local_installers/cuda-repo-ubuntu2204-12-1-local_12.1.0-530.30.02-1_amd64.deb
sudo dpkg -i cuda-repo-ubuntu2204-12-1-local_12.1.0-530.30.02-1_amd64.deb
sudo cp /var/cuda-repo-ubuntu2204-12-1-local/cuda-*-keyring.gpg /usr/share/keyrings/
sudo apt-get update
sudo apt-get -y install cuda
```

---

### 3️⃣ Install System Dependencies

#### Windows:

**Install Poppler:**
```bash
# Download from: https://github.com/oschwartz10612/poppler-windows/releases/
# Extract to C:\Program Files\poppler
# Add C:\Program Files\poppler\Library\bin to System PATH

# Verify
pdftoppm -v
```

**Install Tesseract OCR (optional):**
```bash
# Download from: https://github.com/UB-Mannheim/tesseract/wiki
# Install to default location
# Add to PATH: C:\Program Files\Tesseract-OCR

# Verify
tesseract --version
```

#### Linux (Ubuntu/Debian):
```bash
sudo apt-get update
sudo apt-get install -y \
    poppler-utils \
    tesseract-ocr \
    tesseract-ocr-eng \
    libgl1-mesa-glx \
    libglib2.0-0
```

#### macOS:
```bash
brew install poppler tesseract
```

---

### 4️⃣ Setup Project

#### Navigate to Project Directory:
```bash
cd C:\Users\nk\paperai\answer_evaluation_app
```

#### Create Virtual Environment:
```bash
# Create venv
python -m venv venv

# Activate on Windows
venv\Scripts\activate

# Activate on Linux/macOS
source venv/bin/activate

# Your prompt should now show (venv)
```

---

### 5️⃣ Install Python Packages

#### Install PyTorch with CUDA Support:

**For CUDA 11.8:**
```bash
pip install torch==2.1.1 torchvision==0.16.1 torchaudio==2.1.1 --index-url https://download.pytorch.org/whl/cu118
```

**For CUDA 12.1:**
```bash
pip install torch==2.1.1 torchvision==0.16.1 torchaudio==2.1.1 --index-url https://download.pytorch.org/whl/cu121
```

**For CPU Only (not recommended):**
```bash
pip install torch==2.1.1 torchvision==0.16.1 torchaudio==2.1.1
```

#### Verify PyTorch Installation:
```bash
python -c "import torch; print('PyTorch Version:', torch.__version__); print('CUDA Available:', torch.cuda.is_available()); print('CUDA Version:', torch.version.cuda if torch.cuda.is_available() else 'N/A')"
```

Expected output:
```
PyTorch Version: 2.1.1+cu118
CUDA Available: True
CUDA Version: 11.8
```

#### Install Other Requirements:
```bash
pip install -r requirements.txt
```

This will install:
- Flask (web framework)
- PyPDF2 (PDF processing)
- Pillow (image processing)
- pytesseract (OCR fallback)
- pdf2image (PDF to image conversion)
- reportlab (PDF report generation)
- chromadb (vector database)
- sentence-transformers (embeddings)
- scikit-learn (similarity algorithms)
- transformers (DeepSeek-OCR)
- accelerate (model loading)

---

### 6️⃣ Verify Installation

#### Test GPU Setup:
```bash
python -c "import torch; print(f'GPU Name: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else \"No GPU\"}')"
```

#### Test Import All Dependencies:
```bash
python -c "
import flask
import PyPDF2
import PIL
import pytesseract
import pdf2image
import reportlab
import chromadb
import sentence_transformers
import sklearn
import torch
import transformers
print('✅ All dependencies imported successfully!')
"
```

---

### 7️⃣ Download DeepSeek-OCR Model (First Run)

The DeepSeek-OCR model (~6.7GB) will be downloaded automatically on first use.

**Pre-download (optional):**
```bash
python
>>> from transformers import AutoTokenizer, AutoModel
>>> tokenizer = AutoTokenizer.from_pretrained("deepseek-ai/DeepSeek-OCR", trust_remote_code=True)
>>> model = AutoModel.from_pretrained("deepseek-ai/DeepSeek-OCR", trust_remote_code=True)
>>> print("Model downloaded successfully!")
>>> exit()
```

This may take 10-20 minutes depending on your internet speed.

---

### 8️⃣ Run the Application

#### Start the Server:
```bash
# Make sure virtual environment is activated (venv)
python app.py
```

Expected output:
```
✅ DeepSeek-OCR initialized for handwritten text extraction
 * Running on http://0.0.0.0:5000
 * Debug mode: on
```

#### Access the Application:
Open your browser and go to:
```
http://localhost:5000
```

---

## 🧪 Testing the Installation

### Test 1: Upload Question Paper
1. Prepare a PDF with questions in format: `Q1. Question? (5 marks)`
2. Upload via web interface
3. Check console for: `✅ Extracted X questions from question paper`

### Test 2: Upload Answer Key
1. Prepare a PDF with answers in format: `Answer 1: Text...`
2. Upload via web interface
3. Check console for: `✅ Extracted X answers from answer key`

### Test 3: Evaluate Student Paper
1. Upload a student answer PDF
2. Watch console for DeepSeek-OCR processing messages
3. Results should appear on the web interface
4. Download the generated PDF report

---

## 🔧 Troubleshooting

### Issue: CUDA Not Available

**Solution:**
```bash
# 1. Check NVIDIA driver
nvidia-smi

# 2. Reinstall PyTorch with correct CUDA version
pip uninstall torch torchvision torchaudio
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# 3. Verify
python -c "import torch; print(torch.cuda.is_available())"
```

### Issue: Poppler Not Found

**Windows:**
```bash
# Add poppler to PATH
# System Properties > Environment Variables > Path
# Add: C:\Program Files\poppler\Library\bin
```

**Linux:**
```bash
sudo apt-get install poppler-utils
```

### Issue: Out of Memory (GPU)

**Solution:**
```python
# Edit deepseek_ocr.py, change:
base_size=640,  # Instead of 1024
image_size=640,
crop_mode=False,  # Disable tiling
```

### Issue: Module Not Found

**Solution:**
```bash
# Ensure virtual environment is activated
# Look for (venv) in prompt

# If not activated:
# Windows: venv\Scripts\activate
# Linux/Mac: source venv/bin/activate

# Reinstall requirements
pip install -r requirements.txt
```

### Issue: Port 5000 Already in Use

**Solution:**
```python
# Edit app.py, change:
app.run(debug=True, host='0.0.0.0', port=5001)  # Use different port
```

### Issue: Slow OCR Processing

**Causes:**
- Running on CPU instead of GPU
- Large PDF files
- High resolution images

**Solutions:**
1. Verify GPU is being used: `torch.cuda.is_available()`
2. Reduce PDF resolution (300 DPI is sufficient)
3. Process fewer pages at once

---

## 📊 Performance Benchmarks

| Component | CPU (16GB RAM) | GPU (8GB VRAM) |
|-----------|----------------|----------------|
| Model Loading | 2-3 minutes | 30-60 seconds |
| 1 Page OCR | 30-60 seconds | 5-10 seconds |
| 5 Page PDF | 3-5 minutes | 30-60 seconds |
| Evaluation | 1-2 seconds | 1-2 seconds |

---

## ✅ Installation Complete!

You're now ready to use the AI-Powered Answer Evaluation System.

### Quick Start Commands:
```bash
# Activate environment
cd C:\Users\nk\paperai\answer_evaluation_app
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Start application
python app.py

# Open browser
# http://localhost:5000
```

### Next Steps:
1. Upload a question paper
2. Upload an answer key
3. Upload student papers for evaluation
4. Download results

For detailed usage instructions, see README.md

---

## 🆘 Need Help?

- **GPU Issues**: Check CUDA installation and PyTorch compatibility
- **OCR Issues**: Verify Poppler and Tesseract installation
- **Python Issues**: Ensure Python 3.9+ and virtual environment
- **Port Issues**: Change port in app.py if 5000 is taken
- **Memory Issues**: Reduce batch size or use CPU (slower)

---

**Happy Evaluating! 📝✨**
