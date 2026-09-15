"""
Emotion, Sarcasm, and Cultural Sentiment Analyzer
Analyzes Bengali and English texts for affective tone, polarity,
deadpan sarcasm, irony markers, and cultural slang expressions.
"""

import re
from typing import Dict, Any, List

POS_EN = {
    "good", "great", "excellent", "amazing", "wonderful", "beautiful", "love",
    "happy", "glad", "nice", "well", "perfect", "best", "awesome", "bravo",
    "fine", "ok", "okay", "pleasure", "joy", "fantastic", "brilliant", "superb"
}

NEG_EN = {
    "bad", "terrible", "awful", "hate", "sad", "angry", "useless", "worst",
    "not", "never", "no", "poor", "fail", "failed", "rubbish", "trash",
    "pathetic", "horrible", "disappointed", "ugly", "pain", "annoying",
    "disaster", "ruined", "waste", "crazy", "stupid", "idiot"
}

POS_BN = {
    "ভালো", "সুন্দর", "দারুণ", "বাহ", "চমৎকার", "অসাধারণ", "ধন্যবাদ",
    "আনন্দ", "খুশি", "সুখী", "ভালোবাসি", "লাভ", "স্নেহ", "মিষ্টি", "সেরা"
}

NEG_BN = {
    "খারাপ", "ফালতু", "বাজে", "না", "নাই", "নেই", "ঘৃণা", "রাগ", "দুঃখ",
    "ব্যর্থ", "কষ্ট", "অপদার্থ", "ভয়", "আতঙ্ক", "অসন্তুষ্ট", "ঝামেলা", "পাগল"
}

SARCASM_MARKERS_BN = ("বাহ", "আহা", "দারুণ", "অসাধারণ", "খুব ভালো", "সুন্দর")
SARCASM_MARKERS_EN = ("wow", "great job", "yeah right", "bravo", "oh great", "surely")

# Bengali cultural expressions & slang mappings
CULTURAL_SLANG = {
    "ফালতু": "Bengali slang: 'ফালতু' (meaning useless, worthless, or rubbish)",
    "faltu": "Banglish slang: 'faltu' (meaning useless, worthless, or rubbish)",
    "ঝামেলা": "Bengali idiom: 'ঝামেলা' (denoting headache, trouble, or hassle)",
    "jhamela": "Banglish idiom: 'jhamela' (denoting trouble or hassle)",
    "বাজে": "Bengali colloquialism: 'বাজে' (meaning bad quality or inappropriate)",
    "baje": "Banglish colloquialism: 'baje' (meaning bad quality)",
    "অপদার্থ": "Bengali critique: 'অপদার্থ' (referring to someone or something totally inept)",
    "মাথা নষ্ট": "Bengali expression: 'মাথা নষ্ট' (mind-blowing or utterly baffling)",
    "matha nosto": "Banglish expression: 'matha nosto' (mind-blowing or crazy)"
}

def _extract_tokens(s: str) -> List[str]:
    return re.findall(r"[A-Za-z']+|[\u0980-\u09FF]+", (s or "").lower())

def analyze_emotion_and_sarcasm(original: str, translated: str = "") -> Dict[str, Any]:
    """
    Evaluates polarity, emotion state, sarcasm probability, and cultural nuances.
    
    Args:
        original (str): The original source sentence (Bengali or Banglish).
        translated (str): The translated sentence (English or Bengali).
        
    Returns:
        dict: {
            "emotion": "Positive" | "Negative" | "Neutral" | "Mixed" | "Joy/Happiness" | "Sadness" | "Anger" | "Fear",
            "sarcasm": "Yes" | "Possible" | "No",
            "sarcasm_flag": bool,
            "confidence": float,
            "notes": List[str],
            "sentiment_score": float
        }
    """
    orig_text = original or ""
    trans_text = translated or ""
    
    orig_tokens = _extract_tokens(orig_text)
    trans_tokens = _extract_tokens(trans_text)
    
    pos_count = sum(1 for w in trans_tokens if w in POS_EN) + sum(1 for w in orig_tokens if w in POS_BN)
    neg_count = sum(1 for w in trans_tokens if w in NEG_EN) + sum(1 for w in orig_tokens if w in NEG_BN)
    
    # Negation handling in English / Bengali
    if re.search(r"\b(not|never|no|don't|dont|isn't|isnt|cannot|can't)\b", trans_text.lower()):
        if pos_count and not neg_count:
            neg_count += 1
            pos_count = max(0, pos_count - 1)
            
    # Base polarity determination
    if pos_count > neg_count and pos_count >= 1:
        polarity = "Positive"
        sentiment_score = 0.8
    elif neg_count > pos_count and neg_count >= 1:
        polarity = "Negative"
        sentiment_score = -0.8
    elif pos_count == 0 and neg_count == 0:
        polarity = "Neutral"
        sentiment_score = 0.0
    else:
        polarity = "Mixed"
        sentiment_score = 0.1
        
    # Granular emotion classification
    orig_lower = orig_text.lower()
    trans_lower = trans_text.lower()
    
    if any(w in orig_lower for w in ["খুশি", "আনন্দ", "joy", "happy", "great", "cheer"]):
        emotion = "Joy / Happiness"
    elif any(w in orig_lower for w in ["দুঃখ", "কষ্ট", "sad", "crying", "unhappy"]):
        emotion = "Sadness"
    elif any(w in orig_lower for w in ["রাগ", "অসন্তুষ্ট", "angry", "furious", "hate"]):
        emotion = "Anger"
    elif any(w in orig_lower for w in ["ভয়", "আতঙ্ক", "fear", "scared", "afraid"]):
        emotion = "Fear"
    else:
        emotion = polarity

    # Sarcasm & Irony Assessment
    notes = []
    sarcasm = "No"
    sarcasm_flag = False
    
    has_bn_marker = any(m in orig_text for m in SARCASM_MARKERS_BN)
    has_en_marker = any(m in trans_lower for m in SARCASM_MARKERS_EN)
    has_praise_marker = has_bn_marker or has_en_marker
    
    contrast_marker = ("কিন্তু" in orig_text) or ("kintu" in orig_lower) or ("but" in trans_lower)
    
    # Check 1: Praise marker combined with negative context (Classic Sarcasm)
    if has_praise_marker and (polarity in {"Negative", "Mixed"} or neg_count >= 1):
        sarcasm = "Yes"
        sarcasm_flag = True
        notes.append("Praise marker (বাহ/দারুণ/wow) coupled with negative intent indicates irony/sarcasm.")
        
    # Check 2: Contrast pattern (কন্টেন্ট বৈপরীত্য)
    elif contrast_marker and pos_count >= 1 and neg_count >= 1:
        sarcasm = "Possible"
        sarcasm_flag = True
        notes.append("Contrast pattern ('কিন্তু' / 'but') with shifting polarity suggests nuanced irony.")
        
    # Check 3: Deadpan / Positive wording over negative Bengali cue
    elif polarity == "Positive" and any(w in orig_text for w in NEG_BN):
        sarcasm = "Possible"
        sarcasm_flag = True
        notes.append("Superficially positive wording masking underlying critical sentiment.")
        
    elif has_praise_marker and ("!" in orig_text or "!" in trans_text) and any(w in orig_tokens for w in ["ফালতু", "faltu", "বাজে", "baje"]):
        sarcasm = "Yes"
        sarcasm_flag = True
        notes.append("Sarcastic praise juxtaposed with derogatory expression.")

    # Cultural & Slang Notes
    for idiom, note_text in CULTURAL_SLANG.items():
        if idiom in orig_text or idiom in orig_lower:
            notes.append(note_text)
            
    return {
        "emotion": emotion,
        "polarity": polarity,
        "sarcasm": sarcasm,
        "sarcasm_flag": sarcasm_flag,
        "confidence": 0.88 if sarcasm == "Yes" else (0.75 if sarcasm == "Possible" else 0.95),
        "notes": notes,
        "sentiment_score": sentiment_score
    }
