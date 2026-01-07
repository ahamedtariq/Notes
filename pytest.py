import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.models.notes import Note
from database import get_db
from app.services import summarizer

# -----------------------------
# Test Database (SQLite)
# -----------------------------
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:123456@localhost:5432/notes_db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)

# -----------------------------
# Override DB Dependency
# -----------------------------
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

# -----------------------------
# Mock External API
# -----------------------------
async def fake_generate_summary(title: str):
    return "Mocked DuckDuckGo summary"

summarizer.generate_summary = fake_generate_summary


# -----------------------------
# Setup & Teardown
# -----------------------------
@pytest.fixture(scope="module", autouse=True)
def setup_database():
    Note.metadata.create_all(bind=engine)
    yield
    Note.metadata.drop_all(bind=engine)


# -----------------------------
# TESTS
# -----------------------------

def test_create_note():
    response = client.post(
        "/notes/create_notes",
        json={
            "title": "Artificial Intelligence",
            "content": "AI is a branch of computer science."
        }
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Notes Created Succcessfully"


def test_get_all_notes():
    response = client.get("/notes/get_all_notes")

    assert response.status_code == 200
    assert "data" in response.json()
    assert len(response.json()["data"]) >= 1


def test_get_specific_note():
    response = client.get("/notes/get_note/1")

    assert response.status_code == 200
    data = response.json()

    assert data["title"] == "Artificial Intelligence"
    assert data["summary"] == "Mocked DuckDuckGo summary"


def test_update_note():
    response = client.put(
        "/notes/update_note/1",
        json={
            "title": "AI Updated"
        }
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Note Updated Successfully"


def test_delete_note():
    response = client.delete("/notes/delete_note/1")

    assert response.status_code == 200
    assert response.json()["message"] == "Note Deleted Successfully"


def test_get_deleted_note():
    response = client.get("/notes/get_note/1")

    assert response.status_code == 404
