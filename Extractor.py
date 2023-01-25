class Extractor:

    def __init__(self) -> None:
        pass

    def extract_words_from_pdf_files(self, files: list):
        for file in files:
            words = self.extract_words_from_pdf_file(file) #?
        # do something with words

    def extract_words_from_pdf_file(self, file):
        for page in file:
            words = self.extract_words_from_pdf_page(page)
    
    def extract_words_from_pdf_page(self, page):
        pass


