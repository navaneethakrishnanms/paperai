# GPU-Optimized Requirements Installation Guide

## 🎮 Your System: CUDA 12.1 GPU

This requirements.txt is optimized for your NVIDIA GPU with CUDA 12.1 support.

---

## 📦 Updated requirements.txt

```txt
Flask==3.0.0
PyPDF2==3.0.1
Pillow==10.1.0
pytesseract==0.3.10
pdf2image==1.16.3
reportlab==4.0.7
chromadb==0.4.18
sentence-transformers==2.7.0
huggingface-hub==0.24.0
scikit-learn==1.3.2
numpy==1.26.2
werkzeug==3.0.1

# DeepSeek-OCR dependencies (GPU CUDA 12.1 version)
--extra-index-url https://download.pytorch.org/whl/cu121
torch==2.5.1+cu121
torchvision==0.20.1+cu121
torchaudio==2.5.1+cu121
transformers==4.45.0
accelerate==0.34.0
addict==2.4.0
timm==0.9.12
einops==0.7.0
```

---

## 🚀 Installation Methods

### **Method 1: Use the GPU Install Script** (Recommended) ⭐
```bash
# Just double-click this file:
install_gpu_version.bat
```

This will:
- Install all packages in the correct order
- Use CUDA 12.1 optimized PyTorch
- Test your GPU after installation
- Show your GPU information

### **Method 2: Install from requirements.txt**
```bash
cd C:\Users\nk\paperai\answer_evaluation_app
pip install -r requirements.txt
```

### **Method 3: Manual Installation (Step by Step)**
```bash
# Step 1: Install basic packages
pip install Flask==3.0.0 PyPDF2==3.0.1 Pillow==10.1.0 pytesseract==0.3.10 pdf2image==1.16.3 reportlab==4.0.7 werkzeug==3.0.1

# Step 2: Install ML packages
pip install chromadb==0.4.18 scikit-learn==1.3.2 numpy==1.26.2 sentence-transformers==2.7.0 huggingface-hub==0.24.0

# Step 3: Install PyTorch with CUDA 12.1
pip install torch==2.5.1+cu121 torchvision==0.20.1+cu121 torchaudio==2.5.1+cu121 --extra-index-url https://download.pytorch.org/whl/cu121

# Step 4: Install transformers and dependencies
pip install transformers==4.45.0 accelerate==0.34.0 addict==2.4.0 timm==0.9.12 einops==0.7.0
```

---

## 🔍 Verify GPU Installation

After installation, verify your GPU is recognized:

```bash
python -c "import torch; print('CUDA Available:', torch.cuda.is_available()); print('CUDA Version:', torch.version.cuda); print('GPU:', torch.cuda.get_device_name(0))"
```

Expected output:
```
CUDA Available: True
CUDA Version: 12.1
GPU: NVIDIA GeForce RTX XXXX (or your GPU model)
```

---

## 📊 What Changed from Previous Version

| Package | Old Version | New GPU Version | Reason |
|---------|-------------|-----------------|--------|
| torch | 2.1.1 | 2.5.1+cu121 | Latest with CUDA 12.1 |
| torchvision | Not included | 0.20.1+cu121 | Vision support |
| torchaudio | Not included | 2.5.1+cu121 | Audio support |
| transformers | 4.36.0 | 4.45.0 | Compatible with torch 2.5 |
| accelerate | 0.25.0 | 0.34.0 | Better GPU optimization |
| sentence-transformers | 2.2.2 | 2.7.0 | Fixed huggingface_hub issue |
| huggingface-hub | Not specified | 0.24.0 | Compatible version |

---

## ⚡ Performance Benefits

With GPU optimization, you'll get:

### **DeepSeek-OCR Processing:**
- **CPU**: ~30-60 seconds per page
- **GPU (CUDA 12.1)**: ~5-10 seconds per page
- **Speed improvement**: 3-6x faster

### **Memory Usage:**
- More efficient VRAM utilization
- Better batch processing
- Faster model loading with `accelerate`

---

## 🎯 After Installation

1. **Start your app:**
   ```bash
   python app.py
   ```

2. **Check console for GPU confirmation:**
   ```
   ✅ DeepSeek-OCR initialized for handwritten text extraction
   🎮 Using GPU: NVIDIA GeForce RTX XXXX
   📦 Loading DeepSeek-OCR model...
   ✅ Model loaded on CUDA device
   ```

3. **Upload your PDFs** - they should process much faster now!

---

## ⚠️ Important Notes

### **CUDA Version Check:**
Make sure you have CUDA 12.1 installed on your system:
```bash
nvcc --version
```

If you have a different CUDA version:
- **CUDA 11.8**: Use `torch==2.5.1+cu118`
- **CUDA 12.4**: Use `torch==2.5.1+cu124`
- **No CUDA**: Use `torch==2.5.1` (CPU only)

### **VRAM Requirements:**
- **Minimum**: 6GB VRAM
- **Recommended**: 8GB+ VRAM
- **Optimal**: 12GB+ VRAM

If you run out of VRAM, the model will automatically fall back to CPU.

---

## 🔧 Troubleshooting

### **Issue: "CUDA out of memory"**
```bash
# Reduce batch size or image resolution in deepseek_ocr.py
# Line ~85: Change base_size=1024 to base_size=640
```

### **Issue: "CUDA not available"**
```bash
# Check CUDA installation
nvidia-smi

# Reinstall PyTorch with correct CUDA version
pip uninstall torch torchvision torchaudio
pip install torch==2.5.1+cu121 torchvision==0.20.1+cu121 torchaudio==2.5.1+cu121 --extra-index-url https://download.pytorch.org/whl/cu121
```

### **Issue: Still getting huggingface_hub errors**
```bash
# Force reinstall
pip install --force-reinstall huggingface-hub==0.24.0 sentence-transformers==2.7.0
```

---

## 📈 Expected Results

After GPU installation, you should see:

```
✅ DeepSeek-OCR initialized for handwritten text extraction
🎮 GPU: NVIDIA GeForce RTX 3060 (12GB VRAM)
📄 Question paper appears to be scanned/handwritten, using OCR...
🧠 Using DeepSeek-OCR for text extraction: question_paper_question.pdf
🚀 Running OCR on image: page_1.jpg (GPU accelerated)
📄 Processing page 1/3... (2.3s)
📄 Processing page 2/3... (2.1s)
📄 Processing page 3/3... (2.2s)
✅ Extracted 5 questions from question paper (Total: 6.6s)
```

---

## 🎉 Ready to Use!

Your GPU-optimized setup is complete. Enjoy much faster OCR processing! 🚀

**Files Created:**
- ✅ `requirements.txt` - GPU-optimized dependencies
- ✅ `install_gpu_version.bat` - One-click GPU installer
- ✅ `GPU_INSTALL_GUIDE.md` - This comprehensive guide
