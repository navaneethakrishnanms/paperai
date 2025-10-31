import torch
from transformers import AutoTokenizer, AutoModel
from PIL import Image
import os
from pdf2image import convert_from_path
import tempfile

# Import poppler configuration
try:
    from poppler_config import POPPLER_PATH
except ImportError:
    POPPLER_PATH = None

class DeepSeekOCR:
    """
    DeepSeek-OCR wrapper for extracting text from handwritten documents
    """
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.model_name = "deepseek-ai/DeepSeek-OCR"
        self.initialized = False
        
    def initialize(self):
        """Initialize the model (lazy loading)"""
        if self.initialized:
            return True
            
        try:
            # Check GPU availability
            if not torch.cuda.is_available():
                print("⚠️ Warning: No GPU detected. DeepSeek-OCR requires CUDA for optimal performance.")
                print("   Falling back to CPU (will be slower)")
                
            print("🔄 Loading DeepSeek-OCR tokenizer...")
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_name, 
                trust_remote_code=True
            )
            
            print("📦 Loading DeepSeek-OCR model...")
            try:
                self.model = AutoModel.from_pretrained(
                    self.model_name,
                    trust_remote_code=True,
                    torch_dtype=torch.bfloat16,
                    device_map="auto"
                ).eval()
            except Exception as e:
                print(f"⚠️ Flash attention failed, using eager attention: {e}")
                self.model = AutoModel.from_pretrained(
                    self.model_name,
                    _attn_implementation='eager',
                    trust_remote_code=True,
                    torch_dtype=torch.bfloat16,
                    device_map="auto"
                ).eval()
            
            self.initialized = True
            print("✅ DeepSeek-OCR initialized successfully!")
            return True
            
        except Exception as e:
            print(f"❌ Error initializing DeepSeek-OCR: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def extract_text_from_image(self, image_path: str) -> str:
        """
        Extract text from a single image using DeepSeek-OCR
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Extracted text as string
        """
        if not self.initialized:
            if not self.initialize():
                return ""
        
        try:
            # Prepare prompt for OCR
            prompt = "<image>\n<|grounding|>Convert the document to markdown."
            
            print(f"🚀 Running OCR on image: {os.path.basename(image_path)}")
            
            # Create a temporary directory for output
            with tempfile.TemporaryDirectory() as temp_output_dir:
                # Run inference
                result = self.model.infer(
                    tokenizer=self.tokenizer,
                    prompt=prompt,
                    image_file=image_path,
                    output_path=temp_output_dir,  # Use temp directory instead of None
                    base_size=1024,
                    image_size=640,
                    crop_mode=True,  # Use tiling for better accuracy
                    save_results=False,
                    test_compress=False
                )
                
                return result if result else ""
            
        except Exception as e:
            print(f"❌ Error extracting text from image: {e}")
            # Try simpler configuration
            try:
                print("🔄 Retrying with simpler configuration...")
                with tempfile.TemporaryDirectory() as temp_output_dir:
                    result = self.model.infer(
                        tokenizer=self.tokenizer,
                        prompt=prompt,
                        image_file=image_path,
                        output_path=temp_output_dir,  # Use temp directory instead of None
                        base_size=640,
                        image_size=640,
                        crop_mode=False,
                        save_results=False,
                        test_compress=False
                    )
                    return result if result else ""
            except:
                import traceback
                traceback.print_exc()
                return ""
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """
        Extract text from PDF by converting to images and using DeepSeek-OCR
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Extracted text from all pages
        """
        if not self.initialized:
            if not self.initialize():
                return ""
        
        try:
            print(f"📄 Converting PDF to images: {os.path.basename(pdf_path)}")
            
            # Convert PDF to images with poppler path from config
            if POPPLER_PATH and os.path.exists(POPPLER_PATH):
                images = convert_from_path(pdf_path, dpi=300, poppler_path=POPPLER_PATH)
            else:
                # Try without explicit path (assumes poppler in PATH)
                images = convert_from_path(pdf_path, dpi=300)
            
            all_text = []
            
            # Create temporary directory for images
            with tempfile.TemporaryDirectory() as temp_dir:
                for i, image in enumerate(images, 1):
                    print(f"📄 Processing page {i}/{len(images)}...")
                    
                    # Save image temporarily
                    temp_image_path = os.path.join(temp_dir, f"page_{i}.jpg")
                    image.save(temp_image_path, 'JPEG')
                    
                    # Extract text from image
                    page_text = self.extract_text_from_image(temp_image_path)
                    
                    if page_text:
                        all_text.append(f"\n--- Page {i} ---\n{page_text}\n")
            
            combined_text = "\n".join(all_text)
            print(f"✅ Successfully extracted text from {len(images)} pages")
            
            return combined_text
            
        except Exception as e:
            print(f"❌ Error extracting text from PDF: {e}")
            import traceback
            traceback.print_exc()
            return ""
    
    def cleanup(self):
        """Clean up model resources"""
        if self.model is not None:
            del self.model
            self.model = None
        
        if self.tokenizer is not None:
            del self.tokenizer
            self.tokenizer = None
        
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
        
        self.initialized = False
        print("🧹 DeepSeek-OCR resources cleaned up")


# Singleton instance
_deepseek_ocr_instance = None

def get_deepseek_ocr():
    """Get or create singleton DeepSeek-OCR instance"""
    global _deepseek_ocr_instance
    if _deepseek_ocr_instance is None:
        _deepseek_ocr_instance = DeepSeekOCR()
    return _deepseek_ocr_instance
