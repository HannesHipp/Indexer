import re
from collections import Counter, defaultdict
from nltk.corpus import wordnet

from . import constants as const
from .pos import POS


STAT_WEIGHT = 0.2
TRANS_WEIGHT = 0.3
WORDNET_WEIGHT = 0.5

def identify_concepts(text):
    tagged_tokens = classify_text(text)
    concepts = collect_concepts(tagged_tokens)
    return concepts

def classify_text(text):
    known_tokens, text = replace_known_tokens(text)

    stat_tags, _ = spacy_tagging(text, const.STAT_MODEL)
    trans_tags, doc = spacy_tagging(text, const.TRANS_MODEL)

    tokens = list(stat_tags)
    for i, (token, _) in enumerate(tokens):
        if rule_pos := rule_based_tagging(token):
            tokens[i] = (token, rule_pos)
            continue

        pos_candidates = [(stat_tags[i][1], STAT_WEIGHT),    
                          (trans_tags[i][1], TRANS_WEIGHT)]
        
        if pos_wordnet := wordnet_tagging(token):
            for pos, weight in pos_wordnet.items():
                pos_candidates.append((pos, weight * WORDNET_WEIGHT))

        final_tag = weighted_voting(pos_candidates)
        tokens[i] = (token, final_tag)

    tokens = restore_known_tokens(doc, tokens, known_tokens)

    tokens = [(token, pos) for token, pos in tokens 
              if not (len(token) == 1 and not token.isalnum())]
    return tokens

def replace_known_tokens(text):
    known_tokens = []
    new_text = list(text)  # Convert to a list for easier manipulation.
    offset = 0  # This keeps track of the overall offset due to replacements.
    
    for pos_tag, patterns in const.KNOWN_TOKENS.items():
        for (regex, replacement) in patterns:
            for match in regex.finditer(text):
                start = match.start() + offset
                end = match.end() + offset
                match_text = match.group(0)
                known_tokens.append(((start, start + len(replacement)), match_text, pos_tag))
                new_text[start:end] = replacement
                offset += len(replacement) - (end - start)
            
    return known_tokens, ''.join(new_text)

def spacy_tagging(text, model):
    doc = model(text)
    return [(token.text, map_spacy_tags(token.pos_)) for token in doc], doc

def map_spacy_tags(pos):
    if pos == "NOUN" or pos == "PROPN":
        return POS.NOUN
    elif pos == "ADJ":
        return POS.ADJ
    return POS.OTHER

def rule_based_tagging(word):
    for pos, patterns in const.RULE_BASED_PATTERNS.items():
        for pattern in patterns:
            if pattern.fullmatch(word, re.IGNORECASE):
                return pos 
    return None

def wordnet_tagging(word):
    synsets = wordnet.synsets(word)
    if not synsets:
        return None
    pos_counts = defaultdict(int)
    for synset in synsets:
        pos = synset.pos()
        pos_counts[pos] += 1
    if not pos_counts:
        return None
    pos_distribution = {
        POS.NOUN: pos_counts["n"] / len(synsets),
        POS.ADJ: (pos_counts["a"] + pos_counts['s']) / len(synsets),
        POS.OTHER: 1.0 - ((pos_counts["n"] + pos_counts["a"] + pos_counts["s"]) / len(synsets))
    }
    return pos_distribution

def weighted_voting(pos_candidates):
    score = defaultdict(float)
    for (pos_tag, weight) in pos_candidates:
        score[pos_tag] += weight
    return max(score, key=score.get)

def restore_known_tokens(doc, tokens, known_tokens):
    if not known_tokens:
        return tokens
    
    known_tokens.sort(key=lambda x: x[0][0])
    new_tokens = []
    i = 0
    while i < len(tokens):
        if not known_tokens:
            new_tokens.extend(tokens[i:])
            break
        (start, end), replacement, pos = known_tokens.pop(0)
        span = doc.char_span(start, end, alignment_mode="expand")
        start = span.start
        end = span.end
        while i < start:
            new_tokens.append(tokens[i])
            i += 1
        new_tokens.append((replacement, pos))
        i = end

    return new_tokens

def collect_concepts_(tagged_tokens):
    concepts = []
    adjectives = ''
    nouns = ''

    for (word, pos) in tagged_tokens:
        word = format_concepts(word, pos)

        if pos == POS.OTHER:
            if nouns:
                concepts.append((adjectives.strip(), nouns.strip()))
                adjectives = ''
                nouns = ''
            continue

        if pos == POS.NOUN:
            nouns = f'{nouns} {word}'

        elif pos == POS.SINGLE:
            if nouns:
                concepts.append((adjectives.strip(), nouns.strip()))
                adjectives = ''
                nouns = ''
            concepts.append(('', word.strip()))

        elif pos == POS.ADJ:
            if nouns:
                concepts.append((adjectives.strip(), nouns.strip()))
                adjectives = ''
                nouns = ''
            adjectives = f'{adjectives} {word}'

    if nouns:
        concepts.append((adjectives.strip(), nouns.strip()))

    return concepts

def format_concepts(word, pos):
    if pos == POS.ADJ:
        return word.lower()
    elif pos == POS.NOUN:
        if not word.isupper():
            return word.capitalize()
    return word

def collect_concepts(tagged_tokens):
    concepts = []
    adjectives = ''
    nouns = ''

    for (word, pos) in tagged_tokens:
        word = format_concepts(word, pos)

        if pos == POS.NOUN:
            nouns = f'{nouns} {word}'
        else:
            if nouns:
                concepts.append((adjectives.strip(), nouns.strip()))
                adjectives = ''
                nouns = ''
            if pos == POS.SINGLE:
                concepts.append(('', word.strip()))
            elif pos == POS.ADJ:
                adjectives = f'{adjectives} {word}'

    if nouns:
        concepts.append((adjectives.strip(), nouns.strip()))

    return concepts