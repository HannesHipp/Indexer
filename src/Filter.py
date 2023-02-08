from nltk.corpus import stopwords
import math
from typing import Dict, List
from src.Slide import Slide

stopwords_ = [word.capitalize() for word in stopwords.words("german")]


def filter_words(words: Dict[str, List[Slide]]) -> Dict[str, List[Slide]]:
    max_page_number = get_max_page_number(words)
    removed_words = {}
    for word in list(words):
        # if word == "Absorberrohr":
        #     print("Hello")
        if should_be_removed(word) or not is_dense(words[word], max_page_number):
            removed_slides = words.pop(word)
            removed_words[word] = removed_slides

    index = {}
    for word in removed_words:
        page_numbers = []
        for slide in removed_words[word]:
            page_numbers.append(slide.global_slide_num)
        index[word] = page_numbers
    index = dict(sorted(index.items()))
    with open("removed.txt", "w+") as o:
        for word in index:
            o.write(f"{word}: {str(index[word])}\n")
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
    new_streak_after = 10
    max_num_streaks = 5
    max_streak_length = math.ceil(max_page_number / 60)

    numbers = [slide.global_slide_num for slide in slides]
    numbers = sorted(numbers)

    num_of_streaks = 0
    streak_counter = 0

    first = numbers.pop(0)
    last = first
    for number in numbers:
        diff = number - last
        if diff > new_streak_after:
            num_of_streaks += 1
            streak_counter = 0
        else:
            streak_counter += 1
            if streak_counter > max_streak_length:
                return False
        last = number

    if num_of_streaks > max_num_streaks:
        return False
    return True
