# ============================================================
# RentShield API - cURL Test Commands (Item 6)
# ============================================================
# Prerequisites:
#   1. Start the server:
#      backend\venv\Scripts\python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000
#   2. Run these commands from the project root directory.
# ============================================================

# ----------------------------------------------------------
# TEST 1: Health Check (GET /)
# ----------------------------------------------------------
# curl -s http://127.0.0.1:8000/
#
# Expected Response:
# {"status":"ok","service":"RentShield API","version":"0.1.0"}


# ----------------------------------------------------------
# TEST 2: College Name Evaluation (POST /submit)
# ----------------------------------------------------------
# curl -s -X POST http://127.0.0.1:8000/submit \
#   -F "document_type=offer_letter" \
#   -F "college_name=IIT Bombay"
#
# Expected Response:
# {
#   "status": "success",
#   "document_type": "college_evaluation",
#   "college_name": "IIT Bombay",
#   "evaluation": {"college_tier": 1},
#   "message": "College 'IIT Bombay' classified as Tier 1."
# }


# ----------------------------------------------------------
# TEST 3: Offer Letter PDF (POST /submit)
# ----------------------------------------------------------
# curl -s -X POST http://127.0.0.1:8000/submit \
#   -F "document_type=offer_letter" \
#   -F "file=@path/to/offer_letter.pdf"
#
# Expected Response:
# {
#   "status": "success",
#   "document_type": "offer_letter",
#   "filename": "offer_letter.pdf",
#   "evaluation": {"company_tier": 1, "salary_tier": 1},
#   "message": "Offer letter evaluated: Company Tier 1, Salary Tier 1."
# }


# ----------------------------------------------------------
# TEST 4: Bank Account Statement PDF (POST /submit)
# ----------------------------------------------------------
# curl -s -X POST http://127.0.0.1:8000/submit \
#   -F "document_type=bank_account_statement" \
#   -F "file=@path/to/bank_statement.pdf"
#
# Expected Response:
# {
#   "status": "success",
#   "document_type": "bank_account_statement",
#   "filename": "bank_statement.pdf",
#   "evaluation": {"note": "Bank statement evaluation coming soon."},
#   "message": "Bank statement received..."
# }


# ----------------------------------------------------------
# TEST 5: Error - Missing file for document type
# ----------------------------------------------------------
# curl -s -X POST http://127.0.0.1:8000/submit \
#   -F "document_type=offer_letter"
#
# Expected Response (400):
# {"detail":"A PDF file is required for bank_account_statement and offer_letter document types."}


# ----------------------------------------------------------
# TEST 6: Error - Non-PDF file upload
# ----------------------------------------------------------
# curl -s -X POST http://127.0.0.1:8000/submit \
#   -F "document_type=offer_letter" \
#   -F "file=@path/to/image.jpg"
#
# Expected Response (400):
# {"detail":"Only PDF files are accepted. Received: image.jpg"}


# ----------------------------------------------------------
# TEST 7: API Documentation
# ----------------------------------------------------------
# Open in browser: http://127.0.0.1:8000/docs    (Swagger UI)
# Open in browser: http://127.0.0.1:8000/redoc   (ReDoc)
