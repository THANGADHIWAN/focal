"""
Password hashing and verification utilities.
"""
from typing import Optional
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app.db.models import Users

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    Hash a password
    """
    return pwd_context.hash(password)

def authenticate_user(db: Session, email: str, password: str) -> Optional[Users]:
    """
    Authenticate a user by email and password
    """
    user = db.query(Users).filter(Users.email == email).first()
    
    if not user:
        return None
    
    if not verify_password(password, user.hashed_password):
        return None
    
    return user
