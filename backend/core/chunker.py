"""
Smart Sentence Chunker
Splits text into coherent sentence chunks respecting Bengali danda (।), English periods (.),
exclamation marks (!), question marks (?), and newlines.
"""

import re
from typing import List

# Regular expression that splits on sentence terminators while preserving chunk semantics
_SPLIT_PATTERN = re.compile(r"(?<=[।!?\n])\s+|(?<=[.!?])\s+")

def split_chunks(text: str) -> List[str]:
    """
    Splits Bengali, Banglish, and English text into meaningful sentence chunks.
    
    Args:
        text (str): Input text containing one or multiple sentences.
        
    Returns:
        List[str]: Cleaned list of sentence chunks.
    """
    text = (text or "").strip()
    if not text:
        return []
    
    parts = _SPLIT_PATTERN.split(text)
    chunks = [p.strip() for p in parts if p and p.strip()]
    return chunks if chunks else [text]
