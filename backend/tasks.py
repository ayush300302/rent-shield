# Background tasks and workflow orchestration for RentShield evaluations

from backend.home_owner.home_owner_evaluation import classify_property

def evaluate_home_owner_property_task(location: str, rent: int, deposit: int) -> dict:
    """Task wrapper to classify property."""
    print(f"[Task] Running property classification for Location: {location}, Rent: {rent}, Deposit: {deposit}")
    result = classify_property(location, rent, deposit)
    print(f"[Task] Result: {result}")
    return result
