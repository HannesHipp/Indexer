class Slide:

    def __init__(self, slide_number, pdf_reader) -> None:
        self.pdf_reader = pdf_reader
        self.slide_number = slide_number

    def get_pdf_slide(self):
        return self.pdf_reader.pages[self.slide_number]
