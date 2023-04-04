import re
from pdf2image import convert_from_path
import pandas as pd
from pytesseract import image_to_string
import time
from api import data_str
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'


pdf_file = 'whole exome sequencing (1).pdf'

images = convert_from_path(pdf_file,poppler_path=r'C:\\Users\\s\\Downloads\\poppler-22.12.0\\Library\\bin')

final_text = ""
for pg, img in enumerate(images):
    st = time.time()
    final_text += image_to_string(img)
    en = time.time()

    print(pg)
    with open("whole_exome.txt","a")as f:
        f.write(final_text)
        f.write('\n')