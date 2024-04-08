## Image to Text Conversion using OCR

This Python function utilizes Optical Character Recognition (OCR) to extract text from images. It uses the `pytesseract` library to perform OCR on an image and returns the extracted text.

### Function:

```python
import pytesseract
from PIL import Image
import re

def img_2_text(path):
    """
    Convert an image to text using OCR.
    
    Args:
    - path (str): Path to the image file.
    
    Returns:
    - str: Extracted text from the image.
    """
    
    # Load the image
    image = Image.open(path)

    # Perform OCR
    ocr_text = pytesseract.image_to_string(image)

    return ocr_text
```

### Usage:

To use the `img_2_text` function, provide the path to the image file as an argument:

```python
text = img_2_text('path/to/image.jpg')
print(text)
```

### Requirements:

Make sure to install the required packages:

```plaintext
pytesseract==0.3.8
Pillow==8.4.0
```

You can install the required packages using pip:

```bash
pip install pytesseract Pillow
```
before just unpack the 

https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-5.3.1.20230401.exe
