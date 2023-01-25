import PyPDF2
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# open the PDF file
pdf_file = open('test_data\\V1.pdf', 'rb')

# create a PDF reader object
pdf_reader = PyPDF2.PdfReader(pdf_file)

# create an empty string to store the text
text = ""

# iterate over each page in the PDF
for page_number in range(len(pdf_reader.pages)):
    # extract the text from the page
    text += pdf_reader.pages[page_number].extract_text()

# close the PDF file
pdf_file.close()

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