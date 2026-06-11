import re
import nltk
import spacy
from nltk.corpus import wordnet

from .pos import POS
from constants import RE_NORM

print("Loading parsing constants...")

KNOWN_TOKENS = {
    POS.SINGLE: [(re.compile(pattern), replacement) for pattern, replacement in {
        RE_NORM: 'a norm'
    }.items()]
}
RULE_BASED_PATTERNS = {
    POS.SINGLE: [re.compile(pattern) for pattern in [
        r'\b[A-Z]+\b'
    ]],
    POS.NOUN: [re.compile(pattern) for pattern in [
        r".*tion$", 
        r".*ment$", 
        r".*ness$", 
        r".*ity$", 
        r".*ship$", 
        r".*hood$"
    ]],
    POS.ADJ: [re.compile(pattern) for pattern in [
        r".*ous$", 
        r".*ive$", 
        r".*able$", 
        r".*ible$", 
        r".*ic$", 
        r".*al$", 
        r".*ful$", 
        r".*less$"
    ]]
}
STAT_MODEL = spacy.load("en_core_web_md")
TRANS_MODEL = spacy.load("en_core_web_trf")
try:
    wordnet.ensure_loaded()
except LookupError:
    nltk.download("wordnet")


