from src.Extractor import Extractor, PDFSentenceExtractionStrategy, OKRSentenceExtractionStrategy
from src.Filter import WordFilter
from src.Exporter import IndexExporter
from src.Slide import Slide
from src.SentenceParser import SentenceParser
import os
import glob
import nltk


def main():
    input_paths_backup = [
        "ressources\\test_data\\V1.pdf",
        "ressources\\test_data\\V2.pdf",
        "ressources\\test_data\\V3.pdf",
        "ressources\\test_data\\V4.pdf",
        "ressources\\test_data\\V5.pdf",
        "ressources\\test_data\\V6.pdf",
        "ressources\\test_data\\V7.1.pdf",
        "ressources\\test_data\\V8.pdf",
        "ressources\\test_data\\V9.pdf",
        "ressources\\test_data\\V10.pdf",
        "ressources\\test_data\\V11.pdf",
        "ressources\\test_data\\V12.pdf",
        "ressources\\test_data\\V13.pdf"
    ]
    input_paths = get_pdf_files()

    grouping = (3, 3)  # not active yet
    output_path = "src/index.xlsx"

    print("start extraction")
    extractor = Extractor(PDFSentenceExtractionStrategy())
    slides = extractor.extract_slides(input_paths)

    print("start parsing")
    parser = SentenceParser(None)
    words = parser.parse_slides(slides)

    print("start filter")
    # filter = Filter(None)
    word_filter = WordFilter()
    words = word_filter.filter_words(words)

    print("start export")
    index_exp = IndexExporter()
    index = index_exp.generate_index(words, output_path, grouping)
    # document = exporter.gernerate_document(words, output_path)


def get_pdf_files():
    dir_name = "ressources"
    if not os.path.isdir(dir_name):
        raise FileNotFoundError(f"{dir_name} directory not found")
    pdf_files = glob.glob(os.path.join(dir_name, "**/*.pdf"), recursive=True)
    return pdf_files

def debug():
    #TODO Für neue Benutzer geht der Code nicht, Sie müssen als erstes nltk.download benutzen. Da müssen wir noch eine Lösung finden.
    nltk.download('stopwords')
    pdf = get_pdf_files()
    print(pdf)


if __name__ == '__main__':
    main()
