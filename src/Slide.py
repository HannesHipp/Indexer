# from pypdfium2 import OptimiseMode, PdfPage
from pypdfium2 import PdfPage


class Slide:

    def __init__(self, global_slide_num, pdf_doc, pdf_slide_num) -> None:
        self.pdf_doc = pdf_doc
        self.global_slide_num = global_slide_num
        self.pdf_slide_num = pdf_slide_num
        self.text = None

    def get_pdf_slide(self) -> PdfPage:
        return self.pdf_doc.get_page(self.pdf_slide_num)

    def get_image(self):
        return self.get_pdf_slide().render(scale = 300/72).to_pil()
