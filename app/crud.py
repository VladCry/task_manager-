from sqlalchemy.orm import Session
from . import models, schemas
from .core.security import get_password_hash

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed = get_password_hash(user.password)
    db_user = models.User(username=user.username, email=user.email, hashed_password=hashed)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_tasks(db: Session, skip: int = 0, limit: int = 100, owner_id: int = None, status: str = None):
    query = db.query(models.Task)
    if owner_id:
        query = query.filter(models.Task.owner_id == owner_id)
    if status:
        query = query.filter(models.Task.status == status)
    return query.offset(skip).limit(limit).all()

def create_task(db: Session, task: schemas.TaskCreate, owner_id: int):
    db_task = models.Task(**task.model_dump(), owner_id=owner_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def get_task(db: Session, task_id: int):
    return db.query(models.Task).filter(models.Task.id == task_id).first()

def update_task(db: Session, task_id: int, task_update: schemas.TaskUpdate):
    db_task = get_task(db, task_id)
    if not db_task:
        return None
    for key, value in task_update.model_dump(exclude_unset=True).items():
        setattr(db_task, key, value)
    db.commit()
    db.refresh(db_task)
    return db_task

def delete_task(db: Session, task_id: int):
    db_task = get_task(db, task_id)
    if not db_task:
        return None
    db.delete(db_task)
    db.commit()
    return db_task

def create_comment(db: Session, comment: schemas.CommentCreate, task_id: int, author_id: int):
    db_comment = models.Comment(**comment.model_dump(), task_id=task_id, author_id=author_id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment
