# Quick Fix for "addict" Module Error

## The Problem
The DeepSeek-OCR model requires the `addict` package which is not installed in your environment. This is causing the OCR extraction to fail with 0 questions and 0 answers.

## Quick Solution (Choose One)

### Option 1: Use the Batch File (Easiest)
Just double-click this file:
```
install_missing_deps.bat
```

It will automatically install all missing packages:
- addict (required for DeepSeek-OCR configuration)
- timm (required for vision models)
- einops (required for tensor operations)

### Option 2: Manual Installation
Open Command Prompt and run:
```bash
cd C:\Users\nk\paperai\answer_evaluation_app
pip install addict timm einops
```

Or install all dependencies at once:
```bash
pip install -r requirements.txt
```

## After Installing

1. **Restart the Flask app:**
   ```bash
   python app.py
   ```
   
   Or use the start script:
   ```bash
   start.bat
   ```

2. **Re-upload your PDFs** through the web interface

3. **Check the console** for success messages:
   ```
   ✅ Extracted N questions from question paper
   ✅ Extracted N answers from answer key
   ```

## What Was Fixed

I've updated your `requirements.txt` file to include:
- `addict==2.4.0` - Configuration management for DeepSeek-OCR
- `timm==0.9.12` - Vision model library
- `einops==0.7.0` - Tensor operations library

These are essential dependencies for the DeepSeek-OCR model to work properly with handwritten/scanned documents.

## Verification

After installation, you should see in the console:
```
✅ DeepSeek-OCR initialized for handwritten text extraction
📄 Question paper appears to be scanned/handwritten, using OCR...
🧠 Using DeepSeek-OCR for text extraction: question_paper_question.pdf
✅ Extracted N questions from question paper
```

Instead of the previous error:
```
❌ Error initializing DeepSeek-OCR: This modeling file requires the following packages...
```

## Still Having Issues?

If you still see errors after installation, try:

1. **Check if packages are installed:**
   ```bash
   pip list | findstr addict
   pip list | findstr timm
   pip list | findstr einops
   ```

2. **Reinstall dependencies:**
   ```bash
   pip install --upgrade --force-reinstall addict timm einops
   ```

3. **Check Python environment:**
   ```bash
   python --version
   pip --version
   ```

4. **Run diagnostics:**
   ```bash
   python auto_diagnose.py
   ```

## Technical Details

The error occurred because:
1. DeepSeek-OCR uses dynamic module loading from Hugging Face
2. The model's configuration files import `addict` for config management
3. When `transformers` tries to load the model, it checks for required packages
4. Missing packages cause an ImportError before the model can initialize

The `addict` package provides dictionary-like configuration objects that DeepSeek-OCR uses internally for managing model parameters.

## Next Steps After Fix

Once the packages are installed:
1. Your OCR extraction will work properly
2. Handwritten/scanned PDFs will be processed using DeepSeek-OCR
3. Questions and answers will be extracted correctly
4. You can proceed to evaluate student papers

Note: DeepSeek-OCR works best with a CUDA-enabled GPU. If you don't have a GPU, it will fall back to CPU (slower but still functional).
