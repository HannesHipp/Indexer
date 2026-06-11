from extracting.extracting import extract_text
from parsing.parsing import parse_text 
from indexing import index_slides
from exporting.exporting import export_data
from filtering import IndexFilter




pdf_paths = [r"ressources\DL-Slides.pdf"]
slides_per_page = 9

filter = IndexFilter(
    gap_percentage=0.03,
    max_group_range=40,
    max_outliers=7,
    max_total=40
)

print('Extracting text...')
slides = extract_text(pdf_paths)
number_of_slides = len(slides)

print('Parsing text...')
slides = parse_text(slides)

print('Creating index...')
index = index_slides(slides)

# import json
# # # Save the index to a JSON file
# # with open('index.json', 'w') as json_file:
# #     json.dump(index, json_file)

# # Load the index from the JSON file
# with open('index.json', 'r') as json_file:
#     data = json.load(json_file)
#     # Convert keys to integers
#     index = {key: {k: {int(inner_k): inner_v for inner_k, inner_v in inner_dict.items()} for k, inner_dict in value.items()} for key, value in data.items()}

print("Filtering index...")
index, removed_words = filter.filter_index(index, max(slides.keys()))

print("Exporting data...")
export_data(index, slides_per_page, removed_words)

print("Done!")