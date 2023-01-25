class Filter:

    def __init__(self) -> None:
        pass

    def filter_words(self, dataframe):
        pass

    def filter_stopwords(self, dataframe):
        pass

    def filter_nouns(self, dataframe):
        pass


class Indexer:
    def __init__(self, text, lang='en'):
        self.text = text
        self.lang = lang
        self.index = {}

    def create_index(self, threshold=10):
        # tokenize the text
        tokens = word_tokenize(self.text, language=self.lang)

        # remove stop words
        stop_words = set(stopwords.words(self.lang))
        filtered_tokens = [token for token in tokens if token.lower() not in stop_words]

        # part of speech tagging
        tagged = nltk.pos_tag(filtered_tokens, lang=self.lang)

        # extract only nouns
        nouns = [word for word, pos in tagged if pos.startswith('NN')]

        # create a dictionary where the keys are the nouns and the values are the pages where the nouns appear
        for i, token in enumerate(tagged):
            if token[1].startswith('NN'):
                if token[0] in self.index:
                    self.index[token[0]].append(i//len(tokens) + 1)
                else:
                    self.index[token[0]] = [i//len(tokens) + 1]

        # remove words that appear more than the threshold value
        self.index = {word: pages for word, pages in self.index.items() if len(pages) <= threshold}