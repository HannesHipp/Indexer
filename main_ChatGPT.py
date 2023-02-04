from src.Extractor import *
from Filter import *


def main():
    pdf_file = 'path_to_your_pdf_file'
    lang = input("Enter the language (en/de): ")
    ocr_extractor = OCRTextExtractor(pdf_file, lang)
    ocr_extractor.extract_text()
    indexer = Indexer(ocr_extractor.page_nouns)
    index = indexer.create_index()
    indexer.save_index()


if __name__ == '__main__':
    main()
