import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

playlist_teste = {
    "nome_playlist": "Playlist Teste",
    "descricao": "Descrição de teste",
    "videos_ids": []
}

playlist_atualizada = {
    "nome_playlist": "Playlist Atualizada",
    "descricao": "Nova descrição atualizada",
    "videos_ids": []
}


@pytest.fixture
def criar_playlist():
    response = client.post("/api/playlists/", json=playlist_teste)
    assert response.status_code == 201
    return response.json()["id_playlist"]


def test_criar_playlist():
    response = client.post("/api/playlists/", json=playlist_teste)
    assert response.status_code == 201
    data = response.json()
    assert data["mensagem"] == "Playlist criada com sucesso!"
    assert "id_playlist" in data


def test_listar_playlists():
    response = client.get("/api/playlists/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_atualizar_playlist(criar_playlist):
    playlist_id = criar_playlist
    response = client.put(f"/api/playlists/{playlist_id}", json=playlist_atualizada)
    assert response.status_code == 200
    data = response.json()
    assert data["nome_playlist"] == playlist_atualizada["nome_playlist"]


def test_deletar_playlist(criar_playlist):
    playlist_id = criar_playlist
    response = client.delete(f"/api/playlists/{playlist_id}")
    assert response.status_code == 200
    assert response.json() == {"mensagem": "Playlist deletada com sucesso"}

    # Verifica que foi removida
    response = client.get(f"/api/playlists/{playlist_id}/videos")
    assert response.status_code == 404
