from tqdm import tqdm

from .concepts import identify_concepts


def parse_text(slides: dict[int, list[str]]) -> None:
    for slide_num, sentences in tqdm(slides.items()):
        concepts = []
        for sentence in sentences:
            concepts.extend(identify_concepts(sentence))
        slides[slide_num] = concepts
    return slides
    