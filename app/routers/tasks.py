from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional

from .. import schemas, models, crud
from ..dependencies import get_db, get_current_active_user

router = APIRouter(prefix="/api/tasks", tags=["tasks"])

@router.post("/", response_model=schemas.Task)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    return crud.create_task(db, task, owner_id=current_user.id)

@router.get("/", response_model=list[schemas.Task])
def list_tasks(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    owner_id = None if current_user.role == models.UserRole.ADMIN else current_user.id
    return crud.get_tasks(db, skip, limit, owner_id, status)

@router.get("/{task_id}", response_model=schemas.Task)
def get_task(task_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    task = crud.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if current_user.role != models.UserRole.ADMIN and task.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return task

@router.put("/{task_id}", response_model=schemas.Task)
def update_task(task_id: int, task_update: schemas.TaskUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    task = crud.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if current_user.role != models.UserRole.ADMIN and task.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    updated = crud.update_task(db, task_id, task_update)
    return updated

@router.delete("/{task_id}", response_model=dict)
def delete_task(task_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    task = crud.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if current_user.role != models.UserRole.ADMIN and task.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    crud.delete_task(db, task_id)
    return {"detail": "Task deleted"}

@router.post("/{task_id}/comments", response_model=schemas.Comment)
def add_comment(task_id: int, comment: schemas.CommentCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    task = crud.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if current_user.role != models.UserRole.ADMIN and task.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return crud.create_comment(db, comment, task_id, current_user.id)

@router.get("/{task_id}/comments", response_model=list[schemas.Comment])
def get_comments(task_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_active_user)):
    task = crud.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if current_user.role != models.UserRole.ADMIN and task.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return db.query(models.Comment).filter(models.Comment.task_id == task_id).all()
