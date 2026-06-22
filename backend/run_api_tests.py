"""
RentShield API Integration Tests (Item 6)
Tests all /submit endpoint scenarios against the running FastAPI server.
"""
import urllib.request
import urllib.error
import json
import sys

BASE = "http://127.0.0.1:8000"

def post_form(path, fields):
    """Send a multipart/form-data POST request."""
    boundary = "----RentShieldTestBoundary"
    body = b""
    for name, value in fields.items():
        body += f"------RentShieldTestBoundary\r\n".encode()
        body += f'Content-Disposition: form-data; name="{name}"\r\n\r\n'.encode()
        body += f"{value}\r\n".encode()
    body += b"------RentShieldTestBoundary--\r\n"

    req = urllib.request.Request(
        f"{BASE}{path}",
        data=body,
        headers={"Content-Type": f"multipart/form-data; boundary=----RentShieldTestBoundary"},
    )
    try:
        r = urllib.request.urlopen(req)
        return r.status, json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode())


def test(name, status, body, expected_status, check_fn=None):
    """Validate a test result."""
    ok = status == expected_status
    if check_fn and ok:
        ok = check_fn(body)
    tag = "[PASS]" if ok else "[FAIL]"
    print(f"  {tag} {name}")
    print(f"        Status: {status} (expected {expected_status})")
    if not ok:
        print(f"        Body: {json.dumps(body, indent=2)}")
    return ok


def run_all():
    print("=" * 60)
    print("RENTSHIELD API INTEGRATION TESTS (Item 6)")
    print("=" * 60)
    passed = 0
    total = 0

    # Test 1: Health Check
    print("\n--- Test 1: GET / Health Check ---")
    total += 1
    try:
        r = urllib.request.urlopen(f"{BASE}/")
        status = r.status
        body = json.loads(r.read().decode())
    except Exception as e:
        print(f"  [FAIL] Server not reachable: {e}")
        print("  Make sure the server is running on port 8000.")
        sys.exit(1)
    if test("Health check returns ok", status, body, 200,
            lambda b: b.get("status") == "ok" and b.get("service") == "RentShield API"):
        passed += 1

    # Test 2: College Evaluation - Tier 1
    print("\n--- Test 2: College Evaluation (Tier 1) ---")
    total += 1
    s, b = post_form("/submit", {"document_type": "offer_letter", "college_name": "IIT Bombay"})
    if test("IIT Bombay -> Tier 1", s, b, 200,
            lambda b: b.get("evaluation", {}).get("college_tier") == 1):
        passed += 1

    # Test 3: College Evaluation - Tier 2
    print("\n--- Test 3: College Evaluation (Tier 2) ---")
    total += 1
    s, b = post_form("/submit", {"document_type": "offer_letter", "college_name": "VIT Vellore"})
    if test("VIT Vellore -> Tier 2", s, b, 200,
            lambda b: b.get("evaluation", {}).get("college_tier") == 2):
        passed += 1

    # Test 4: College Evaluation - Tier 3
    print("\n--- Test 4: College Evaluation (Tier 3) ---")
    total += 1
    s, b = post_form("/submit", {"document_type": "offer_letter", "college_name": "Random Local College"})
    if test("Random Local College -> Tier 3", s, b, 200,
            lambda b: b.get("evaluation", {}).get("college_tier") == 3):
        passed += 1

    # Test 5: Missing file for offer_letter
    print("\n--- Test 5: Missing file (Error Case) ---")
    total += 1
    s, b = post_form("/submit", {"document_type": "offer_letter"})
    if test("No file -> 400 error", s, b, 400,
            lambda b: "required" in b.get("detail", "").lower()):
        passed += 1

    # Test 6: Bank statement placeholder
    print("\n--- Test 6: Bank Statement (no file -> error) ---")
    total += 1
    s, b = post_form("/submit", {"document_type": "bank_account_statement"})
    if test("Bank statement no file -> 400", s, b, 400):
        passed += 1

    # Summary
    print("\n" + "=" * 60)
    print(f"RESULTS: {passed}/{total} tests passed")
    print("=" * 60)

    return passed == total


if __name__ == "__main__":
    success = run_all()
    sys.exit(0 if success else 1)
