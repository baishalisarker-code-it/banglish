"""
BanglaBridge Unified Processing Pipeline
Coordinates chunking, language detection, transliteration, translation,
and affective sentiment & sarcasm analysis.
"""

from typing import Dict, Any, List
from .core.chunker import split_chunks
from .core.detector import detect_language
from .core.transliterator import transliterate_romanized_to_bengali
from .core.analyzer import analyze_emotion_and_sarcasm
from .core.translator import translate, is_nllb_available

def full_pipeline(text: str, direction: str = "auto") -> Dict[str, Any]:
    """
    Processes user text through the complete BanglaBridge pipeline.
    
    Args:
        text (str): Source input containing Bengali, Banglish, and/or English.
        direction (str): "auto" | "bn-en" | "en-bn"
        
    Returns:
        Dict[str, Any]: Comprehensive analysis and translation payload.
    """
    clean_text = (text or "").strip()
    if not clean_text:
        return {
            "success": True,
            "full_translation": "",
            "chunks": [],
            "summary": {
                "total_chunks": 0,
                "overall_emotion": "Neutral",
                "has_sarcasm": False,
                "sarcasm_status": "No",
                "scripts_detected": [],
                "engine": "Idle"
            }
        }
        
    chunks = split_chunks(clean_text)
    chunk_results: List[Dict[str, Any]] = []
    translated_pieces: List[str] = []
    
    detected_scripts = set()
    emotion_counts: Dict[str, int] = {}
    any_sarcasm_yes = False
    any_sarcasm_possible = False
    all_notes = set()
    engine_used = "BanglaBridge Engine"

    for idx, chunk in enumerate(chunks, 1):
        lang_info = detect_language(chunk)
        detected_scripts.add(lang_info["script"])
        
        # Decide translation path based on direction and detected language
        is_source_bengali = (lang_info["lang"] == "bn") or (direction == "bn-en")
        if direction == "en-bn":
            is_source_bengali = False
            
        transliterated = chunk
        if is_source_bengali:
            # If Romanized Banglish or Mixed, transliterate first
            if lang_info["script"] in ("Romanized", "Mixed"):
                transliterated = transliterate_romanized_to_bengali(chunk)
                
            trans_result, engine = translate(transliterated, src_lang="ben_Beng", tgt_lang="eng_Latn")
            engine_used = engine
        else:
            trans_result, engine = translate(chunk, src_lang="eng_Latn", tgt_lang="ben_Beng")
            engine_used = engine

        # Analyze emotion, sarcasm, and cultural nuance
        analysis = analyze_emotion_and_sarcasm(chunk, trans_result)
        
        # Track statistics
        emotion = analysis["emotion"]
        emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
        
        if analysis["sarcasm"] == "Yes":
            any_sarcasm_yes = True
        elif analysis["sarcasm"] == "Possible":
            any_sarcasm_possible = True
            
        for n in analysis["notes"]:
            all_notes.add(n)
            
        translated_pieces.append(trans_result)
        
        chunk_results.append({
            "chunk_id": idx,
            "original": chunk,
            "script": lang_info["script"],
            "language_note": lang_info["note"],
            "transliterated": transliterated if transliterated != chunk else None,
            "translation": trans_result,
            "emotion": emotion,
            "polarity": analysis["polarity"],
            "sarcasm": analysis["sarcasm"],
            "sarcasm_flag": analysis["sarcasm_flag"],
            "confidence": analysis["confidence"],
            "notes": analysis["notes"]
        })
        
    # Global summary calculation
    dominant_emotion = "Neutral"
    if emotion_counts:
        dominant_emotion = max(emotion_counts, key=emotion_counts.get)
        
    sarcasm_status = "Yes" if any_sarcasm_yes else ("Possible" if any_sarcasm_possible else "No")
    
    return {
        "success": True,
        "input_text": clean_text,
        "full_translation": " ".join(translated_pieces),
        "chunks": chunk_results,
        "summary": {
            "total_chunks": len(chunk_results),
            "dominant_emotion": dominant_emotion,
            "has_sarcasm": any_sarcasm_yes or any_sarcasm_possible,
            "sarcasm_status": sarcasm_status,
            "scripts_detected": sorted(list(detected_scripts)),
            "all_notes": sorted(list(all_notes)),
            "engine": engine_used,
            "nllb_available": is_nllb_available()
        }
    }
