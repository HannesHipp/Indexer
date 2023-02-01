# import nltk
from nltk.corpus import stopwords

stopwords_ = [word.capitalize() for word in stopwords.words("german")]


def filter_words(words):
    for word in list(words):
        if should_be_removed(word):
            words.pop(word)
    return words


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
