
from collections import Counter
import re


def index_slides(slides: dict[int, list[tuple[str, str]]]) -> dict[str, dict[str, dict[int, int]]]:
    index: dict[str, dict[str, dict[int, int]]] = {}

    for slide_num, concepts in slides.items():
        concept_counts = Counter(concepts)
        for (adjectives, noun), count in concept_counts.items():
            if noun not in index:
                index[noun] = {}
            if adjectives not in index[noun]:
                index[noun][adjectives] = {}
            index[noun][adjectives][slide_num] = count

    return index
