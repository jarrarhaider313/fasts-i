from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Task
from schema import tasks


async def read(db: AsyncSession, user_id: int):
    result = await db.execute(select(Task).where(Task.user_id == user_id))
    return result.scalars().all()


async def get_task_by_id(db: AsyncSession, task_id: int, user_id: int):
    result = await db.execute(select(Task).where(Task.id == task_id, Task.user_id == user_id))
    return result.scalar_one_or_none()


async def update(use: Task, db: AsyncSession):
    db.add(use)
    await db.commit()
    await db.refresh(use)


async def delete_task(task: Task, db: AsyncSession):
    await db.delete(task)
    await db.commit()


async def create(use: tasks, db: AsyncSession, user_id: int):
    new_task = Task(title=use.title, description=use.description, user_id=user_id)
    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)
    return new_task

