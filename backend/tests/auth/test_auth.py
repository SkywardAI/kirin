from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.main import initialize_backend_application


app = initialize_backend_application()

client = TestClient(app)



def test_regist_user():
    response = client.post(
        "/api/auth/signin",
        headers={"Content-Type": "application/json"},
        json={"username": "aisuko", "email": "aisuko@example.com", "password": "aisuko"},
    )
    assert response.status_code == 200
    assert response.json() is not None


def test_auth_signin():
    response = client.post(
        "/api/auth/signin",
        headers={"Content-Type": "application/json"},
        json={"username": "admin","password": "admin"},
    ) 
    assert response.status_code == 200
    assert response.json()  is not None
    
def test_get_token():
    response = client.get("/api/auth/token", headers={"accept": "application/json"})
    assert response.status_code == 200
    assert response.json()  is not None

def testi_auth_verify():
    response = client.post(
        "/api/auth/verify",
        headers={"Content-Type": "application/json"},
        json={"username": "admin", "password": "aisuko"},
    )
    assert response.status_code == 200
    assert response.json() is not None