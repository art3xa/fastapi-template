import pytest
from fastapi.testclient import TestClient

from src.app.main import app


@pytest.fixture
def client():
    test_app = TestClient(app)
    return test_app
