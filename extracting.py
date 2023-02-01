from PyPDF2 import PdfWriter, PdfReader
import pytesseract
import pdf2image
from Slide import Slide
import re
import os


def extract_words_from_files(paths):
    pdf_reader = PdfReader(merge_files_from_paths(paths))
    words = {}
    page_number = 1
    for path in paths:
        images = pdf2image.convert_from_path(path, dpi=300)
        for image in images:
            slide = Slide(page_number, pdf_reader)
            for word in extract_words_from_image(image):
                if word in words:
                    if not slide in words[word]:
                        words[word].append(slide)
                else:
                    words[word] = [slide]
            page_number += 1
    return words


def merge_files_from_paths(paths):
    output = "merged.pdf"
    pdf_writer = PdfWriter()
    for path in paths:
        pdf_reader = PdfReader(path)
        for page_number in range(len(pdf_reader.pages)):
            pdf_writer.add_page(pdf_reader.pages[page_number])
    with open(output, 'wb') as out:
        pdf_writer.write(out)
    return output


def extract_words_from_image(image):
    words = []
    raw_text = pytesseract.image_to_string(image)
    raw_words_list = re.split("[^a-zA-ZäöüÄÖÜß]", raw_text)
    raw_words_list = ' '.join(raw_words_list).split()
    words = [word for word in raw_words_list if len(word) != 1]
    return words
