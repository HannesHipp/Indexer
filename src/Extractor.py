from typing import List
from pypdfium2 import PdfDocument
import pytesseract
from src.Slide import Slide
import re
from abc import ABC, abstractmethod

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'


class Extractor:

    def __init__(self, paths, sentence_extraction_strategy) -> None:
        self.sentence_extraction_strategy = sentence_extraction_strategy
        slides = []
        global_page_num = 1
        for path in paths:
            pdf_doc = PdfDocument(path)
            for page_num in range(len(pdf_doc)):
                slides.append(Slide(global_page_num, pdf_doc, page_num))
                global_page_num += 1
        self.slides = slides

    def extract_sentences_into_slides(self):
        for slide in self.slides:
            slide.sentences = self.sentence_extraction_strategy.extract_from(
                slide)
        return self.slides


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
