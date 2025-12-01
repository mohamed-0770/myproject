from typing import Annotated
from fastapi import Depends
from sqlmodel import Field, Session, SQLModel, create_engine

# ✅ اسم الكلاس: User (ليس USER أو USERT)
class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    age: int | None = Field(default=None, index=True)
    secret_name: str

# إعداد قاعدة البيانات SQLite
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"
connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)

# إنشاء الجداول
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# جلسة قاعدة البيانات
def get_session():
    with Session(engine) as session:
        yield session

# ✅ SessionDep للتعامل مع Depends في FastAPI
SessionDep = Annotated[Session, Depends(get_session)]
