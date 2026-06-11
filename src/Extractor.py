from typing import List
import fitz
import pytesseract
from src.Slide import Slide
import re
from abc import ABC, abstractmethod

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'


class TextExtractionStrategy(ABC):
    @abstractmethod
    def extract(self, slide: Slide) -> List[str]:
        pass


class PDFExtractionStrategy(TextExtractionStrategy):
    def extract(self, slide: Slide) -> List[str]:
        return slide.get_pdf_slide().get_textpage().get_text_bounded()
        


class OCRExtractionStrategy(TextExtractionStrategy):
    def extract(self, slide: Slide) -> List[str]:
        return pytesseract.image_to_string(slide.get_image())


class Extractor:

    def __init__(self, text_strategy) -> None:
        self.text_strategy: TextExtractionStrategy = text_strategy

    def extract_slides(self, paths):
        all_slides = []
        
        global_page_num = 1
        for path in paths:
            pdf_doc = fitz.open(path)
            for page_num in range(len(pdf_doc)):
                slide = Slide(global_page_num, pdf_doc, page_num)
                all_slides.append(slide)
                slide.text = self.text_strategy.extract(slide)
                global_page_num += 1
        return all_slides