import sys
import os
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.damage_evaluation import evaluate_damage

def run_evaluations():
    test_cases = [
        {
            "name": "No damage (perfect condition)",
            "before": "Clean white walls, polished wooden floor, new kitchen cabinets, working AC.",
            "after": "Clean white walls, polished wooden floor, new kitchen cabinets, working AC. No damage visible.",
            "expected_score": 0,
        },
        {
            "name": "Minimal damage (light wear)",
            "before": "Freshly painted walls, new carpet, clean bathroom tiles.",
            "after": "Walls have minor wear and light scratch marks, carpet shows normal wear from daily use.",
            "expected_score": 2,
        },
        {
            "name": "Moderate damage (stains and scratches)",
            "before": "White walls, wooden floor, glass window intact.",
            "after": "Walls have stain marks from cooking, wooden floor has scratched floor areas, peeling paint near bathroom.",
            "expected_score": 4,
        },
        {
            "name": "Significant damage (broken fixtures)",
            "before": "All doors working, windows intact, plumbing functional.",
            "after": "Broken door in bedroom, large hole in living room wall, damaged plumbing in kitchen causing leaks.",
            "expected_score": 6,
        },
        {
            "name": "Severe damage (structural issues)",
            "before": "Solid structure, dry walls, clean ceiling.",
            "after": "Mold growth on walls and ceiling, water damage in bathroom, flood marks on floor.",
            "expected_score": 8,
        },
    ]

    print("=" * 60)
    print("RENTSHIELD - DAMAGE EVALUATION")
    print("=" * 60)

    passed = 0
    total = len(test_cases)

    for case in test_cases:
        print(f"\nTest: {case['name']}")
        try:
            result = evaluate_damage(case["before"], case["after"])
            actual = result.get("damage_score")
            expected = case["expected_score"]
            # Allow +/- 1 tolerance for heuristic
            tag = "[PASS]" if abs(actual - expected) <= 1 else "[WARN]"
            if abs(actual - expected) <= 1:
                passed += 1
            print(f"  Result: {json.dumps(result)}")
            print(f"  {tag} Score: {actual} (expected ~{expected})")
        except Exception as e:
            print(f"  [ERROR] {str(e)}")

    print(f"\n{'=' * 60}")
    print(f"RESULTS: {passed}/{total} damage tests passed (tolerance +/- 1)")
    print(f"{'=' * 60}")

if __name__ == "__main__":
    run_evaluations()
