from fastapi import FastAPI, Depends, Query, Body
from .DB import create_db_and_tables, SessionDep, User
from . import crud


app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
def read_root():
    return {"message": "hello api"}

@app.post("/users/")
def create_user_endpoint(user: User, session: SessionDep ):
    return crud.create_user(session, user)

@app.get("/users/")
def read_users_endpoint(
    session: SessionDep ,
    offset: int = 0,
    limit: int = Query(100, le=100)
):
    return crud.get_users(session, offset, limit)

@app.get("/users/{user_id}")
def read_user_endpoint(user_id: int, session: SessionDep ):
    return crud.get_user(session, user_id)

@app.delete("/users/{user_id}")
def delete_user_endpoint(user_id: int, session: SessionDep ):
    return crud.delete_user(session, user_id)

@app.put("/users/{user_id}")
def update_user_endpoint(user_id: int, updated_user: User, session: SessionDep):
    return crud.update_user(session, user_id, updated_user)