"""
Authentication module for RentShield.
Uses SQLite database for persistent user storage.
"""

import os
import time
import uuid
import bcrypt
import jwt
from typing import Optional

from backend.db import init_db, get_user_by_email, create_user

# JWT Configuration
JWT_SECRET = os.getenv("JWT_SECRET", "rentshield-dev-secret-key-change-in-prod")
JWT_ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_SECONDS = 3600       # 1 hour
REFRESH_TOKEN_EXPIRE_SECONDS = 86400 * 7  # 7 days

# Initialize DB on import
init_db()


def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(password: str, password_hash: str) -> bool:
    """Verify a password against its bcrypt hash."""
    return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))


def create_token(user_id: str, email: str, role: str, expires_in: int) -> str:
    """Create a JWT token."""
    payload = {
        "sub": user_id,
        "email": email,
        "role": role,
        "iat": int(time.time()),
        "exp": int(time.time()) + expires_in,
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def decode_token(token: str) -> Optional[dict]:
    """Decode and validate a JWT token."""
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def signup(role: str, name: str, phone: str, email: str, password: str) -> dict:
    """
    Register a new user (persisted to SQLite).
    Returns: {"user_id": str, "message": str} on success.
    Raises: ValueError if email already registered.
    """
    user_id = str(uuid.uuid4())
    password_hash = hash_password(password)

    # create_user raises ValueError if email already exists
    create_user(
        user_id=user_id,
        name=name,
        email=email,
        phone=phone,
        role=role,
        password_hash=password_hash,
    )

    return {"user_id": user_id, "message": "User registered successfully."}


def login(email: str, password: str) -> dict:
    """
    Authenticate a user and return JWT tokens.
    Returns: {"access_token": str, "refresh_token": str, "token_type": "bearer"}
    Raises: ValueError if credentials are invalid.
    """
    user = get_user_by_email(email)
    if not user:
        raise ValueError("Invalid email or password.")

    if not verify_password(password, user["password_hash"]):
        raise ValueError("Invalid email or password.")

    access_token = create_token(
        user["id"], user["email"], user["role"], ACCESS_TOKEN_EXPIRE_SECONDS
    )
    refresh_token = create_token(
        user["id"], user["email"], user["role"], REFRESH_TOKEN_EXPIRE_SECONDS
    )

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }
