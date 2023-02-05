import re
from src.Slide import Slide
from typing import List, Dict


class SentenceParser:

    def __init__(self, parsing_strategy) -> None:
        self.parsing_strategy = parsing_strategy

    def parse_slides(self, slides) -> Dict[str, List[Slide]]:
        words = {}
        for slide in slides:
            for sentence in slide.sentences:
                for word in self.parse_sentence(sentence):
                    if word in words:
                        if not slide in words[word]:
                            words[word].append(slide)
                    else:
                        words[word] = [slide]
        return words

    def parse_sentence(self, sentence: str) -> List[str]:
        raw_words_list = re.split("[^a-zA-ZäöüÄÖÜß]", sentence)
        raw_words_list = ' '.join(raw_words_list).split()
        words = [word for word in raw_words_list if len(word) != 1]
        # add parsing strategy here
        return words
