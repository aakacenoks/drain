import requests


def test_cycle_mode():
    response = requests.get("http://localhost:5000/api/cycle")
    response_body = response.json()
    assert response.status_code == 200
    assert response_body["message"] == "Cycle mode enabled"


def test_connect():
    response = requests.get("http://localhost:5000/api/connect")
    response_body = response.json()
    assert response.status_code == 200
    assert response_body["message"] == "Cycle mode disabled. All ports connected."
