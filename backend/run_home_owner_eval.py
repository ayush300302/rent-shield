import sys
import os
import json

# Setup import path for backend
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.home_owner.home_owner_evaluation import classify_property

def run_evaluations():
    # Define 3 popular cities, 3 mid cities, and 3 actual villages
    test_cases = [
        # Popular Cities (Tier 1 Location)
        {"type": "Popular City", "location": "Mumbai", "rent": 65000, "deposit": 2},
        {"type": "Popular City", "location": "Bengaluru", "rent": 35000, "deposit": 6},
        {"type": "Popular City", "location": "Pune", "rent": 12000, "deposit": 1},
        
        # Mid Cities (Tier 2 Location)
        {"type": "Mid City", "location": "Meerut", "rent": 18000, "deposit": 2},
        {"type": "Mid City", "location": "Ghaziabad", "rent": 22000, "deposit": 3},
        {"type": "Mid City", "location": "Jaipur", "rent": 14000, "deposit": 1},
        
        # Villages (Tier 3 Location)
        {"type": "Village", "location": "Ralegan Siddhi", "rent": 6000, "deposit": 2},
        {"type": "Village", "location": "Mawlynnong", "rent": 8000, "deposit": 1},
        {"type": "Village", "location": "Hampi", "rent": 11000, "deposit": 4}
    ]

    print("==================================================")
    print("RENTSHIELD - PROPERTY CLASSIFICATION EVALUATIONS  ")
    print("==================================================")
    
    for idx, case in enumerate(test_cases, 1):
        print(f"\n[{idx}] Testing {case['type']} - {case['location']}:")
        print(f"    Input: Rent = INR {case['rent']:,}, Deposit = {case['deposit']} months")
        
        try:
            result = classify_property(case["location"], case["rent"], case["deposit"])
            print(f"    Result JSON: {json.dumps(result)}")
            
            # Print friendly explanations
            loc_tier = result.get("location")
            rent_tier = result.get("rent")
            dep_tier = result.get("deposit_neededd")
            
            print(f"    Interpretation:")
            print(f"      - Location: Tier {loc_tier} "
                  f"({'Metro/Popular' if loc_tier == 1 else 'Mid City' if loc_tier == 2 else 'Village/Town'})")
            print(f"      - Rent: Tier {rent_tier} "
                  f"({'>50k (High)' if rent_tier == 1 else '15k-50k (Medium)' if rent_tier == 2 else '<15k (Low)'})")
            print(f"      - Deposit: Tier {dep_tier} "
                  f"({'1 mo (Low Risk)' if dep_tier == 1 else '2-3 mo (Medium Risk)' if dep_tier == 2 else '>3 mo (High Risk)'})")
        except Exception as e:
            print(f"    Error executing case: {str(e)}")
            
    print("\n==================================================")
    print("EVALUATIONS COMPLETED")
    print("==================================================")

if __name__ == "__main__":
    run_evaluations()
