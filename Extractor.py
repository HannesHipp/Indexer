import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from fpdf import FPDF
from PIL import Image
import pytesseract
import pandas as pd

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

class OCRTextExtractor:
    def __init__(self, pdf_file, lang='en'):
        self.pdf_file = pdf_file
        self.lang = lang
        self.page_nouns = {}

    def extract_text(self):
        pdf_reader = PyPDF2.PdfReader(self.pdf_file)
        for page_number, page in enumerate(pdf_reader.pages):
            # use Tesseract to extract the text from the image
            text = pytesseract.image_to_string(page.stream.get_rawdata(), lang=self.lang)
            # tokenize the text
            tokens = word_tokenize(text, language=self.lang)
            # remove stop words
            stop_words = set(stopwords.words(self.lang))
            filtered_tokens = [token for token in tokens if token.lower() not in stop_words]
            # part of speech tagging
            tagged = nltk.pos_tag(filtered_tokens, lang=self.lang)
            # extract only nouns
            nouns = [word for word, pos in tagged if pos.startswith('NN')]
            # add the page number and nouns to the dictionary
            self.page_nouns[page_number + 1] = nouns

    def save_index(self):
        # create a list of tuples where the first element is the page number and the second element is the noun
        data = [(page, noun) for page, nouns in self.page_nouns.items() for noun in nouns]
        # create a DataFrame from the list of tuples
        df = pd.DataFrame(data, columns=['page', 'noun'])
        # group by page number
        df = df.groupby(['page']).noun.apply(list).reset_index(name='nouns')
        pdf = PDF()
        # iterate over the dataframe and add the word and its count to the pdf file
        for i in range(len(df)):
            pdf.add_page()
            pdf.set_font('Arial', 'B', 16)
            pdf.cell(0, 10, 'Page number: ' + str(df.page[i]), 0, 1, 'C')
            pdf.ln(5)
            pdf.set_font('Arial', '', 12)
            for noun in df.nouns[i]:
                pdf.cell(0, 10, noun, 0, 1)
        pdf.output("index.pdf", "F")

