import os
from datetime import datetime, timedelta, timezone

from dotenv import load_dotenv
from jose import JWTError, jwt
from passlib.context import CryptContext

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY") or os.getenv("secret_key") or "mysecretkey"
ALGORITHM = os.getenv("ALGORITHM") or os.getenv("Algorithm") or "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_pass(password: str) -> str:
    return pwd_context.hash(password)


def verify_pass(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)


def create_access_token(user_id: int) -> str:
    expire = datetime.now(timezone.utc) + timedelta(days=3)
    payload = {"sub": str(user_id), "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def refresh(user_id: int) -> str:
    expire = datetime.now(timezone.utc) + timedelta(days=7)
    payload = {"sub": str(user_id), "type": "Refresh", "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def verify_refresh_token(refresh_token: str):
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload.get("type") != "Refresh":
            return None
        return int(payload.get("sub"))
    except JWTError:
        return None

