from src.Extractor import Extractor, PDFExtractionStrategy, OCRExtractionStrategy
from src.parsing import parse_text
from src.filtering import filter_index
from src.exporting import export_index

def main():
    input_paths = [
        r"ressources\Skript.pdf"
    ]

    slides_per_page = 1
    filter_agressiveness = 0.1

    extractor = Extractor(OCRExtractionStrategy())


    print("extract slides")
    all_slides = extractor.extract_slides(input_paths)

    print("create index and extract words")
    index: dict[str,set] = {}

    for slide in all_slides:
        slide_words, slide.text = parse_text(slide.text)
        for slide_word in slide_words:
            if not slide_word in index:
                index[slide_word] = set()
            index[slide_word].add(slide)

    print("filter index")
    index, removed_words = filter_index(index, all_slides, filter_agressiveness) 

    print("export index")
    export_index(index, slides_per_page, removed_words)

if __name__ == '__main__':
    main()
