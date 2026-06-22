from backend.prompts import COLLEGE_EVALUATION_PROMPT
from backend.llm import run_llm_classification, get_heuristic_college_evaluation

def evaluate_college(college_name: str) -> dict:
    """
    Evaluate a college/university name and classify it into Tier 1, 2, or 3.
    Uses LLM scoring and falls back to keyword-based heuristic if no API key.
    Returns: {"college_tier": 1 | 2 | 3}
    """
    def fallback_eval():
        return get_heuristic_college_evaluation(college_name)

    heuristics = fallback_eval()

    prompt = COLLEGE_EVALUATION_PROMPT.format(
        college_name=college_name,
        college_default=heuristics["college_tier"]
    )

    return run_llm_classification(prompt, fallback_eval)
