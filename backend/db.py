"""
Database module for RentShield.
Uses SQLite for persistent user storage.
"""

import os
import sqlite3
import threading

# Database file path (stored alongside the backend code)
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "rentshield.db")

# Thread-local storage for connections (SQLite connections are not thread-safe)
_local = threading.local()


def get_connection() -> sqlite3.Connection:
    """Get a thread-local SQLite connection."""
    if not hasattr(_local, "connection") or _local.connection is None:
        _local.connection = sqlite3.connect(DB_PATH)
        _local.connection.row_factory = sqlite3.Row
        _local.connection.execute("PRAGMA journal_mode=WAL")
    return _local.connection


def init_db():
    """Initialize the database schema. Safe to call multiple times."""
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT NOT NULL,
            role TEXT NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS questionnaire_responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_email TEXT,
            user_type TEXT NOT NULL,
            answers TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_email) REFERENCES users(email)
        )
    """)
    conn.commit()


def get_user_by_email(email: str) -> dict | None:
    """Fetch a user by email. Returns dict or None."""
    conn = get_connection()
    cursor = conn.execute("SELECT * FROM users WHERE email = ?", (email.lower(),))
    row = cursor.fetchone()
    if row is None:
        return None
    return dict(row)


def create_user(user_id: str, name: str, email: str, phone: str, role: str, password_hash: str) -> dict:
    """Insert a new user into the database."""
    conn = get_connection()
    try:
        conn.execute(
            "INSERT INTO users (id, name, email, phone, role, password_hash) VALUES (?, ?, ?, ?, ?, ?)",
            (user_id, name, email.lower(), phone, role, password_hash),
        )
        conn.commit()
        return {"id": user_id, "name": name, "email": email.lower(), "phone": phone, "role": role}
    except sqlite3.IntegrityError:
        raise ValueError(f"Email '{email}' is already registered.")


def save_questionnaire_response(user_email: str | None, user_type: str, answers_json: str) -> int:
    """Save questionnaire answers to the database. Returns the row ID."""
    conn = get_connection()
    cursor = conn.execute(
        "INSERT INTO questionnaire_responses (user_email, user_type, answers) VALUES (?, ?, ?)",
        (user_email, user_type, answers_json),
    )
    conn.commit()
    return cursor.lastrowid


def get_all_users() -> list:
    """Fetch all users (for admin/debug). Returns list of dicts."""
    conn = get_connection()
    cursor = conn.execute("SELECT id, name, email, phone, role, created_at FROM users")
    return [dict(row) for row in cursor.fetchall()]
