import copy

import pytest
from fastapi.testclient import TestClient

from src.app import app, activities as activities_store


# Keep an immutable snapshot of the original activities for test isolation
_ORIGINAL_ACTIVITIES = copy.deepcopy(activities_store)


@pytest.fixture
def client():
    """Provide a TestClient for the FastAPI app."""
    with TestClient(app) as c:
        yield c


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset the in-memory activities store before and after each test."""
    activities_store.clear()
    activities_store.update(copy.deepcopy(_ORIGINAL_ACTIVITIES))
    yield
    activities_store.clear()
    activities_store.update(copy.deepcopy(_ORIGINAL_ACTIVITIES))
