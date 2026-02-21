"""
Aura Intelligence Modules
UK-focused AI educational components
"""

from .socratic_engine import socratic_viva
from .career_matcher import analyze_career_match
from .integrity_guard import check_academic_integrity, is_request_appropriate
from .chunker import chunk_text, chunk_by_sentences, chunk_by_paragraphs

__all__ = [
    'socratic_viva',
    'analyze_career_match',
    'check_academic_integrity',
    'is_request_appropriate',
    'chunk_text',
    'chunk_by_sentences',
    'chunk_by_paragraphs'
]
