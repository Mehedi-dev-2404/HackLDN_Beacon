import os
import sys
import json
import re

# Add backend directory to path for config imports
backend_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'backend')
sys.path.insert(0, backend_path)

from config import gemini_model


def analyze_career_match(job_text: str) -> dict:
    """
    Extract structured career requirements from UK job descriptions.
    
    Args:
        job_text: The job description text to analyze
        
    Returns:
        Dictionary with extracted skills, tools, and requirements
        
    Raises:
        ValueError: If JSON parsing fails or output is malformed
    """
    # Construct path to prompt file
    prompts_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'prompts')
    prompt_path = os.path.join(prompts_dir, 'career_analysis.txt')
    
    with open(prompt_path, 'r', encoding='utf-8') as f:
        base_prompt = f.read()

    # Inject job text into prompt
    prompt = base_prompt.format(job_text=job_text)

    # Generate with very low temperature for deterministic extraction
    response = gemini_model.generate_content(
        prompt,
        generation_config={
            "temperature": 0.2,
            "top_p": 0.9,
            "top_k": 20,
        }
    )

    raw_text = response.text.strip()
    
    # Safe JSON extraction with markdown fallback
    parsed_json = _extract_json_safely(raw_text)
    
    # Validate required fields
    _validate_career_schema(parsed_json)
    
    return parsed_json


def _extract_json_safely(text: str) -> dict:
    """
    Extract JSON from model output, handling markdown code blocks.
    
    Args:
        text: Raw model output
        
    Returns:
        Parsed JSON dictionary
        
    Raises:
        ValueError: If JSON cannot be parsed
    """
    # Try direct JSON parse first
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    
    # Check for markdown code blocks
    markdown_pattern = r'```(?:json)?\s*(\{.*?\})\s*```'
    match = re.search(markdown_pattern, text, re.DOTALL)
    
    if match:
        try:
            return json.loads(match.group(1))
        except json.JSONDecodeError:
            pass
    
    # Try extracting first JSON object
    json_pattern = r'\{.*\}'
    match = re.search(json_pattern, text, re.DOTALL)
    
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            pass
    
    raise ValueError(f"Could not extract valid JSON from model output: {text[:200]}")


def _validate_career_schema(data: dict) -> None:
    """
    Ensure the parsed JSON contains all required fields.
    
    Args:
        data: Parsed JSON dictionary
        
    Raises:
        ValueError: If required fields are missing or malformed
    """
    required_fields = {
        "technical_skills": list,
        "tools_technologies": list,
        "cognitive_skills": list,
        "behavioural_traits": list,
        "experience_level": str
    }
    
    for field, expected_type in required_fields.items():
        if field not in data:
            raise ValueError(f"Missing required field: {field}")
        
        if not isinstance(data[field], expected_type):
            raise ValueError(
                f"Field '{field}' must be {expected_type.__name__}, got {type(data[field]).__name__}"
            )
