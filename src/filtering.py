from nltk.corpus import stopwords
import math
import numpy as np
from typing import Dict, List
from src.Slide import Slide


def filter_index(index: dict[str,set[Slide]], all_slides: List[Slide], threshold_percentage=0.1):
    removed_words = {}
    score_board = {}
    for word in list(index.keys()):
        if (is_stopword(word) 
            or not is_noun(word)):
            removed_words[word] = index.pop(word)
        else:
            score_board[word] = score_word(word, all_slides)
    
    scores_sorted = sorted(score_board.items(), key=lambda item: item[1])
    cutoff_index = int(len(scores_sorted) * threshold_percentage)
    threshold_score = scores_sorted[cutoff_index][1]

    for word, score in scores_sorted:
        if score <= threshold_score and word in index:
            removed_words[word] = index.pop(word)

    visualize_word_scores(scores_sorted, all_slides)

    return index, removed_words


def is_stopword(word):
    if word in [word.capitalize() for word in stopwords.words("german")]:
        return True
    return False


def is_noun(word):
    if word[0].isupper():
        return True
    return False

def score_word(word, all_slides):
    word_occurences = [slide.text.count(word) for slide in all_slides]
    variance = np.var(word_occurences)
    return variance / (sum(word_occurences))

import matplotlib.pyplot as plt

def visualize_word_scores(scores_sorted, all_slides, num_words=10):
    highest_scores = scores_sorted[-num_words:]
    lowest_scores = scores_sorted[:num_words]
    
    combined_scores = lowest_scores + highest_scores

    fig, axes = plt.subplots(len(combined_scores), 1, figsize=(10, len(combined_scores) * 3))
    if len(combined_scores) == 1:
        axes = [axes]  # Ensure axes is iterable if there's only one subplot
    
    for ax, (word, score) in zip(axes, combined_scores):
        word_occurrences = [slide.text.count(word) for slide in all_slides]
        ax.bar(range(len(all_slides)), word_occurrences, color='blue')
        ax.set_xlabel('Slide Index')
        ax.set_ylabel('Word Count')
        ax.set_title(f'Occurrences of "{word}" (Score: {score:.4f}) across slides')

    plt.tight_layout()
    plt.savefig('word_scores_visualization.png')  # Save to a file
    plt.close()  # Close the plot to avoid display issues

# IDEAS:
# nltk filtering for nouns and combinations of nouns and adjectives 
# if adjective noun combination occurs more than once it gets added
# word occurence gaps filtering 
