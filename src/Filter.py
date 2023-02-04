from nltk.corpus import stopwords
import math
from typing import Dict, List
from src.Slide import Slide

stopwords_ = [word.capitalize() for word in stopwords.words("german")]


def filter_words(words: Dict[str, List[Slide]]) -> Dict[str, List[Slide]]:
    max_page_number = get_max_page_number(words)
    for word in list(words):
        if should_be_removed(word) or not is_dense(words[word], max_page_number):
            words.pop(word)
    return words


def get_max_page_number(words_dict):
    max = 0
    for slides in words_dict.values():
        for slide in slides:
            if slide.global_slide_num > max:
                max = slide.global_slide_num
    return max


def should_be_removed(word):
    if not word[0].isupper():
        return True
    if is_stopword(word):
        return True
    if not is_noun(word):
        return True
    return False


def is_stopword(word):
    if word in stopwords_:
        return True
    return False


def is_noun(word):
    return True


def is_dense(slides, max_page_number):
    if len(slides) == 1:
        return True
    diff_schwelle = 10
    abstand_schwelle = max_page_number / 5
    max_streak_length = math.ceil(max_page_number / 20)

    numbers = [slide.global_slide_num for slide in slides]
    numbers = sorted(numbers)

    big_diffs = []
    first = numbers.pop(0)
    last = first
    streak_counter = 0
    for number in numbers:
        diff = number - last
        if diff > diff_schwelle:
            big_diffs.append(diff)
            streak_counter = 0
        else:
            streak_counter += 1
            if streak_counter > max_streak_length:
                return False
        last = number

    if len(big_diffs) != 0:
        avrg_diff = sum(big_diffs)/len(big_diffs)
        if avrg_diff > abstand_schwelle:
            return True
    return False
