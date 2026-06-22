import sys
import os
import json

# Setup import path for backend
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.offer_letter_evaluation import evaluate_offer_letter

def run_evaluations():
    # Define three typical offer letter texts
    test_cases = [
        {
            "id": "Case A (High Tier / Google)",
            "text": """
            Google India Private Limited
            Signature Towers, Gurugram, India
            
            Dear Candidate,
            We are pleased to offer you employment at Google India as a Software Engineer.
            Your annual base salary (CTC) will be INR 15,00,000 (15 LPA), paid monthly.
            You will also be eligible for stock grants and performance bonuses.
            """
        },
        {
            "id": "Case B (Mid Tier / MidStart)",
            "text": """
            MidStart Technologies Private Limited
            Indiranagar, Bengaluru
            
            Subject: Offer of Employment
            
            Dear Candidate,
            We are delighted to offer you the position of Senior QA Engineer at MidStart Technologies. 
            We are a growing mid-sized software company with 150 employees.
            Your total annual compensation will be 6.5 LPA (Six Lakh Fifty Thousand Rupees per annum).
            """
        },
        {
            "id": "Case C (Low Tier / Small Startup)",
            "text": """
            QuickClean Local Services
            Mumbai, India
            
            Letter of Appointment
            
            We are pleased to offer you the position of Office Assistant.
            Your monthly salary will be INR 25,000 (equivalent to 3 Lakhs Per Annum).
            This is a full-time contract role.
            """
        }
    ]

    print("==================================================")
    print("RENTSHIELD - OFFER LETTER EVALUATIONS            ")
    print("==================================================")
    
    for case in test_cases:
        print(f"\nTesting {case['id']}:")
        print("    Offer Text Snippet:")
        # Print a clean summary of input text
        clean_text = " ".join(case["text"].strip().split())
        print(f"      \"{clean_text[:140]}...\"")
        
        try:
            result = evaluate_offer_letter(case["text"])
            print(f"    Result JSON: {json.dumps(result)}")
            
            comp_tier = result.get("company_tier")
            sal_tier = result.get("salary_tier")
            
            print(f"    Interpretation:")
            print(f"      - Company Tier: {comp_tier} "
                  f"({'Tier 1 (MAANG/Multinational)' if comp_tier == 1 else 'Tier 2 (Mid-sized)' if comp_tier == 2 else 'Tier 3 (Small/Local)'})")
            print(f"      - Salary Tier: {sal_tier} "
                  f"({'Tier 1 (>10 LPA)' if sal_tier == 1 else 'Tier 2 (4-10 LPA)' if sal_tier == 2 else 'Tier 3 (<4 LPA)'})")
        except Exception as e:
            print(f"    Error executing case: {str(e)}")
            
    print("\n==================================================")
    print("EVALUATIONS COMPLETED")
    print("==================================================")

if __name__ == "__main__":
    run_evaluations()
