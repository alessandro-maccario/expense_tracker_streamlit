"""Reference:
- https://learnopencv.com/edge-detection-using-opencv/
"""

import sys
import os
import pytesseract


# Add the root folder to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sandbox.image_processing import ImageProcessing
from sandbox.text_extraction import TextExtraction

# define where tesseract lies
pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract.exe"

# image processing
image_processing = ImageProcessing()
search_contours = image_processing.topdown_view()

# text extraction
text_extraction = TextExtraction()
content = text_extraction.extract_info()
print(content)
