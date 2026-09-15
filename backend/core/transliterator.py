"""
Romanized Bengali (Banglish) to Bengali Script Transliterator
Converts phonetic Banglish expressions into standardized Bengali unicode characters.
"""

import re

# Comprehensive Romanized Banglish to Bengali Unicode Mapping
ROMAN_TO_BN = {
    # Pronouns
    "ami": "আমি", "tumi": "তুমি", "apni": "আপনি", "amra": "আমরা",
    "tomra": "তোমরা", "tora": "তোরা", "tui": "তুই", "apnara": "আপনারা",
    "tara": "তারা", "se": "সে", "she": "সে", "o": "ও", "ei": "এই", "oi": "ওই",
    "oder": "ওদের", "amader": "আমাদের", "tomader": "তোমাদের",
    
    # Adjectives & Descriptors
    "bhalo": "ভালো", "valo": "ভালো", "kharap": "খারাপ", "khub": "খুব",
    "onek": "অনেক", "ektu": "একটু", "kom": "কম", "beshi": "বেশি",
    "sundor": "সুন্দর", "shundor": "সুন্দর", "faltu": "ফালতু", "fultu": "ফালতু",
    "baje": "বাজে", "osadharon": "অসাধারণ", "darun": "দারুণ", "thik": "ঠিক",
    "vul": "ভুল", "shohoj": "সহজ", "kothin": "কঠিন",
    
    # Negations & Assertions
    "na": "না", "nai": "নাই", "nei": "নেই", "noy": "নয়", "nah": "নাহ",
    "haan": "হ্যাঁ", "ha": "হ্যাঁ", "hha": "হ্যাঁ",
    
    # State & Auxiliary Verbs
    "achi": "আছি", "acho": "আছো", "ache": "আছে", "achhe": "আছে", "achhi": "আছি",
    "chilam": "ছিলাম", "chilo": "ছিল", "chile": "ছিলে",
    
    # Action Verbs
    "jabo": "যাবো", "jaabo": "যাবো", "jacchi": "যাচ্ছি", "gechi": "গেছি", "geche": "গেছে",
    "kori": "করি", "korchi": "করছি", "korlam": "করলাম", "korbo": "করবো",
    "korechi": "করেছি", "korte": "করতে", "korle": "করলে", "kore": "করে",
    "hobe": "হবে", "hoyeche": "হয়েছে", "hoise": "হইছে", "hocche": "হচ্ছে",
    "holo": "হলো", "hoy": "হয়",
    "pari": "পারি", "parbo": "পারবো", "parchi": "পারছি", "parlam": "পারলাম",
    "chai": "চাই", "chaile": "চাইলে", "chao": "চাও",
    "bolchi": "বলছি", "bollam": "বললাম", "bolo": "বলো", "bolte": "বলতে",
    "dekhi": "দেখি", "dekhlam": "দেখলাম", "dekhbo": "দেখবো",
    "shuni": "শুনি", "shunlam": "শুনলাম", "shunbo": "শুনবো",
    "jani": "জানি", "janlam": "জানলাম", "jano": "জানো",
    "miss": "মিস", "love": "লাভ", "call": "কল", "meeting": "মিটিং",
    
    # Interrogatives & Conjunctions
    "kemon": "কেমন", "keno": "কেন", "kothay": "কোথায়", "kobe": "কবে",
    "ki": "কী", "kichu": "কিছু", "kintu": "কিন্তু", "ar": "আর",
    "ebong": "এবং", "ba": "বা", "naki": "নাকি", "kokhon": "কখন",
    
    # Cultural, Relationship & Courtesy
    "kaj": "কাজ", "kajta": "কাজটা", "ta": "টা", "ti": "টি",
    "shomoy": "সময়", "din": "দিন", "raat": "রাত", "shokal": "সকাল", "bikel": "বিকাল",
    "bhai": "ভাই", "bon": "বোন", "maa": "মা", "baba": "বাবা",
    "bondhu": "বন্ধু", "prem": "প্রেম", "bhalobashi": "ভালোবাসি",
    "dhonnobad": "ধন্যবাদ", "shubho": "শুভ", "khobor": "খবর", "mon": "মন",
    "kotha": "কথা", "jhamela": "ঝামেলা"
}

_WORD_PATTERN = re.compile(r"[A-Za-z]+")

def transliterate_romanized_to_bengali(text: str) -> str:
    """
    Replaces Romanized Bengali tokens with accurate Bengali script while
    preserving punctuation and unmapped English terms (e.g. 'meeting', 'zoom').
    """
    if not text:
        return ""
        
    def _replace_word(match: re.Match) -> str:
        word = match.group(0)
        lower_word = word.lower()
        if lower_word in ROMAN_TO_BN:
            return ROMAN_TO_BN[lower_word]
        return word

    return _WORD_PATTERN.sub(_replace_word, text)
