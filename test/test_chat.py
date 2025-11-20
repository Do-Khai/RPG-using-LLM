import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

@pytest.fixture
def valid_chat_request():
    return {
        "user_id": "test_user",
        "message": "/start",
        "all_region_data": [
            {"code": "VALORIA", "name": "Thành Valoria", "description": "Vùng đất ánh sáng."},
            {"code": "CELESTRA", "name": "Thung lũng Celestra", "description": "Vùng đất phép thuật."}
        ],
        "current_stats": {"level": 1, "hp": 100, "atk": 10},
        "next_stats": {"level": 2, "hp": 120, "atk": 15},
        "user_state": {"faction": "LIGHT", "gender": "male"},
        "recent_messages": [{"role": "user", "content": "Hello"}],
        "last_story": {"title": "Quest 1", "description": "Start your journey."}
    }

def test_chat_success(valid_chat_request):
    response = client.post("/api/v1/chat", json=valid_chat_request)
    response_data = response.json()
    assert "choices" in response_data
    assert "description" in response_data
    assert "title" in response_data
    assert "type" in response_data

def test_chat_missing_user_id(valid_chat_request):
    del valid_chat_request["user_id"]
    response = client.post("/api/v1/chat", json=valid_chat_request)
    assert response.status_code == 422  # Missing required field should return validation error

def test_chat_invalid_region_data(valid_chat_request):
    valid_chat_request["all_region_data"] = "invalid_data"
    response = client.post("/api/v1/chat", json=valid_chat_request)
    assert response.status_code == 422  # Invalid data type should return validation error