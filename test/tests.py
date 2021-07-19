import requests

BASE_URL = "http://localhost:5000/api"

def test_cycle_mode():
    response = requests.get(f'{BASE_URL}/cycle')
    response_body = response.json()
    assert response.status_code == 200
    assert response_body["message"] == "Cycle mode enabled"

def test_connect():
    response = requests.get(f'{BASE_URL}/connect')
    response_body = response.json()
    assert response.status_code == 200
    assert response_body["message"] == "Cycle mode disabled. All ports connected."

def test_status():
    response = requests.get(f'{BASE_URL}/status')
    response_body = response.json()
    assert response.status_code == 200
    assert len(response_body) > 0