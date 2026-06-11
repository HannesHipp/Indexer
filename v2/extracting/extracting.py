import fitz
from tqdm import tqdm

from .grouping.block_grouping import get_block_groups
from .grouping.text_grouping import get_text_groups
from .cleaning import clean_text


def extract_text_from_slide(page):
    block_groups = get_block_groups(page)
    text_groups = get_text_groups(block_groups)

    text = []
    for group in text_groups:
        sentences = clean_text(group)
        text.extend(sentences)
    return text
        

def extract_text(paths) -> dict:
    all_slides = {}
    
    global_page_num = 1
    for doc_num, path in enumerate(paths):
        doc = fitz.open(path)
        print(F"Document {doc_num + 1} of {len(paths)}")
        for page_num in tqdm(range(len(doc))):
            page = doc[page_num]
            text = extract_text_from_slide(page)
            all_slides[global_page_num] = text
            global_page_num += 1
    return all_slides
