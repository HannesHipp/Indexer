import PyPDF2
import nltk
import pandas as pd
from nltk.corpus import stopwords
from fpdf import FPDF
from Exporter import Exporter
from Extractor import Extractor
from Filter import Filter

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'Index of important words', 0, 1, 'C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'C')


# Data Flow
# pdfs -> Extractor -> dataframe -> Filter -> dataframe -> Exporter -> pdfs
extractor = Extractor()
filter = Filter()
exporter = Exporter()



nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')

# open the PDF file
pdf_file = open('test_data//V1.pdf', 'rb')

# create a PDF reader object
pdf_reader = PyPDF2.PdfReader(pdf_file)

# create an empty string to store the text
text = ""

# iterate over each page in the PDF
for page in range(len(pdf_reader.pages)):
    # extract the text from the page
    text += pdf_reader.pages[page].extract_text()

# close the PDF file
pdf_file.close()

# split the text into tokens using the space character as the delimiter
tokens = text.split()

# remove stop words
stop_words = stopwords.words('german')
filtered_tokens = [token for token in tokens if token.lower() not in stop_words]

# part of speech tagging
tagged = nltk.pos_tag(filtered_tokens, lang='eng')

# extract only nouns
nouns = [word for word, pos in tagged if pos.startswith('NN')]

# create a dictionary where the keys are the nouns and the values are the pages where the nouns appear
index = {}
for i, token in enumerate(tagged):
    if token[1].startswith('NN'):
        if token[0] in index:
            index[token[0]].append(i//len(tokens) + 1)
        else:
            index[token[0]] = [i//len(tokens) + 1]

# set a threshold value
threshold = 10

# remove words that appear more than the threshold value
index = {word: pages for word, pages in index.items() if len(pages) <= threshold}

data = [(word, page) for word, pages in index.items() for page in pages]

# create a DataFrame from the list of tuples
df = pd.DataFrame(data, columns=['word', 'page'])

# create a pdf object
pdf = PDF()

# add a page
pdf.add_page()

# set the font
pdf.set_font('Arial', '', 12)

# iterate over the index and add the word and its count to the pdf file
for word, count in index.items():
    pdf.cell(0, 10, word + ': ' + str(count), 0, 1)

print(index)

# save the pdf to the local directory
pdf.output("index.pdf", "F")

#print the index
#print(index)

#Todo >>> df.groupby(["state", "gender"])["last_name"].count()