from pypdfium2 import OptimiseMode, PdfPage


class Slide:

    def __init__(self, global_slide_num, pdf_doc, local_slide_num) -> None:
        self.pdf_doc = pdf_doc
        self.global_slide_num = global_slide_num
        self.local_slide_num = local_slide_num
        self.sentences = None

    def get_pdf_slide(self) -> PdfPage:
        return self.pdf_doc.get_page(self.local_slide_num)

    def get_image(self):
        return self.get_pdf_slide().render_topil(
            scale=300/72,
            rotation=0,
            crop=(0, 0, 0, 0),
            greyscale=False,
            optimise_mode=OptimiseMode.NONE,
        )
