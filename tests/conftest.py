import sys
import os
from typing import Generator
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient

# Adjust the Python path to import the app module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.main import app
from app.config.database import Base, get_session
from app.models.user import User

# User details for testing
USER_NAME = "Keshari Nandan"
USER_EMAIL = "keshari@describly.com"
USER_PASSWORD = "123#Describly"

# Create an SQLite engine for testing
engine = create_engine("sqlite:///./fastapi.db")
SessionTesting = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def test_session() -> Generator: #Creates a database session for each test, ensuring isolation.
    session = SessionTesting()
    try:
        yield session
    finally:
        session.close()

@pytest.fixture(scope="function") #Sets up the test application by creating database tables and tears them down after the test.
def app_test():
    Base.metadata.create_all(bind=engine)
    yield app
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function") # Creates a test client, overrides the get_session dependency, and provides a testing environment.
def client(app_test, test_session):
    def _test_db():
        try:
            yield test_session
        finally:
            pass
    app_test.dependency_overrides[get_session] = _test_db
    return TestClient(app_test)
