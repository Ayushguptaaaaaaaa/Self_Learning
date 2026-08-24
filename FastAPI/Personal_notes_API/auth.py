from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, Header, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User

# Secret key for signing JWT tokens (use a random string)
SECRET_KEY = "your-secret-key-change-this-in-production"

# Algorithm for JWT
ALGORITHM = "HS256"

# Token expiration time (30 minutes)
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing context (using argon2 instead of bcrypt to avoid version issues)
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a plain password"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify plain password against hash"""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    """Create JWT access token"""
    to_encode = data.copy()
    
    # Set expiration time (30 minutes from now)
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    # Encode and sign token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt

def verify_token(token: str) -> dict:
    """Verify and decode JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

def get_current_user(token: str = Header(None), db: Session = Depends(lambda: SessionLocal())) -> User:
    """
    Dependency to get current authenticated user
    Used on protected routes
    """
    if not token:
        raise HTTPException(
            status_code=401,
            detail="Token missing"
        )
    
    # Verify token and get payload
    payload = verify_token(token)
    username: str = payload.get("sub")
    
    if username is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )
    
    # Get user from database
    user = db.query(User).filter(User.username == username).first()
    
    if user is None:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )
    
    return user