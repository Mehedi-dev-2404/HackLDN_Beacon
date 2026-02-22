import os
import sys

# Add backend directory to path for config imports
backend_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'backend')
sys.path.insert(0, backend_path)

from config import generate_content


def socratic_viva(topic: str, previous_answer: str = None) -> str:
    """
    Generate Socratic questions using UK academic methodology.
    
    Args:
        topic: The subject matter for questioning
        previous_answer: Optional student's previous response
        
    Returns:
        A thoughtfully crafted Socratic question
    """
    # Construct path to prompt file
    prompts_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'prompts')
    prompt_path = os.path.join(prompts_dir, 'socratic_viva.txt')
    
    with open(prompt_path, 'r', encoding='utf-8') as f:
        base_prompt = f.read()

    # Inject variables into prompt
    prompt = base_prompt.format(
        topic=topic,
        previous_answer=previous_answer or "No prior response."
    )

    # Generate with low temperature for consistency
    return generate_content(prompt, temperature=0.4, top_p=0.8, top_k=40)