"""RentShield FastAPI Backend Application."""

import os
import sys
import shutil
import tempfile
import logging
from typing import Optional

from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# Ensure backend package is importable
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.models import (
    DocumentType, SubmissionResponse, SignupRequest, LoginRequest,
    TokenResponse, PropertyClassifyRequest, DamageEvalRequest,
    QuestionnaireRequest,
)
from backend.offer_letter_evaluation import evaluate_offer_letter
from backend.college_evaluation import evaluate_college
from backend.bank_statement_evaluation import evaluate_bank_statement
from backend.home_owner.home_owner_evaluation import classify_property
from backend.damage_evaluation import evaluate_damage
from backend.auth import signup as auth_signup, login as auth_login
from backend.db import save_questionnaire_response

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="RentShield API",
    description="Backend API for RentShield — deposit insurance platform for India's rental market.",
    version="0.1.0",
)

# CORS — allow the frontend (localhost:5173 for Vite dev) to call us
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"status": "ok", "service": "RentShield API", "version": "0.1.0"}


@app.post("/auth/signup")
def signup_route(req: SignupRequest):
    """
    Register a new user.
    - **role**: 'renter' or 'owner'
    - **name**: Full name
    - **phone**: Phone number
    - **email**: Email address
    - **password**: Password (min 6 chars recommended)
    """
    try:
        result = auth_signup(
            role=req.role,
            name=req.name,
            phone=req.phone,
            email=req.email,
            password=req.password,
        )
        return {"status": "success", **result}
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))


@app.post("/auth/login", response_model=TokenResponse)
def login_route(req: LoginRequest):
    """
    Login with email and password. Returns JWT access and refresh tokens.
    """
    try:
        tokens = auth_login(email=req.email, password=req.password)
        return TokenResponse(**tokens)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))


@app.post("/classify-property")
def classify_property_route(req: PropertyClassifyRequest):
    """
    Classify a rental property based on location, rent, and deposit.
    Returns tier scores (1/2/3) for each dimension.
    """
    result = classify_property(
        location=req.location,
        rent=req.rent,
        deposit=req.deposit,
    )
    return {
        "status": "success",
        "evaluation": result,
        "message": f"Property classified: Location Tier {result.get('location')}, Rent Tier {result.get('rent')}, Deposit Tier {result.get('deposit_neededd')}.",
    }


@app.post("/evaluate-damage")
def evaluate_damage_route(req: DamageEvalRequest):
    """
    Evaluate property damage by comparing before and after descriptions.
    Returns a damage score (0-9) and category.
    """
    result = evaluate_damage(
        before_description=req.before_description,
        after_description=req.after_description,
    )
    return {
        "status": "success",
        "evaluation": result,
        "message": f"Damage score: {result.get('damage_score')}/9 ({result.get('damage_category')}).",
    }


@app.post("/questionnaire")
def submit_questionnaire(req: QuestionnaireRequest):
    """
    Submit questionnaire answers for storage and processing.
    - **user_type**: 'renter' or 'owner'
    - **answers**: dict of { question_id: answer_value }
    """
    import json
    answers_json = json.dumps(req.answers)
    row_id = save_questionnaire_response(
        user_email=None,  # Can be extracted from JWT token in future
        user_type=req.user_type,
        answers_json=answers_json,
    )
    return {
        "status": "success",
        "response_id": row_id,
        "message": f"Questionnaire submitted successfully ({len(req.answers)} answers recorded).",
    }


@app.post("/submit", response_model=SubmissionResponse)
async def submit_document(
    document_type: DocumentType = Form(...),
    college_name: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
):
    """
    Submit a document for evaluation.

    - **document_type**: `bank_account_statement` or `offer_letter`
    - **college_name**: (optional) college name string for college evaluation
    - **file**: PDF file upload (required for bank_account_statement and offer_letter)
    """

    # --- College name evaluation (no file needed) ---
    if college_name:
        result = evaluate_college(college_name)
        return SubmissionResponse(
            status="success",
            document_type="college_evaluation",
            college_name=college_name,
            evaluation=result,
            message=f"College '{college_name}' classified as Tier {result.get('college_tier')}.",
        )

    # --- File-based evaluations ---
    if file is None:
        raise HTTPException(
            status_code=400,
            detail="A PDF file is required for bank_account_statement and offer_letter document types.",
        )

    # Validate file type
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail=f"Only PDF files are accepted. Received: {file.filename}",
        )

    # Save uploaded file to a temp location
    tmp_dir = tempfile.mkdtemp()
    tmp_path = os.path.join(tmp_dir, file.filename)
    try:
        with open(tmp_path, "wb") as f:
            content = await file.read()
            f.write(content)

        if document_type == DocumentType.OFFER_LETTER:
            # Extract text from PDF (basic extraction)
            text = _extract_text_from_pdf(tmp_path)
            if not text.strip():
                raise HTTPException(
                    status_code=422,
                    detail="Could not extract text from the uploaded PDF. Ensure it is not image-only.",
                )
            result = evaluate_offer_letter(text)
            return SubmissionResponse(
                status="success",
                document_type=document_type.value,
                filename=file.filename,
                evaluation=result,
                message=f"Offer letter evaluated: Company Tier {result.get('company_tier')}, Salary Tier {result.get('salary_tier')}.",
            )

        elif document_type == DocumentType.BANK_ACCOUNT_STATEMENT:
            text = _extract_text_from_pdf(tmp_path)
            if not text.strip():
                raise HTTPException(
                    status_code=422,
                    detail="Could not extract text from the bank statement PDF. Ensure it is not image-only.",
                )
            result = evaluate_bank_statement(text)
            return SubmissionResponse(
                status="success",
                document_type=document_type.value,
                filename=file.filename,
                evaluation=result,
                message=f"Bank statement evaluated: Age Tier {result.get('account_age_tier')}, Frequency Tier {result.get('transaction_frequency_tier')}, Volume Tier {result.get('transaction_volume_tier')}.",
            )

    finally:
        # Clean up temp files
        shutil.rmtree(tmp_dir, ignore_errors=True)


def _extract_text_from_pdf(pdf_path: str) -> str:
    """Extract text from a PDF file using PyPDF2."""
    try:
        from PyPDF2 import PdfReader
        reader = PdfReader(pdf_path)
        text_parts = []
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text)
        return "\n".join(text_parts)
    except ImportError:
        logger.warning("PyPDF2 not installed. Install it with: pip install PyPDF2")
        return ""
    except Exception as e:
        logger.error(f"Failed to extract PDF text: {e}")
        return ""
