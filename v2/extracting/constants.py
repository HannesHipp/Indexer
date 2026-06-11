from spellchecker import SpellChecker
import re
from constants import RE_NORM

print("Loading extraction constants...")

SPELL_CHECKER = SpellChecker()
RE_LINKS = re.compile(r'\S*\/\S*\.\S*')
RE_MATH = re.compile(r'[\U0001D400-\U0001D7FF\U00002200-\U000022FF\U000027C0-\U000027EF\U00002980-\U000029FF]')
RE_NORMS = re.compile(RE_NORM)
RE_NUMBERS = re.compile(r'\d+([^\d\w]+\d+)*')
RE_SPECIAL_CHARS = re.compile(r"[^A-Za-z0-9.,:;!?'’\"“/\\\(\)\-\s]+")
RE_HYPHENS = re.compile(r"(?<!\w)-|-(?!\w)")
RE_BRACKET_SENTENCES = re.compile(r"\((.*?)\)")
RE_BRACKET_POINTS = re.compile(r"(\b(\w|\d))\)")
RE_BRACKETS = re.compile(r"\(|\)")
RE_SLASH = re.compile(r"\/|\\")
RE_QUOTES = re.compile(r"\"|“")
RE_APOSTROPHES = re.compile(r"(?<!s)['](?!(?:s|t|m|d|ll|ve|re))")
RE_SPACE_BEFORE_PUNCT = re.compile(r"(\w)\s+([.,:!?'\-])")
RE_SINGLE_LETTER_WORDS = re.compile(r"(?<!['’])\b(?![aI])\w\b")
RE_PUNCT_NO_WORD_BEFORE = re.compile(r"(?<!\w)[.,:!?'\-]")
RE_MULTIPLE_SPACES = re.compile(r"\s+")
RE_WORDS = re.compile(r'\b\w+\b')