from typing import List
from pypdfium2 import PdfDocument
import pytesseract
from src.Slide import Slide
import re
from abc import ABC, abstractmethod

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'


class Extractor:

    def __init__(self, sentence_extraction_strategy) -> None:
        self.sentence_extraction_strategy = sentence_extraction_strategy

    def extract_slides(self, paths):
        slides = []
        global_page_num = 1
        for path in paths:
            pdf_doc = PdfDocument(path)
            for page_num in range(len(pdf_doc)):
                slide = Slide(global_page_num, pdf_doc, page_num)
                slide.sentences = self.sentence_extraction_strategy.extract_from(
                    slide)
                slides.append(slide)
                global_page_num += 1
        return slides


class SentenceExtractionStrategy(ABC):
    @abstractmethod
    def extract_from(self, slide: Slide) -> List[str]:
        pass


class PDFSentenceExtractionStrategy(SentenceExtractionStrategy):
    def extract_from(self, slide: Slide) -> List[str]:
        raw_text = slide.get_pdf_slide().get_textpage().get_text_bounded()
        sentences = raw_text.split("\n")
        return sentences


class OKRSentenceExtractionStrategy(SentenceExtractionStrategy):
    def extract_from(self, slide: Slide) -> List[str]:
        raw_text = pytesseract.image_to_string(slide.get_image())
        sentences = raw_text.split("\n\n")
        return sentences
