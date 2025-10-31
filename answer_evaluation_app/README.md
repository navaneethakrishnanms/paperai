# 📝 AI-Powered Answer Paper Evaluation System

An intelligent automated system for evaluating handwritten answer scripts using **DeepSeek-OCR** and AI-based similarity matching.

## 🌟 Features

- ✅ **Handwritten Text Extraction**: Uses DeepSeek-OCR for accurate handwritten text recognition
- ✅ **Question Paper Processing**: Automatically extracts questions with marks from PDFs
- ✅ **Answer Key Management**: Stores correct answers in vector database
- ✅ **Student Answer Evaluation**: Compares student answers with answer key using AI
- ✅ **Intelligent Scoring**: Uses multiple similarity algorithms for fair marking
- ✅ **Detailed Reports**: Generates comprehensive PDF reports with question-wise breakdown
- ✅ **Web Interface**: Easy-to-use web application for upload and evaluation
- ✅ **Vector Database**: ChromaDB for efficient answer storage and retrieval

## 🔧 System Requirements

### Hardware Requirements
- **GPU**: NVIDIA GPU with CUDA support (required for DeepSeek-OCR)
  - Minimum 6GB VRAM
  - Recommended: 8GB+ VRAM
- **RAM**: Minimum 16GB
- **Storage**: 10GB free space (for model downloads)

### Software Requirements
- Python 3.9 or higher
- CUDA Toolkit 11.8+ (for GPU support)
- Poppler (for PDF to image conversion)
- Tesseract OCR (optional fallback)

## 📦 Installation

### Step 1: Clone or Navigate to Directory
```bash
cd C:\Users\nk\paperai\answer_evaluation_app
```

### Step 2: Create Virtual Environment (Recommended)
```bash
python -m venv venv

# Activate on Windows
venv\Scripts\activate

# Activate on Linux/Mac
source venv/bin/activate
```

### Step 3: Install Dependencies

#### Install PyTorch with CUDA Support First:
```bash
# For CUDA 11.8
pip install torch==2.1.1 torchvision==0.16.1 torchaudio==2.1.1 --index-url https://download.pytorch.org/whl/cu118

# For CUDA 12.1
pip install torch==2.1.1 torchvision==0.16.1 torchaudio==2.1.1 --index-url https://download.pytorch.org/whl/cu121
```

#### Install Other Requirements:
```bash
pip install -r requirements.txt
```

### Step 4: Install System Dependencies

#### Windows:
1. **Install Poppler**:
   - Download from: https://github.com/oschwartz10612/poppler-windows/releases/
   - Extract and add `bin` folder to PATH
   
2. **Install Tesseract OCR** (optional):
   - Download from: https://github.com/UB-Mannheim/tesseract/wiki
   - Install and add to PATH

#### Linux (Ubuntu/Debian):
```bash
sudo apt-get update
sudo apt-get install poppler-utils tesseract-ocr
```

#### macOS:
```bash
brew install poppler tesseract
```

### Step 5: Verify GPU Setup
```bash
python -c "import torch; print(f'CUDA Available: {torch.cuda.is_available()}')"
```

## 🚀 Usage

### Starting the Application

#### Method 1: Using Python
```bash
python app.py
```

#### Method 2: Using Batch File (Windows)
```bash
start.bat
```

#### Method 3: Using Shell Script (Linux/Mac)
```bash
chmod +x start.sh
./start.sh
```

The application will start on: **http://localhost:5000**

### Workflow

1. **Upload Question Paper** 📋
   - Upload PDF containing questions with marks
   - Format: `Q1. Question text? (5 marks)`
   - System extracts questions and stores them

2. **Upload Answer Key** ✅
   - Upload PDF containing correct answers
   - Format: `Answer 1: Correct answer text...`
   - System stores answers in vector database

3. **Evaluate Student Paper** ✍️
   - Upload student's handwritten answer script (PDF)
   - System uses DeepSeek-OCR to extract handwritten text
   - Compares with answer key using AI algorithms
   - Generates marks and detailed report

4. **Download Results** 📊
   - View results on web interface
   - Download detailed PDF report
   - Results saved in `results/` folder

## 📁 Project Structure

```
answer_evaluation_app/
├── app.py                      # Flask web application
├── pdf_processor.py            # PDF processing and DeepSeek-OCR integration
├── deepseek_ocr.py            # DeepSeek-OCR wrapper
├── vector_db_manager.py       # ChromaDB vector database manager
├── answer_evaluator.py        # Answer comparison and scoring logic
├── config.py                  # Configuration settings
├── requirements.txt           # Python dependencies
├── templates/
│   └── index.html            # Web interface
├── static/
│   ├── style.css             # Styling
│   └── script.js             # Frontend JavaScript
├── uploads/                  # Uploaded PDFs
├── results/                  # Generated result PDFs
└── vector_db/               # ChromaDB vector storage
```

## ⚙️ Configuration

Edit `config.py` to customize:

- **Grading Scale**: Adjust similarity thresholds and marks percentages
- **OCR Settings**: DPI, language, and other OCR parameters
- **Evaluation Weights**: Modify similarity algorithm weights
- **Grade Thresholds**: Customize grade boundaries
- **Feedback Messages**: Edit feedback based on performance

## 🧠 How It Works

### 1. Text Extraction (DeepSeek-OCR)
- Converts PDF pages to images
- Uses DeepSeek-OCR model for handwritten text recognition
- Processes each page with tiling for better accuracy
- Combines extracted text from all pages

### 2. Answer Comparison
- **TF-IDF + Cosine Similarity** (35% weight)
- **Sequence Matching** (25% weight)
- **Word Overlap** (25% weight)
- **Keyword Matching** (15% weight)

### 3. Marking System
- Similarity scores mapped to marks using grading curve
- 90%+ similarity → Full marks
- 80-90% similarity → 95% marks
- Graduated marking down to 10% for attempts

### 4. Report Generation
- Comprehensive PDF with question-wise breakdown
- Summary statistics and grade
- Color-coded performance indicators

## 🛠️ Troubleshooting

### ⚠️ POPPLER NOT INSTALLED ERROR (MOST COMMON)

If you see this error:
```
PDFInfoNotInstalledError: Unable to get page count. Is poppler installed and in PATH?
```

**Quick Fix:**
```bash
# Run the automated installer
fix_poppler.bat

# Or check installation status
check_poppler.bat
```

**Manual Fix:**
1. Download Poppler: https://github.com/oschwartz10612/poppler-windows/releases/
2. Extract to `C:\poppler`
3. Add `C:\poppler\Library\bin` to PATH
4. **Restart your terminal**
5. Verify: `pdfinfo -v`

**See detailed guide:** `POPPLER_FIX.md`

### DeepSeek-OCR Model Download
On first run, the system will download the DeepSeek-OCR model (~6.7GB):
```
🔄 Loading DeepSeek-OCR model...
Downloading model files... (this may take a few minutes)
✅ DeepSeek-OCR initialized successfully!
```

### GPU Not Detected
If CUDA is not available:
- Install NVIDIA drivers
- Install CUDA Toolkit
- Reinstall PyTorch with CUDA support
- The system will fall back to CPU (slower)

### Poor OCR Results
- Ensure PDF images are high quality (300+ DPI)
- Check that handwriting is reasonably clear
- Try adjusting `base_size` and `image_size` in `deepseek_ocr.py`

### Poppler Not Found Error
```bash
# Windows: Add poppler bin folder to PATH
# Linux: sudo apt-get install poppler-utils
# macOS: brew install poppler
```

### Memory Issues
- Reduce batch size in config
- Process fewer pages at once
- Close other GPU-intensive applications
- Consider using a machine with more VRAM

## 📊 Example Question Paper Format

```
Q1. What is photosynthesis? Explain the process. (5 marks)

Q2. Describe the water cycle with a diagram. (10 marks)

Q3. List five types of renewable energy sources. (5 marks)
```

## 📝 Example Answer Key Format

```
Answer 1: Photosynthesis is the process by which green plants convert light energy into chemical energy. It occurs in chloroplasts using chlorophyll...

Answer 2: The water cycle is the continuous movement of water on, above, and below the Earth's surface. It includes evaporation, condensation, precipitation...

Answer 3: Five types of renewable energy sources are: 1) Solar energy, 2) Wind energy, 3) Hydroelectric power, 4) Geothermal energy, 5) Biomass energy.
```

## 🔒 Privacy & Security

- All processing happens locally on your machine
- No data is sent to external servers (except model downloads)
- PDFs and results are stored locally only
- Vector database is stored locally

## 🤝 Contributing

Contributions are welcome! To contribute:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is for educational and evaluation purposes.

## 🙏 Acknowledgments

- **DeepSeek-OCR**: Advanced OCR model for handwritten text
- **ChromaDB**: Vector database for semantic search
- **Sentence Transformers**: Embedding models for text similarity
- **Flask**: Web framework

## 📞 Support

For issues or questions:
- Check the troubleshooting section
- Review configuration settings
- Ensure all dependencies are installed
- Verify GPU/CUDA setup

## 🎯 Future Enhancements

- [ ] Multi-language support
- [ ] Batch processing of multiple papers
- [ ] Custom scoring rubrics
- [ ] Database persistence for historical data
- [ ] REST API for integration
- [ ] Mobile app support
- [ ] Real-time progress tracking
- [ ] Answer quality analysis

## 📈 Performance Tips

1. **GPU Utilization**: Ensure GPU is being used for optimal speed
2. **PDF Quality**: Higher DPI = better OCR results
3. **Clear Handwriting**: More legible writing = better extraction
4. **Batch Processing**: Process multiple papers in sequence
5. **Regular Cleanup**: Clear old uploads and results periodically

---

**Note**: This system uses AI and may not be 100% accurate. Always review results before final grading.
