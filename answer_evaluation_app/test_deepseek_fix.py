"""
Test script to verify DeepSeek-OCR fix
Run this to test if the OCR is working correctly
"""

import os
import sys
from pathlib import Path

# Add the current directory to path
sys.path.insert(0, str(Path(__file__).parent))

def test_deepseek_ocr():
    """Test DeepSeek-OCR initialization and basic functionality"""
    print("="*60)
    print("Testing DeepSeek-OCR Fix")
    print("="*60)
    
    try:
        # Import the module
        print("\n1️⃣ Importing deepseek_ocr module...")
        from deepseek_ocr import DeepSeekOCR, get_deepseek_ocr
        print("   ✅ Import successful")
        
        # Initialize OCR
        print("\n2️⃣ Initializing DeepSeek-OCR...")
        ocr = get_deepseek_ocr()
        success = ocr.initialize()
        
        if success:
            print("   ✅ DeepSeek-OCR initialized successfully")
        else:
            print("   ❌ Failed to initialize DeepSeek-OCR")
            return False
        
        # Check if uploads directory exists with PDFs
        print("\n3️⃣ Checking for test PDFs in uploads directory...")
        uploads_dir = Path("uploads")
        
        if not uploads_dir.exists():
            print("   ⚠️ Uploads directory doesn't exist")
            print("   Creating uploads directory...")
            uploads_dir.mkdir(exist_ok=True)
            print("   ℹ️ Please upload PDF files to test OCR")
            return True
        
        # Look for PDF files
        pdf_files = list(uploads_dir.glob("*.pdf"))
        
        if not pdf_files:
            print("   ⚠️ No PDF files found in uploads directory")
            print("   ℹ️ Please upload PDF files to test OCR")
            return True
        
        print(f"   ✅ Found {len(pdf_files)} PDF file(s)")
        
        # Test with the first PDF
        test_pdf = pdf_files[0]
        print(f"\n4️⃣ Testing OCR with: {test_pdf.name}")
        print("   This may take a few minutes...")
        
        try:
            text = ocr.extract_text_from_pdf(str(test_pdf))
            
            if text:
                print(f"   ✅ Successfully extracted {len(text)} characters")
                print(f"\n   Preview (first 200 chars):")
                print(f"   {'-'*50}")
                print(f"   {text[:200]}...")
                print(f"   {'-'*50}")
            else:
                print("   ⚠️ No text extracted (might be empty or image-only PDF)")
            
            return True
            
        except Exception as e:
            print(f"   ❌ Error during OCR: {e}")
            import traceback
            traceback.print_exc()
            return False
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("\nMake sure all dependencies are installed:")
        print("  pip install torch transformers pdf2image pillow")
        return False
    
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_pdf_processor():
    """Test PDF processor with question extraction"""
    print("\n" + "="*60)
    print("Testing PDF Processor")
    print("="*60)
    
    try:
        from pdf_processor import PDFProcessor
        
        print("\n1️⃣ Initializing PDF Processor...")
        processor = PDFProcessor(use_deepseek=True)
        print("   ✅ PDF Processor initialized")
        
        # Check for question paper
        uploads_dir = Path("uploads")
        question_papers = list(uploads_dir.glob("question_paper_*.pdf"))
        
        if not question_papers:
            print("\n   ⚠️ No question paper found (files starting with 'question_paper_')")
            print("   ℹ️ Upload a question paper to test extraction")
            return True
        
        test_file = question_papers[0]
        print(f"\n2️⃣ Testing question extraction with: {test_file.name}")
        
        questions = processor.extract_questions_with_marks(str(test_file))
        
        print(f"\n   ✅ Extracted {len(questions)} questions")
        
        if questions:
            print("\n   Sample questions:")
            for i, q in enumerate(questions[:3], 1):
                print(f"\n   Question {q['question_number']}:")
                print(f"   Text: {q['question_text'][:100]}...")
                print(f"   Max Marks: {q['max_marks']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing PDF processor: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("\n" + "🔧 "*20)
    print("DeepSeek-OCR Fix Verification Script")
    print("🔧 "*20 + "\n")
    
    # Test 1: DeepSeek-OCR
    ocr_success = test_deepseek_ocr()
    
    # Test 2: PDF Processor
    if ocr_success:
        processor_success = test_pdf_processor()
    else:
        processor_success = False
    
    # Final Summary
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)
    
    if ocr_success and processor_success:
        print("✅ All tests passed!")
        print("\nThe DeepSeek-OCR fix is working correctly.")
        print("You can now run the main application:")
        print("  python app.py")
    elif ocr_success:
        print("⚠️ OCR works, but PDF processor needs testing with actual files")
        print("\nUpload test PDFs and run the main application:")
        print("  python app.py")
    else:
        print("❌ Some tests failed")
        print("\nPlease check the error messages above.")
        print("Make sure all dependencies are installed.")
    
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
