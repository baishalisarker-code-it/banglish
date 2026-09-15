"""
Language and Script Detector
Accurately distinguishes Bengali script, Romanized Bengali (Banglish),
Mixed/Code-switched sentences, and English.
"""

import re
from typing import Dict, Any

BN_RANGE = re.compile(r"[\u0980-\u09FF]")
LATIN_WORD = re.compile(r"[A-Za-z]+")

# Comprehensive Banglish / Romanized Bengali Lexicon
ROMAN_BN_LEXICON = {
    # Pronouns
    "ami", "tumi", "apni", "amra", "tora", "tui", "tomra", "apnara",
    "tara", "se", "she", "o", "ei", "oi", "tai", "oder", "amader", "tomader",
    # Verbs & Conjugations
    "achi", "acho", "ache", "achhe", "achhi", "jaabo", "jabo", "jacchi", "gechi",
    "kori", "korchi", "korlam", "korbo", "korechi", "korte", "korle",
    "hobe", "hoyeche", "hoise", "hocche", "holo", "hoy",
    "pari", "parbo", "parchi", "parlam", "chai", "chaile", "bolchi", "bollam",
    "dekhi", "dekhlam", "dekhbo", "shunlam", "shunbo", "jani", "janlam",
    # Adverbs / Adjectives / Quantifiers
    "bhalo", "kharap", "valo", "khub", "onek", "ektu", "kom", "beshi", "sob",
    "thik", "vul", "sundor", "fultu", "faltu", "baje", "osadharon", "darun",
    # Interrogatives & Conjunctions
    "kemon", "keno", "kothay", "kobe", "ki", "kichu", "kintu", "ar", "ebong",
    "ba", "naki", "kar", "kake", "kokhon",
    # Negations & Assertions
    "na", "nai", "noy", "nah", "haan", "hha",
    # Nouns & Common Colloquial words
    "kaj", "kajta", "shomoy", "din", "raat", "shokal", "bikel",
    "bhai", "bon", "maa", "baba", "bondhu", "prem", "bhalobashi",
    "dhonnobad", "shubho", "khobor", "mon", "kotha", "matha", "baper", "mama"
}

def detect_language(chunk: str) -> Dict[str, Any]:
    """
    Detects the language and script type for a given text chunk.
    
    Returns:
        dict: {
            "lang": "bn" | "en" | "unknown",
            "script": "Bengali" | "Romanized" | "Mixed" | "Latin",
            "note": Descriptive human-readable label,
            "bn_char_count": int,
            "roman_hits": int
        }
    """
    chunk = (chunk or "").strip()
    if not chunk:
        return {
            "lang": "unknown",
            "script": "Unknown",
            "note": "Empty text",
            "bn_char_count": 0,
            "roman_hits": 0
        }
    
    bn_chars = len(BN_RANGE.findall(chunk))
    latin_words = LATIN_WORD.findall(chunk)
    roman_hits = sum(1 for w in latin_words if w.lower() in ROMAN_BN_LEXICON)
    
    # Pure Bengali script
    if bn_chars >= 2 and roman_hits == 0 and len(latin_words) == 0:
        return {
            "lang": "bn",
            "script": "Bengali",
            "note": "Bengali (Script)",
            "bn_char_count": bn_chars,
            "roman_hits": roman_hits
        }
    
    # Mixed script / Code-switching
    if bn_chars >= 1 and (roman_hits >= 1 or len(latin_words) >= 1):
        return {
            "lang": "bn",
            "script": "Mixed",
            "note": "Bengali (Mixed / Code-Switch)",
            "bn_char_count": bn_chars,
            "roman_hits": roman_hits
        }
    
    # Romanized Bengali (Banglish)
    if roman_hits >= 1 and bn_chars == 0:
        return {
            "lang": "bn",
            "script": "Romanized",
            "note": "Bengali (Romanized / Banglish)",
            "bn_char_count": bn_chars,
            "roman_hits": roman_hits
        }
        
    # English
    if latin_words and roman_hits == 0 and bn_chars == 0:
        return {
            "lang": "en",
            "script": "Latin",
            "note": "English",
            "bn_char_count": bn_chars,
            "roman_hits": 0
        }
    
    # Fallback if Bengali characters are present
    if bn_chars > 0:
        return {
            "lang": "bn",
            "script": "Bengali",
            "note": "Bengali (Script)",
            "bn_char_count": bn_chars,
            "roman_hits": roman_hits
        }
        
    return {
        "lang": "en",
        "script": "Latin",
        "note": "English / Latin Script",
        "bn_char_count": 0,
        "roman_hits": 0
    }
