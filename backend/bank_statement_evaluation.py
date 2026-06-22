from backend.prompts import BANK_STATEMENT_EVALUATION_PROMPT
from backend.llm import run_llm_classification, get_heuristic_bank_evaluation


def evaluate_bank_statement(text: str) -> dict:
    """
    Evaluate bank statement text and score on three dimensions:
    - account_age_tier (1/2/3)
    - transaction_frequency_tier (1/2/3)
    - transaction_volume_tier (1/2/3)
    Uses LLM scoring with heuristic fallback.
    """
    def fallback_eval():
        return get_heuristic_bank_evaluation(text)

    heuristics = fallback_eval()

    prompt = BANK_STATEMENT_EVALUATION_PROMPT.format(
        text=text[:3000],  # Limit text length for LLM context window
        account_age_default=heuristics["account_age_tier"],
        txn_freq_default=heuristics["transaction_frequency_tier"],
        txn_vol_default=heuristics["transaction_volume_tier"],
    )

    return run_llm_classification(prompt, fallback_eval)
