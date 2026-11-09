from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from dao.task_dao import create, delete_task, get_task_by_id, read, update
from database import get_db
from dependency import get_current_user
from schema import taskresponse, tasks

router = APIRouter(prefix="/api", tags=["Task Routes"])


@router.post("/tasks", response_model=taskresponse)
async def create_task(task: tasks, user_id: int = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    new_task = await create(task, db, user_id)
    return new_task


@router.get("/tasks", response_model=list[taskresponse])
async def list_tasks(user_id: int = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    tasks_list = await read(db, user_id)
    return tasks_list


@router.get("/tasks/{task_id}", response_model=taskresponse)
async def get_single_task(task_id: int, user_id: int = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    task = await get_task_by_id(db, task_id, user_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.put("/tasks/{task_id}", response_model=taskresponse)
async def update_task(task_id: int, task: tasks, user_id: int = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    existing_task = await get_task_by_id(db, task_id, user_id)
    if existing_task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    existing_task.title = task.title
    existing_task.description = task.description
    await update(existing_task, db)
    return existing_task


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task_endpoint(task_id: int, user_id: int = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    task = await get_task_by_id(db, task_id, user_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    await delete_task(task, db)
    return None
