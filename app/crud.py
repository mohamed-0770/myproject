from sqlmodel import select
from fastapi import HTTPException
from typing import Annotated
from .DB import User, SessionDep

# ✅ دوال CRUD فقط - بدون app أو router

def create_user(session: SessionDep, user: User) -> User:
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def get_users(session: SessionDep, offset: int = 0, limit: int = 100):
    return session.exec(select(User).offset(offset).limit(limit)).all()

def get_user(session: SessionDep, user_id: int):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def delete_user(session: SessionDep, user_id: int):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    session.delete(user)
    session.commit()
    return {"ok": True}

def update_user(session: SessionDep, user_id: int, updated_user: User) -> User:
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # تحديث الحقول الموجودة
    user.name = updated_user.name
    user.age = updated_user.age
    user.secret_name = updated_user.secret_name
    
    session.add(user)
    session.commit()
    session.refresh(user)
    return user