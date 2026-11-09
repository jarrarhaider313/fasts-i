from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auth import create_access_token, refresh, verify_pass, verify_refresh_token
from dao.user_dao import create
from database import get_db
from models import user
from schema import TokenResponse, RefreshTokenResponse, users, userresponse

router = APIRouter(prefix="/api", tags=["Authentication"])


@router.post("/register", response_model=userresponse)
async def create_user(use: users, db: AsyncSession = Depends(get_db)):
    new_user = await create(use, db)
    if new_user is None:
        raise HTTPException(status_code=400, detail="User already exists")
    return new_user


@router.post("/login", response_model=TokenResponse)
async def login(use: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(user).where(user.username == use.username))
    existing_user = result.scalar_one_or_none()

    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")
    if not verify_pass(use.password, existing_user.password):
        raise HTTPException(status_code=403, detail="Invalid username or password")

    token = create_access_token(existing_user.id)
    refresh_token = refresh(existing_user.id)
    return {"access_token": token, "token_type": "bearer", "refresh_token": refresh_token}


@router.post("/refresh", response_model=RefreshTokenResponse)
def refresh_access_token(refresh_token: str = Body(..., embed=True)):
    user_id = verify_refresh_token(refresh_token)
    if user_id is None:
        raise HTTPException(status_code=401, detail="Expired refresh token")

    new_token = create_access_token(user_id)
    return {"access_token": new_token, "token_type": "bearer"}


