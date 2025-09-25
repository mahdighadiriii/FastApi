import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.dependencies import create_access_token
from app.main import app
from app.models import User

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)


@pytest.fixture
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)


@pytest.fixture
def test_user(db):
    user = User(username="testuser", hashed_password="123")
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def auth_headers(test_user):
    access_token = create_access_token(data={"sub": str(test_user.id)})
    return {"Authorization": f"Bearer {access_token}"}


def test_get_nonexistent_expense(client, auth_headers):
    response = client.get(
        "/expenses/999", headers=auth_headers, params={"lang": "fa"}
    )
    assert response.status_code == 404
    assert response.json() == {
        "status": "error",
        "message": "هزینه یافت نشد",
    }


def test_delete_nonexistent_expense(client, auth_headers):
    response = client.delete(
        "/expenses/999", headers=auth_headers, params={"lang": "fa"}
    )
    assert response.status_code == 404
    assert response.json() == {
        "status": "error",
        "message": "هزینه یافت نشد",
    }


def test_create_expense_success(client, auth_headers):
    response = client.post(
        "/expenses/",
        json={"description": "Coffee", "amount": 5.0},
        headers=auth_headers,
        params={"lang": "en"},
    )
    assert response.status_code == 200
    assert "id" in response.json()
    assert response.json()["description"] == "Coffee"
    assert response.json()["amount"] == 5.0


def test_get_expenses_success(client, auth_headers, db):
    client.post(
        "/expenses/",
        json={"description": "Coffee", "amount": 5.0},
        headers=auth_headers,
        params={"lang": "en"},
    )
    response = client.get(
        "/expenses/", headers=auth_headers, params={"lang": "en"}
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0
    assert response.json()[0]["description"] == "Coffee"
