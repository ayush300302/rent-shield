"""Pydantic models and enums for RentShield backend."""

from enum import Enum
from pydantic import BaseModel
from typing import Optional


class DocumentType(str, Enum):
    """Supported document types for submission."""
    BANK_ACCOUNT_STATEMENT = "bank_account_statement"
    OFFER_LETTER = "offer_letter"


class SubmissionRequest(BaseModel):
    """Request model for the /submit endpoint."""
    document_type: DocumentType
    college_name: Optional[str] = None  # string field for college name


class SubmissionResponse(BaseModel):
    """Response model for the /submit endpoint."""
    status: str
    document_type: str
    filename: Optional[str] = None
    college_name: Optional[str] = None
    evaluation: Optional[dict] = None
    message: str


class SignupRequest(BaseModel):
    """Request model for /auth/signup."""
    role: str  # "renter" or "owner"
    name: str
    phone: str
    email: str
    password: str


class LoginRequest(BaseModel):
    """Request model for /auth/login."""
    email: str
    password: str


class TokenResponse(BaseModel):
    """Response model for /auth/login."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class PropertyClassifyRequest(BaseModel):
    """Request model for /classify-property."""
    location: str
    rent: float
    deposit: float  # number of months


class DamageEvalRequest(BaseModel):
    """Request model for /evaluate-damage."""
    before_description: str
    after_description: str


class QuestionnaireRequest(BaseModel):
    """Request model for /questionnaire."""
    user_type: str  # "renter" or "owner"
    answers: dict   # { question_id: answer_value }
