from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from auth import hash_pass
from cache import user_cache
from database import get_db
from dao.user_dao import deleteuser, read, update
from dependency import get_current_user
from schema import userresponse, users

router = APIRouter(prefix="/api", tags=["User Routes"])


@router.get("/user", response_model=userresponse)
async def read_user_data(user_id: int = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    cache_key = f"user_id{user_id}"
    if cache_key in user_cache:
        return user_cache[cache_key]

    user_data = await read(db, user_id)
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")

    user_cache[cache_key] = user_data
    return user_data


@router.put("/user", response_model=userresponse)
async def update_user(use: users, user_id: int = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    user_data = await read(db, user_id)
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")

    user_data.username = use.name
    user_data.password = hash_pass(use.password)
    await update(user_data, db)

    user_cache.pop(f"user_id{user_id}", None)
    return user_data


@router.delete("/delete_user", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    user_data = await read(db, user_id)
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")

    await deleteuser(user_data, db)
    user_cache.pop(f"user_id{user_id}", None)
    return None










