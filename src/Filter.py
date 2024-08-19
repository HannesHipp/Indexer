from nltk.corpus import stopwords
import math
from typing import Dict, List
from src.Slide import Slide

# Use a set for faster membership testing
stopwords_ = set([word.capitalize() for word in stopwords.words("german")])


def filter_words(words: Dict[str, List[Slide]]) -> Dict[str, List[Slide]]:
    max_page_number = get_max_page_number(words)
    removed_words = {}

    for word in list(words):
        if should_be_removed(word) or not is_dense(words[word], max_page_number):
            removed_words[word] = words.pop(word)

    log_removed_words(removed_words)
    return words


def get_max_page_number(words_dict: Dict[str, List[Slide]]) -> int:
    # Use max function with generator expressions
    return max(
        (slide.global_slide_num for slides in words_dict.values() for slide in slides),
        default=0
    )


def should_be_removed(word: str) -> bool:
    # Combine stopword and noun check for efficiency
    return is_stopword(word) or not is_noun(word)


def is_stopword(word: str) -> bool:
    # Check against the stopword set
    return word in stopwords_


def is_noun(word: str) -> bool:
    # Consider German nouns typically start with a capital letter
    return word[0].isupper()


def is_dense(slides: List[Slide], max_page_number: int) -> bool:
    if len(slides) == 1:
        return True

    # Parameters for streak detection
    new_streak_after = 10
    max_num_streaks = 5
    max_streak_length = math.ceil(max_page_number / 60)

    # Extract slide numbers and sort them
    numbers = sorted(slide.global_slide_num for slide in slides)

    num_of_streaks, streak_counter = 0, 0
    last = numbers[0]

    for number in numbers[1:]:
        diff = number - last

        if diff > new_streak_after:
            num_of_streaks += 1
            streak_counter = 0
        else:
            streak_counter += 1
            if streak_counter > max_streak_length:
                return False
        last = number

    return num_of_streaks <= max_num_streaks


def log_removed_words(removed_words: Dict[str, List[Slide]]) -> None:
    # Create an index of removed words with associated page numbers
    index = {
        word: sorted(slide.global_slide_num for slide in slides)
        for word, slides in sorted(removed_words.items())
    }

    # Write the index to a file
    with open("removed.txt", "w+") as o:
        for word, page_numbers in index.items():
            o.write(f"{word}: {page_numbers}\n")
