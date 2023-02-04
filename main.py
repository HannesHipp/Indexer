from src.Extractor import Extractor, PDFSentenceExtractionStrategy, OKRSentenceExtractionStrategy
from src.Filter import filter_words
from src.Exporter import generate_index
from src.SentenceParser import SentenceParser

input_paths = [
    "ressources\\test_data\\V1.pdf"
    # "ressources\\test_data\\V2.pdf",
    # "ressources\\test_data\\V3.pdf",
    # "ressources\\test_data\\V4.pdf",
    # "ressources\\test_data\\V5.pdf",
    # "ressources\\test_data\\V6.pdf",
    # "ressources\\test_data\\V7.1.pdf",
    # "ressources\\test_data\\V8.pdf",
    # "ressources\\test_data\\V9.pdf",
    # "ressources\\test_data\\V10.pdf",
    # "ressources\\test_data\\V11.pdf",
    # "ressources\\test_data\\V12.pdf",
    # "ressources\\test_data\\V13.pdf"
]
grouping = (3, 3)  # not active yet
output_path = ""

print("start extraction")
extractor = Extractor(input_paths, OKRSentenceExtractionStrategy())
slides = extractor.extract_sentences_into_slides()
print("start parsing")
parser = SentenceParser(slides, None)
words = parser.parse_sentences()

print("start filter")
words = filter_words(words)  # needs to be rewritten as a Class

print("start export")
index = generate_index(words, output_path, grouping)
# document = exporter.gernerate_document(words, output_path)
