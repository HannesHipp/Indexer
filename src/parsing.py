import re

def parse_text(text):
    words = []
    clean_text = ''

    for word in text.split():
        if '\x02' in word:
            sub_words = word.split('\x02')
            word = sub_words.pop(0)
            for sub_word in sub_words:
                word = word + sub_word.lower()
        word = re.sub("[^a-zA-ZäöüÄÖÜß]", '', word).strip()
        clean_text += word + ' '
        if len(word) > 1:
            words.append(word)
    return words, clean_text
