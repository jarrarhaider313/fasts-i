from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auth import hash_pass
from models import user
from schema import users


async def read(db: AsyncSession, user_id: int):
    result = await db.execute(select(user).where(user.id == user_id))
    return result.scalar_one_or_none()


async def update(use: user, db: AsyncSession):
    db.add(use)
    await db.commit()
    await db.refresh(use)


async def deleteuser(us: user, db: AsyncSession):
    await db.delete(us)
    await db.commit()


async def create(use: users, db: AsyncSession):
    existing_use = await db.execute(select(user).where(user.username == use.name))
    existing_user = existing_use.scalar_one_or_none()
    if existing_user:
        return None

    new_user = user(username=use.name, password=hash_pass(use.password))
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user
