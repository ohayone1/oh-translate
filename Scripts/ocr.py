import pytesseract
from PIL import Image
import re
def img_2_text(path):

    # Load the image
    image = Image.open(path)

    # Perform OCR
    ocr_text = pytesseract.image_to_string(image)

    return (ocr_text)