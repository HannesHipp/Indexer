import PyPDF2
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# open the PDF file
pdf_file = open('example.pdf', 'rb')

# create a PDF reader object
pdf_reader = PyPDF2.PdfFileReader(pdf_file)

# create an empty string to store the text
text = ""

# iterate over each page in the PDF
for page in range(pdf_reader.numPages):
    # extract the text from the page
    text += pdf_reader.getPage(page).extractText()

# close the PDF file
pdf_file.close()

# tokenize the text
tokens = word_tokenize(text)

# remove stop words
stop_words = set(stopwords.words('english'))
filtered_tokens = [token for token in tokens if token.lower() not in stop_words]

# lemmatize the tokens
lemmatizer = WordNetLemmatizer()
lemmatized_tokens = [lemmatizer.lemmatize(token) for token in filtered_tokens]

# part of speech tagging
tagged = nltk.pos_tag(lemmatized_tokens)

# extract only nouns
nouns = [word for word, pos in tagged if pos.startswith('NN')]

# create a frequency distribution of the nouns
index = {}
for noun in nouns:
    if noun in index:
        index[noun] += 1
    else:
        index[noun] = 1

#print the index
print(index)