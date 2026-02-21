import os
import sys
import re

# Add backend directory to path for config imports
backend_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'backend')
sys.path.insert(0, backend_path)

from config import gemini_model


def check_academic_integrity(student_query: str) -> dict:
    """
    Assess whether a student query is attempting to bypass academic integrity.
    UK Russell Group compliant detection.
    
    Args:
        student_query: The student's question or request
        
    Returns:
        Dictionary with 'is_acceptable' (bool) and 'reason' (str)
    """
    # Pattern-based pre-screening
    red_flags = [
        r'\b(write|complete|do|solve) (my|this|the) (assignment|essay|coursework|homework)\b',
        r'\b(give|provide|show) (me )?(the )?(answer|solution|code)\b',
        r'\bwrite.*for me\b',
        r'\bcomplete.*assignment\b',
        r'\bgive.*full (code|essay|solution)\b'
    ]
    
    for pattern in red_flags:
        if re.search(pattern, student_query, re.IGNORECASE):
            return {
                "is_acceptable": False,
                "reason": "Request appears to seek direct assignment completion",
                "severity": "high"
            }
    
    # AI-based assessment for subtle cases
    integrity_check = _ai_integrity_assessment(student_query)
    
    return integrity_check


def _ai_integrity_assessment(query: str) -> dict:
    """
    Use Gemini to assess academic integrity of nuanced queries.
    
    Args:
        query: Student's query
        
    Returns:
        Assessment dictionary
    """
    prompt = f"""You are an academic integrity officer at a UK Russell Group university.

Assess if this student query violates academic integrity policies.

Query: "{query}"

Determine:
1. Is the student asking for direct assignment completion?
2. Or are they seeking legitimate learning support?

Legitimate: concept explanations, debugging guidance, methodology questions
Violation: requests for complete solutions, essay writing, direct answers

Respond with ONLY:
ACCEPTABLE - if legitimate learning request
VIOLATION - if seeking direct completion

Classification:"""

    try:
        response = gemini_model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.1,
                "top_p": 0.9,
            }
        )
        
        result = response.text.strip().upper()
        
        if "VIOLATION" in result:
            return {
                "is_acceptable": False,
                "reason": "AI detected potential academic integrity violation",
                "severity": "medium"
            }
        else:
            return {
                "is_acceptable": True,
                "reason": "Query is a legitimate learning request",
                "severity": "none"
            }
    
    except Exception:
        # Fail open for edge cases, but log
        return {
            "is_acceptable": True,
            "reason": "Could not assess - defaulting to acceptable",
            "severity": "unknown"
        }


def is_request_appropriate(query: str) -> bool:
    """
    Quick boolean check for academic integrity.
    
    Args:
        query: Student query
        
    Returns:
        True if appropriate, False if violates policy
    """
    result = check_academic_integrity(query)
    return result["is_acceptable"]
