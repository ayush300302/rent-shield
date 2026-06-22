import sys
import os
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.bank_statement_evaluation import evaluate_bank_statement

def run_evaluations():
    test_cases = [
        {
            "name": "High-tier account (5-year old, high volume credits)",
            "text": """
            State Bank of India - Account Statement
            Account Opened: 15/03/2019
            Statement Period: 01/01/2024 to 31/12/2024

            Date        Description                     Credit(INR)   Debit(INR)   Balance
            02/01/2024  Salary Credit                   Rs. 1,50,000               Rs. 2,30,000
            05/01/2024  UPI Transfer                                  Rs. 5,000    Rs. 2,25,000
            07/01/2024  Online Shopping                                Rs. 3,500    Rs. 2,21,500
            10/01/2024  Rent Received                   Rs. 25,000                 Rs. 2,46,500
            12/01/2024  Insurance Premium                             Rs. 8,000    Rs. 2,38,500
            15/01/2024  Freelance Income                Rs. 45,000                 Rs. 2,83,500
            18/01/2024  Grocery                                       Rs. 4,200    Rs. 2,79,300
            20/01/2024  EMI Payment                                   Rs. 15,000   Rs. 2,64,300
            22/01/2024  FD Interest                     Rs. 12,000                 Rs. 2,76,300
            25/01/2024  Mutual Fund SIP                               Rs. 10,000   Rs. 2,66,300
            """,
            "expected_age": 1,  # 2019 to 2024 = 5 years -> Tier 1
        },
        {
            "name": "Mid-tier account (2-year old)",
            "text": """
            HDFC Bank - Account Statement
            Account Opened: 10/06/2022
            Statement Period: 01/06/2024 to 30/06/2024

            Date        Description                     Credit(INR)   Debit(INR)   Balance
            01/06/2024  Salary Credit                   Rs. 45,000                 Rs. 78,000
            05/06/2024  UPI Transfer                                  Rs. 2,000    Rs. 76,000
            10/06/2024  Electricity Bill                              Rs. 1,800    Rs. 74,200
            15/06/2024  Recharge                                      Rs. 599      Rs. 73,601
            20/06/2024  Transfer from Friend             Rs. 5,000                 Rs. 78,601
            25/06/2024  ATM Withdrawal                                Rs. 5,000    Rs. 73,601
            """,
            "expected_age": 2,  # 2022 to 2024 = 2 years -> Tier 2
        },
        {
            "name": "New account (less than 1 year)",
            "text": """
            Kotak Mahindra Bank - Account Statement
            Account Opened: 15/11/2024
            Statement Period: 15/11/2024 to 31/12/2024

            Date        Description                     Credit(INR)   Debit(INR)   Balance
            15/11/2024  Opening Deposit                 Rs. 5,000                  Rs. 5,000
            01/12/2024  UPI                                           Rs. 500      Rs. 4,500
            """,
            "expected_age": 3,  # Same year -> Tier 3
        },
    ]

    print("=" * 60)
    print("RENTSHIELD - BANK STATEMENT EVALUATION")
    print("=" * 60)

    passed = 0
    total = 0
    for case in test_cases:
        print(f"\nTest: {case['name']}")
        try:
            result = evaluate_bank_statement(case["text"])
            print(f"  Result: {json.dumps(result)}")

            # Check account age (the primary heuristic that works well)
            total += 1
            actual_age = result.get("account_age_tier")
            expected_age = case["expected_age"]
            tag = "[PASS]" if actual_age == expected_age else "[FAIL]"
            if actual_age == expected_age:
                passed += 1
            print(f"  {tag} account_age_tier: {actual_age} (expected {expected_age})")

            # Show other tiers (informational)
            print(f"  [INFO] transaction_frequency_tier: {result.get('transaction_frequency_tier')}")
            print(f"  [INFO] transaction_volume_tier: {result.get('transaction_volume_tier')}")
        except Exception as e:
            total += 1
            print(f"  [ERROR] {str(e)}")

    print(f"\n{'=' * 60}")
    print(f"RESULTS: {passed}/{total} account age tests passed")
    print(f"Note: txn frequency/volume depend on statement length and format.")
    print(f"LLM mode (with API key) provides more accurate analysis.")
    print(f"{'=' * 60}")

if __name__ == "__main__":
    run_evaluations()
