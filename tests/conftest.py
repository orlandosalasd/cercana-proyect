import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.base import Base
from app.main import app
from fastapi.testclient import TestClient
from app.db.session import get_db
from app.core.settings import settings


engine = create_engine(settings.TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override get_db dependency."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="session", autouse=True)
def prepare_database():
    """Create test database."""
    Base.metadata.create_all(bind=engine)
    app.dependency_overrides[get_db] = override_get_db
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    """App test client."""
    with TestClient(app) as c:
        yield c


@pytest.fixture(autouse=True)
def clean_tables():
    """Delete test data to start tests"""
    from sqlalchemy import text

    with engine.connect() as conn:
        trans = conn.begin()
        for table in reversed(Base.metadata.sorted_tables):
            conn.execute(text(f"TRUNCATE TABLE {table.name} RESTART IDENTITY CASCADE;"))
        trans.commit()


@pytest.fixture
def header_user_token(client):
    """Create and generate test user and bearer token"""
    email = "user@example.com"
    password = "123456"
    client.post(
        "/auth/register",
        json={"email": email, "password": password, "full_name": "test name"},
    )
    response = client.post("/auth/login", json={"email": email, "password": password})
    headers = {"Authorization": f"Bearer {response.json()["access_token"]}"}
    return headers
