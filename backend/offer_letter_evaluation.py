from backend.prompts import OFFER_LETTER_EVALUATION_PROMPT
from backend.llm import run_llm_classification, get_heuristic_offer_letter_evaluation

def evaluate_offer_letter(text: str) -> dict:
    """
    Evaluate job offer letter text to classify company and salary tiers.
    Uses LLM scoring and falls back to programmatic evaluation if needed.
    """
    # Fallback function definition for the LLM runner
    def fallback_eval():
        return get_heuristic_offer_letter_evaluation(text)
        
    # Generate default heuristic answers to provide as helpful hints/defaults to the LLM
    heuristics = fallback_eval()
    
    # Format prompt template
    prompt = OFFER_LETTER_EVALUATION_PROMPT.format(
        text=text,
        company_default=heuristics["company_tier"],
        salary_default=heuristics["salary_tier"]
    )
    
    # Run classification
    return run_llm_classification(prompt, fallback_eval)
