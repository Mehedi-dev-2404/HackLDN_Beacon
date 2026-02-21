import re
from typing import List


def chunk_text(
    text: str,
    max_chunk_size: int = 1000,
    overlap: int = 100
) -> List[str]:
    """
    Split large text into overlapping chunks for processing.
    Useful for long documents like lecture notes or assignments.
    
    Args:
        text: Input text to chunk
        max_chunk_size: Maximum characters per chunk
        overlap: Number of characters to overlap between chunks
        
    Returns:
        List of text chunks
    """
    if len(text) <= max_chunk_size:
        return [text]
    
    chunks = []
    start = 0
    
    while start < len(text):
        end = start + max_chunk_size
        
        # Try to break at sentence boundary
        if end < len(text):
            # Look for sentence ending
            sentence_break = text.rfind('.', start, end)
            if sentence_break != -1 and sentence_break > start + max_chunk_size // 2:
                end = sentence_break + 1
        
        chunks.append(text[start:end].strip())
        start = end - overlap
    
    return chunks


def chunk_by_sentences(text: str, sentences_per_chunk: int = 5) -> List[str]:
    """
    Split text into chunks containing a fixed number of sentences.
    Better for maintaining semantic coherence.
    
    Args:
        text: Input text
        sentences_per_chunk: Number of sentences per chunk
        
    Returns:
        List of text chunks
    """
    # Split into sentences using regex
    sentence_pattern = r'(?<=[.!?])\s+'
    sentences = re.split(sentence_pattern, text)
    
    chunks = []
    for i in range(0, len(sentences), sentences_per_chunk):
        chunk = ' '.join(sentences[i:i + sentences_per_chunk])
        chunks.append(chunk.strip())
    
    return chunks


def chunk_by_paragraphs(text: str, max_paragraphs: int = 3) -> List[str]:
    """
    Split text by paragraphs (useful for essays and reports).
    
    Args:
        text: Input text
        max_paragraphs: Maximum paragraphs per chunk
        
    Returns:
        List of text chunks
    """
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
    
    chunks = []
    for i in range(0, len(paragraphs), max_paragraphs):
        chunk = '\n\n'.join(paragraphs[i:i + max_paragraphs])
        chunks.append(chunk)
    
    return chunks
