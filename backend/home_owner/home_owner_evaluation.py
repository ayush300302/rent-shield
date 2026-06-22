from backend.prompts import PROPERTY_CLASSIFICATION_PROMPT
from backend.llm import run_llm_classification, get_heuristic_property_classification

def classify_property(location: str, rent: int, deposit: int) -> dict:
    """
    Classify a homeowner's property location, rent, and deposit requirements.
    Uses LLM scoring and falls back to programmatic evaluation if needed.
    """
    # Fallback function definition for the LLM runner
    def fallback_eval():
        return get_heuristic_property_classification(location, rent, deposit)
        
    # Generate default heuristic answers to provide as helpful hints/defaults to the LLM
    heuristics = fallback_eval()
    
    # Format prompt template
    prompt = PROPERTY_CLASSIFICATION_PROMPT.format(
        location=location,
        rent=rent,
        deposit=deposit,
        location_default=heuristics["location"],
        rent_default=heuristics["rent"],
        deposit_default=heuristics["deposit_neededd"]
    )
    
    # Run classification
    return run_llm_classification(prompt, fallback_eval)
