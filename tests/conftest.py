from typing import Generator

import pytest
from fastapi.testclient import TestClient
from api.config import settings
from api.app import app  # type: ignore
from sqlmodel import Session, create_engine
from api.models import SQLModel
from api.db import get_session

from .providers import set_factories_session


engine = create_engine(
    settings.db.uri,  # pyright: ignore
)


@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    """
    Create the test database schema before any tests run,
    and drop it after all tests are done.
    """
    SQLModel.metadata.create_all(bind=engine)  # Create tables
    yield
    SQLModel.metadata.drop_all(bind=engine)  # Drop tables after tests


@pytest.fixture(scope="function")
def db() -> Generator:
    """
    Create a new database session for each test and roll it back after the test.
    """
    connection = engine.connect()
    transaction = connection.begin()
    with Session(engine) as session:
        yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture(scope="function")
def client(db: Session) -> Generator[TestClient, None, None]:
    """
    Provide a TestClient that uses the test database session.
    Override the get_db dependency to use the test session.
    """

    def override_get_db():
        yield db

    app.dependency_overrides[get_session] = override_get_db

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()


@pytest.fixture(autouse=True)
def set_session_for_factories(db: Session):
    set_factories_session(db)
