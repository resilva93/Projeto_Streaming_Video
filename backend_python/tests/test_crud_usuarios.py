import pytest
from fastapi.testclient import TestClient
from app.main import app
from uuid import uuid4

client = TestClient(app)


def gerar_dados_usuario():
    login = f"testuser_{uuid4().hex[:6]}"
    return {
        "usuario": {
            "nome_usuario": "Usuário Teste",
            "login": login,
            "senha": "senha123"
        },
        "login": {
            "login": login,
            "senha": "senha123"
        },
        "nova_senha": {
            "login": login,
            "senha_atual": "senha123",
            "nova_senha": "novaSenha456"
        }
    }


def test_criar_usuario():
    dados = gerar_dados_usuario()
    response = client.post("/api/usuarios/criar", json=dados["usuario"])
    assert response.status_code == 200
    data = response.json()
    assert data["msg"] == "Usuário criado com sucesso"
    assert "id" in data


def test_login_usuario():
    dados = gerar_dados_usuario()

    # Cria usuário primeiro
    response = client.post("/api/usuarios/criar", json=dados["usuario"])
    assert response.status_code == 200

    # Faz login
    response = client.post("/api/usuarios/login", json=dados["login"])
    assert response.status_code == 200, f"Erro no login: {response.text}"

    data = response.json()
    assert "login" in data
    assert data["login"] == dados["login"]["login"]


def test_trocar_senha():
    dados = gerar_dados_usuario()

    # Cria usuário
    response = client.post("/api/usuarios/criar", json=dados["usuario"])
    assert response.status_code == 200

    # Troca senha
    response = client.put("/api/usuarios/perfil/trocar-senha", json=dados["nova_senha"])
    assert response.status_code == 200, f"Erro ao trocar senha: {response.text}"
    assert response.json() == {"msg": "Senha atualizada com sucesso"}
