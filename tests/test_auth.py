from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from database import get_session
from main import app
from models import table_registry


def make_client():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    table_registry.metadata.create_all(engine)

    def override_session():
        with Session(engine) as session:
            yield session

    app.dependency_overrides[get_session] = override_session
    return TestClient(app), engine


def test_authentication_flow_and_protected_recipe():
    client, _ = make_client()
    payload = {
        "email": "ana@example.com",
        "password": "SenhaSegura123",
        "re_password": "SenhaSegura123",
        "nome_usuario": "ana",
        "first_name": "Ana",
        "last_name": "Silva",
    }
    response = client.post("/auth/users/", json=payload)
    assert response.status_code == 201
    assert "senha" not in response.json()

    response = client.post("/auth/jwt/create/", json={"email": payload["email"], "password": payload["password"]})
    assert response.status_code == 200
    tokens = response.json()
    assert tokens["access"] and tokens["refresh"]

    assert client.get("/auth/users/me/").status_code == 401
    headers = {"Authorization": f"Bearer {tokens['access']}"}
    me = client.get("/auth/users/me/", headers=headers)
    assert me.status_code == 200
    assert me.json()["email"] == payload["email"]

    recipe = client.post("/receitas", json={"nome": "Bolo", "ingredientes": ["farinha"], "modo_de_preparo": "Misture"}, headers=headers)
    assert recipe.status_code == 201

    refreshed = client.post("/auth/jwt/refresh/", json={"refresh": tokens["refresh"]})
    assert refreshed.status_code == 200
    assert refreshed.json()["access"]


def test_wrong_password_is_rejected():
    client, _ = make_client()
    client.post("/auth/users/", json={"email": "bob@example.com", "password": "SenhaSegura123", "re_password": "SenhaSegura123", "nome_usuario": "bob"})
    response = client.post("/auth/jwt/create/", json={"email": "bob@example.com", "password": "errada123"})
    assert response.status_code == 401
