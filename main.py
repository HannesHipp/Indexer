from extracting import extract_words_from_files
from filtering import filter_words
from exporting import generate_index

# Data Flow
# pdfs -> Extractor -> words_dict: dict[str:Slide] -> Filter -> words_dict: dict[str:Slide] -> Exporter -> pdfs

input_paths = [
    "test_data\\V1.pdf"
    # "test_data\\V2.pdf",
    # "test_data\\V3.pdf",
    # "test_data\\V4.pdf",
    # "test_data\\V5.pdf",
    # "test_data\\V6.pdf",
    # "test_data\\V7.1.pdf",
    # "test_data\\V8.pdf",
    # "test_data\\V9.pdf",
    # "test_data\\V10.pdf",
    # "test_data\\V11.pdf",
    # "test_data\\V12.pdf",
    # "test_data\\V13.pdf"
]
grouping = (3, 3)
output_path = ""

print("start extraction")
words = extract_words_from_files(input_paths)

print("start filter")
words = filter_words(words)

print("start export")
index = generate_index(words, output_path, grouping)
# document = exporter.gernerate_document(words, output_path)
