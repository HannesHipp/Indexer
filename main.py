from src.Extractor import Extractor, PDFSentenceExtractionStrategy
from src.Exporter import generate_index
from src.Slide import Slide
from src.SentenceParser import SentenceParser
from src.Filter import filter_words
import os, glob
import nltk
import logging
import concurrent.futures


def ensure_nltk_data():
    try:
        nltk.data.find('corpora/stopwords.zip')
    except LookupError:
        nltk.download('stopwords')


def get_pdf_files():
    dir_name = "ressources"
    if not os.path.isdir(dir_name):
        raise FileNotFoundError(f"{dir_name} directory not found")
    pdf_files = glob.glob(os.path.join(dir_name, "**/*.pdf"), recursive=True)
    if not pdf_files:
        raise FileNotFoundError("No PDF files found in the specified directory.")
    return pdf_files


def extract_slides_from_pdf(file):
    extractor = Extractor(PDFSentenceExtractionStrategy())
    return extractor.extract_slides([file])


def main():
    logging.basicConfig(level=logging.INFO)

    logging.info("Ensuring NLTK data is available")
    ensure_nltk_data()

    logging.info("Fetching PDF files")
    input_paths = get_pdf_files()

    logging.info("Starting extraction")
    slides = []
    for path in input_paths:
        slides.extend(extract_slides_from_pdf(path))

    logging.info("Parsing slides")
    parser = SentenceParser(None)
    words = parser.parse_slides(slides)

    logging.info("Filtering words")
    words = filter_words(words)

    logging.info("Generating index")
    grouping = (3, 3)
    output_path = ""
    index = generate_index(words, output_path, grouping)

    logging.info("Process completed successfully")


if __name__ == '__main__':
    main()


