import re
from unidecode import unidecode
from . import constants as const

def remove_links(text: str) -> str:
    return const.RE_LINKS.sub('', text)

def remove_math(text: str) -> str:
    return const.RE_MATH.sub('', text)

def remove_numbers_and_keep_norms(text):
    def is_in_matches(start, end):
        return any(ms <= start < me or ms < end <= me for ms, me in matches)
    def replacer(match):
        start, end = match.span()
        return match.group() if is_in_matches(start, end) else ""
    matches = [m.span() for m in const.RE_NORMS.finditer(text)]
    cleaned_text = const.RE_NUMBERS.sub(replacer, text)
    return cleaned_text

def remove_special_chars(text: str) -> str:
    text = const.RE_SPECIAL_CHARS.sub(". ", text)
    # punctuation . , : ; ! ? ' ’ " “ / \ ( ) -
    text = const.RE_HYPHENS.sub(". ", text)
    brackets = const.RE_BRACKET_SENTENCES.findall(text)
    text = const.RE_BRACKET_SENTENCES.sub(" ", text)
    for bracket in brackets:
        text = f"{text}. {bracket}."
    text = const.RE_BRACKET_POINTS.sub(". ", text)
    text = const.RE_BRACKETS.sub(" ", text)
    # punctuation . , : ; ! ? ' ’ " “ / \ -
    text = const.RE_SLASH.sub(" or ", text)
    # punctuation . , : ; ! ? ' ’ " “ -
    text = const.RE_QUOTES.sub(" ", text)
    # punctuation . , : ; ! ? ' ’ -
    text = text.replace("’", "'")
    # punctuation . , : ; ! ? ' -
    text = const.RE_APOSTROPHES.sub("", text)
    text = text.replace(";", ".")
    # punctuation . , : ! ? ' -
    return text

def remove_single_letter_words(text: str) -> str:
    return const.RE_SINGLE_LETTER_WORDS.sub('', text)

def remove_random_puctuation(text: str) -> str:
    return const.RE_PUNCT_NO_WORD_BEFORE.sub("", text)

def clean_spaces(text: str) -> str:
    text = const.RE_SPACE_BEFORE_PUNCT.sub(r"\1\2", text)
    text = const.RE_MULTIPLE_SPACES.sub(" ", text)
    return text.strip()

def clean_text(text: str) -> list:
    text = remove_links(text)
    text = remove_math(text)
    text = unidecode(text)
    text = remove_numbers_and_keep_norms(text)
    text = remove_special_chars(text)
    text = remove_single_letter_words(text)

    # keep long capitalized words (len > 2) where all the other letters except the first are lowercase: e.g. "Home"
    # keep all words that are only capitalized and have length > 2: e.g. "PDF"
    # send all other words to the spell checker and make them lowercase
    word_map = {word.lower(): word for word in const.RE_WORDS.findall(text) 
                if not (word[0].isupper() and word[1:].islower() and len(word) > 3) 
                and not (word.isupper() and len(word) > 2)}

    misspelled_words = [word_map[w] for w in const.SPELL_CHECKER.unknown(list(word_map.keys()))]

    for word in misspelled_words:
        text = text.replace(word, '')
    
    text = remove_random_puctuation(text)
    text = clean_spaces(text)

    sentences = [part.strip() for part in text.split('.') if part.strip()]
    return sentences