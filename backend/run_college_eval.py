import sys
import os
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.college_evaluation import evaluate_college

def run_evaluations():
    test_cases = [
        {"college": "IIT Bombay", "expected_tier": 1},
        {"college": "IIM Ahmedabad", "expected_tier": 1},
        {"college": "VIT University, Vellore", "expected_tier": 2},
        {"college": "Symbiosis Institute of Technology, Pune", "expected_tier": 2},
        {"college": "Shri Ram College of Unknown Sciences, Aurangabad", "expected_tier": 3},
        {"college": "Harvard University", "expected_tier": 1},
        {"college": "Local Municipal College, Latur", "expected_tier": 3},
    ]

    print("==================================================")
    print("RENTSHIELD - COLLEGE EVALUATION (ITEM 4)         ")
    print("==================================================")

    for case in test_cases:
        college = case["college"]
        expected = case["expected_tier"]
        print(f"\nTesting: {college}")
        print(f"  Expected Tier: {expected}")
        try:
            result = evaluate_college(college)
            tier = result.get("college_tier")
            match = "[PASS]" if tier == expected else "[WARN]"
            print(f"  Result JSON: {json.dumps(result)}")
            label = "Tier 1 (Top/IIT/IIM/Global)" if tier == 1 else "Tier 2 (Mid/Private Univ.)" if tier == 2 else "Tier 3 (Unknown/Local)"
            print(f"  {match} Classified as: {label}")
        except Exception as e:
            print(f"  Error: {str(e)}")

    print("\n==================================================")
    print("EVALUATIONS COMPLETED")
    print("==================================================")

if __name__ == "__main__":
    run_evaluations()
