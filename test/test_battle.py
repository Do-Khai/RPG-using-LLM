import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

@pytest.fixture
def valid_battle_request():
    return {
        "battleType": "CASUAL",
        "firstUserDisplayName": "Knight001",
        "firstUserStats": {
            "hp": 120.0,
            "atk": 90.0,
            "def": 30.0,
            "crit": 5.05,
            "critDamage": 240.0,
            "dodge": 10.0,
            "speed": 24.0
        },
        "secondUserDisplayName": "MageX",
        "secondUserStats": {
            "hp": 100.0,
            "atk": 80.0,
            "def": 20.0,
            "crit": 10.0,
            "critDamage": 200.0,
            "dodge": 15.0,
            "speed": 30.0
        }
    }

def test_battle_success(valid_battle_request):
    response = client.post("/api/v1/player-battle", json=valid_battle_request)
    assert response.status_code == 200
    response_data = response.json()
    assert "type" in response_data
    assert "title" in response_data
    assert "description" in response_data
    assert "status" in response_data
    assert "combat" in response_data

def test_battle_missing_first_user(valid_battle_request):
    del valid_battle_request["firstUserDisplayName"]
    response = client.post("/api/v1/player-battle", json=valid_battle_request)
    assert response.status_code == 422  # Missing required field should return validation error

def test_battle_invalid_stats(valid_battle_request):
    valid_battle_request["firstUserStats"]["hp"] = -100  # Invalid HP
    response = client.post("/api/v1/player-battle", json=valid_battle_request)
    assert response.status_code == 422  # Invalid stats should return validation error