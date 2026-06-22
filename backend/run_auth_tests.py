"""Test auth endpoints against the running RentShield API."""
import urllib.request
import urllib.error
import json
import sys
import os

BASE = os.getenv("API_BASE", "http://127.0.0.1:8000")

def post_json(path, data):
    """Send a JSON POST request."""
    body = json.dumps(data).encode("utf-8")
    req = urllib.request.Request(
        f"{BASE}{path}",
        data=body,
        headers={"Content-Type": "application/json"},
    )
    try:
        r = urllib.request.urlopen(req)
        return r.status, json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode())


def run_tests():
    print("=" * 60)
    print("RENTSHIELD - AUTH ENDPOINT TESTS")
    print("=" * 60)

    passed = 0
    total = 0

    # Test 1: Signup
    print("\n--- Test 1: POST /auth/signup ---")
    total += 1
    status, body = post_json("/auth/signup", {
        "role": "renter",
        "name": "Ayush Patil",
        "phone": "9876543210",
        "email": "ayush@test.com",
        "password": "securepass123"
    })
    if status == 200 and body.get("status") == "success":
        passed += 1
        print(f"  [PASS] Signup successful: {body.get('user_id')}")
    else:
        print(f"  [FAIL] Status: {status}, Body: {json.dumps(body)}")

    # Test 2: Duplicate signup
    print("\n--- Test 2: Duplicate Signup (should fail) ---")
    total += 1
    status, body = post_json("/auth/signup", {
        "role": "renter",
        "name": "Ayush Patil",
        "phone": "9876543210",
        "email": "ayush@test.com",
        "password": "securepass123"
    })
    if status == 409:
        passed += 1
        print(f"  [PASS] Correctly rejected: {body.get('detail')}")
    else:
        print(f"  [FAIL] Status: {status}, Body: {json.dumps(body)}")

    # Test 3: Login with correct credentials
    print("\n--- Test 3: POST /auth/login (correct password) ---")
    total += 1
    status, body = post_json("/auth/login", {
        "email": "ayush@test.com",
        "password": "securepass123"
    })
    if status == 200 and body.get("access_token"):
        passed += 1
        token = body["access_token"][:30] + "..."
        print(f"  [PASS] Login successful, token: {token}")
    else:
        print(f"  [FAIL] Status: {status}, Body: {json.dumps(body)}")

    # Test 4: Login with wrong password
    print("\n--- Test 4: POST /auth/login (wrong password) ---")
    total += 1
    status, body = post_json("/auth/login", {
        "email": "ayush@test.com",
        "password": "wrongpassword"
    })
    if status == 401:
        passed += 1
        print(f"  [PASS] Correctly rejected: {body.get('detail')}")
    else:
        print(f"  [FAIL] Status: {status}, Body: {json.dumps(body)}")

    # Test 5: Login with non-existent user
    print("\n--- Test 5: POST /auth/login (non-existent user) ---")
    total += 1
    status, body = post_json("/auth/login", {
        "email": "nobody@test.com",
        "password": "whatever"
    })
    if status == 401:
        passed += 1
        print(f"  [PASS] Correctly rejected: {body.get('detail')}")
    else:
        print(f"  [FAIL] Status: {status}, Body: {json.dumps(body)}")

    # Summary
    print(f"\n{'=' * 60}")
    print(f"RESULTS: {passed}/{total} auth tests passed")
    print(f"{'=' * 60}")

    return passed == total

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
