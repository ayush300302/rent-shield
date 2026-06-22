from backend.prompts import DAMAGE_EVALUATION_PROMPT
from backend.llm import run_llm_classification, get_heuristic_damage_evaluation


def evaluate_damage(before_description: str, after_description: str) -> dict:
    """
    Evaluate property damage by comparing before and after descriptions.
    Returns: {"damage_score": 0-9, "damage_category": str}
    Uses LLM scoring with heuristic fallback.
    """
    def fallback_eval():
        return get_heuristic_damage_evaluation(before_description, after_description)

    heuristics = fallback_eval()

    prompt = DAMAGE_EVALUATION_PROMPT.format(
        before_description=before_description,
        after_description=after_description,
        damage_default=heuristics["damage_score"],
        category_default=heuristics["damage_category"],
    )

    return run_llm_classification(prompt, fallback_eval)
