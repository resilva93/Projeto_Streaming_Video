import pytest
from fastapi.testclient import TestClient
from app.main import app
import io

client = TestClient(app)

video_atualizado = {
    "titulo": "Video Atualizado",
    "descricao": "Nova descrição",
    "categoria": "Atualizado",
    "url": "video_atualizado.mp4"
}


@pytest.fixture
def criar_video():
    fake_file = io.BytesIO(b"conteudo de teste de video")
    response = client.post(
        "/api/videos/upload",
        data={
            "titulo": "Video Teste",
            "descricao": "Descrição do vídeo teste",
            "categoria": "Teste"
        },
        files={"file": ("video_teste.mp4", fake_file, "video/mp4")}
    )
    assert response.status_code == 201
    return response.json()["id"]


def test_criar_video():
    fake_file = io.BytesIO(b"conteudo de teste de video")
    response = client.post(
        "/api/videos/upload",
        data={
            "titulo": "Video Teste",
            "descricao": "Descrição do vídeo teste",
            "categoria": "Teste"
        },
        files={"file": ("video_teste.mp4", fake_file, "video/mp4")}
    )
    assert response.status_code == 201
    assert response.json()["mensagem"] == "Vídeo armazenado com sucesso!"
    assert "id" in response.json()


def test_listar_videos():
    response = client.get("/api/videos/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_atualizar_video(criar_video):
    video_id = criar_video
    response = client.put(f"/api/videos/{video_id}", json=video_atualizado)
    assert response.status_code == 200
    assert response.json()["titulo"] == video_atualizado["titulo"]


def test_deletar_video(criar_video):
    video_id = criar_video
    response = client.delete(f"/api/videos/{video_id}")
    assert response.status_code == 200
    assert response.json() == {"mensagem": "Vídeo deletado com sucesso"}

    # Verifica se foi realmente removido
    response = client.get(f"/api/videos/{video_id}")
    assert response.status_code == 404
