import requests

BASE_URL = "http://localhost:5004/api"

def test_status():
    response = requests.get(f'{BASE_URL}/status')
    response_body = response.json()
    assert response.status_code == 200
    assert len(response_body) > 0

def test_connect():
    response = requests.post(f'{BASE_URL}/connect')
    response_body = response.json()
    assert response.status_code == 200
    assert response_body["message"] == "cycle mode disabled. all ports connected. ready for testing."

def test_cycle_mode():
    response = requests.post(f'{BASE_URL}/cycle')
    response_body = response.json()
    assert response.status_code == 200
    assert response_body["message"] == "cycle mode enabled"