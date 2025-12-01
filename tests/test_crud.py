import pytest
from sqlmodel import Session, SQLModel, create_engine
from app.DB import User, get_session
from app import crud

# إعداد قاعدة بيانات مؤقتة للاختبار
sqlite_url = "sqlite:///:memory:"  # قاعدة بيانات في الذاكرة
engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})

@pytest.fixture
def session():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as s:
        yield s

def test_create_user(session):
    user = User(name="Ali", age=25, secret_name="HeroX")
    created = crud.create_user(session, user)
    assert created.id is not None
    assert created.name == "Ali"

def test_get_user(session):
    user = User(name="Sara", age=30, secret_name="HeroY")
    session.add(user)
    session.commit()
    session.refresh(user)
    
    fetched = crud.get_user(session, user.id)
    assert fetched.name == "Sara"

def test_update_user(session):
    user = User(name="John", age=20, secret_name="HeroZ")
    session.add(user)
    session.commit()
    session.refresh(user)
    
    updated_user = User(name="John Updated", age=21, secret_name="HeroZZ")
    result = crud.update_user(session, user.id, updated_user)
    assert result.name == "John Updated"

def test_delete_user(session):
    user = User(name="Mark", age=28, secret_name="HeroM")
    session.add(user)
    session.commit()
    session.refresh(user)
    
    response = crud.delete_user(session, user.id)
    assert response == {"ok": True}
