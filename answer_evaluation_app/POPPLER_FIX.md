# Poppler Installation Guide

## Problem
Your application needs Poppler to convert PDF files to images. The error message is:
```
PDFInfoNotInstalledError: Unable to get page count. Is poppler installed and in PATH?
```

## Quick Solution

### Method 1: Automated Installation (RECOMMENDED)
1. Close your Flask app (Ctrl+C)
2. Run: `install_poppler_auto.bat`
3. Wait for download and installation to complete
4. **CLOSE your current terminal window completely**
5. Open a **NEW** command prompt
6. Navigate back: `cd C:\Users\nk\paperai\answer_evaluation_app`
7. Activate environment: `conda activate torch_gpu`
8. Run app: `python app.py`

### Method 2: Using Winget (Windows 11/Updated Windows 10)
1. Run: `install_poppler_winget.bat`
2. Restart your terminal
3. Verify: `pdfinfo -v`

### Method 3: Using Chocolatey (if you have it)
1. Run: `install_poppler_choco.bat`
2. Restart your terminal
3. Verify: `pdfinfo -v`

### Method 4: Manual Installation
1. Download from: https://github.com/oschwartz10612/poppler-windows/releases/
2. Download the latest `Release-XX.XX.X-X.zip`
3. Extract to `C:\poppler`
4. Add to PATH:
   - Open System Properties → Environment Variables
   - Edit User PATH variable
   - Add: `C:\poppler\Library\bin` (adjust path based on extracted folder structure)
5. Restart terminal

## Verification
After installation and terminal restart, verify with:
```bash
pdfinfo -v
```

You should see Poppler version information.

## Troubleshooting

### "Command not found" after installation
- Make sure you **completely closed and reopened** your terminal
- Verify the bin path was added to PATH correctly
- Try logging out and back in to Windows

### Still not working?
1. Check where Poppler was installed:
   ```bash
   dir C:\poppler /s /b | findstr bin
   ```
2. Manually verify the path exists
3. Add the correct bin path to your system PATH

### Alternative: Use conda
```bash
conda install -c conda-forge poppler
```

## Why This Happens
The `pdf2image` library requires Poppler utilities (like `pdfinfo`, `pdftoppm`) to convert PDFs to images. Your DeepSeek-OCR model needs to process PDFs as images, so Poppler is essential.

## Next Steps
Once Poppler is installed and working:
1. Your app should successfully extract text from PDFs
2. The OCR process will work for handwritten/scanned documents
3. Questions will be properly extracted and stored
