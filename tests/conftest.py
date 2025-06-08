import pytest
from fastapi.testclient import TestClient
from Library.main import app
from Library.datab.database import engine
from Library.datab.dbmodels import Base

@pytest.fixture(autouse=True, scope="function")
def reset_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

@pytest.fixture
def client():
    return TestClient(app)