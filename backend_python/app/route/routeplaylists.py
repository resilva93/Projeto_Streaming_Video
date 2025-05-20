from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.playlists import Playlist
from app.models.videos import Videos
from app.core.conexaoBD import get_db
from app.schemas.playlists import PlaylistCreate
from typing import List

router = APIRouter(
    prefix="/api/playlists",
    tags=["playlists"]
)

# Criar nova playlist
@router.post("/", status_code=201)
def criar_playlist(payload: PlaylistCreate, db: Session = Depends(get_db)):
    try:
        nova_playlist = Playlist(
            nome_playlist=payload.nome_playlist,
            descricao=payload.descricao
        )

        if payload.videos_ids:
            videos = db.query(Videos).filter(Videos.id_video.in_(payload.videos_ids)).all()
            if not videos:
                raise HTTPException(
                    status_code=400,
                    detail="Nenhum vídeo válido foi encontrado com os IDs fornecidos."
                )
            nova_playlist.videos = videos

        db.add(nova_playlist)
        db.commit()
        db.refresh(nova_playlist)

        return {
            "mensagem": "Playlist criada com sucesso!",
            "id_playlist": nova_playlist.id_playlist
        }

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro ao criar playlist: {str(e)}")


# Atualizar playlist
@router.put("/{playlist_id}")
def atualizar_playlist(playlist_id: int, payload: PlaylistCreate, db: Session = Depends(get_db)):
    playlist = db.query(Playlist).filter(Playlist.id_playlist == playlist_id).first()
    if not playlist:
        raise HTTPException(status_code=404, detail="Playlist não encontrada")

    playlist.nome_playlist = payload.nome_playlist
    playlist.descricao = payload.descricao

    if payload.videos_ids:
        videos = db.query(Videos).filter(Videos.id_video.in_(payload.videos_ids)).all()
        playlist.videos = videos
    else:
        playlist.videos = []

    db.commit()
    db.refresh(playlist)

    return {
        "id_playlist": playlist.id_playlist,
        "nome_playlist": playlist.nome_playlist,
        "descricao": playlist.descricao
    }


# Listar vídeos de uma playlist
@router.get("/{playlist_id}/videos")
def listar_videos_playlist(playlist_id: int, db: Session = Depends(get_db)):
    playlist = db.query(Playlist).filter(Playlist.id_playlist == playlist_id).first()
    if not playlist:
        raise HTTPException(status_code=404, detail="Playlist não encontrada")

    videos = [
        {
            "id_video": video.id_video,
            "titulo": video.titulo,
            "descricao": video.descricao,
            "categoria": video.categoria,
            "url": video.url
        }
        for video in playlist.videos
    ]
    return {
        "id_playlist": playlist.id_playlist,
        "nome_playlist": playlist.nome_playlist,
        "videos": videos
    }


# Excluir uma playlist
@router.delete("/{playlist_id}")
def deletar_playlist(playlist_id: int, db: Session = Depends(get_db)):
    playlist = db.query(Playlist).filter(Playlist.id_playlist == playlist_id).first()
    if not playlist:
        raise HTTPException(status_code=404, detail="Playlist não encontrada")

    db.delete(playlist)
    db.commit()
    return {"mensagem": "Playlist deletada com sucesso"}


# Adicionar vídeo à playlist
@router.post("/{playlist_id}/add-video/{video_id}")
def adicionar_video_playlist(playlist_id: int, video_id: int, db: Session = Depends(get_db)):
    playlist = db.query(Playlist).filter(Playlist.id_playlist == playlist_id).first()
    video = db.query(Videos).filter(Videos.id_video == video_id).first()

    if not playlist or not video:
        raise HTTPException(status_code=404, detail="Playlist ou vídeo não encontrado")

    if video in playlist.videos:
        raise HTTPException(status_code=400, detail="Vídeo já adicionado à playlist")

    playlist.videos.append(video)
    db.commit()
    return {"mensagem": "Vídeo adicionado à playlist com sucesso"}


# Remover vídeo da playlist
@router.delete("/{playlist_id}/remove-video/{video_id}")
def remover_video_playlist(playlist_id: int, video_id: int, db: Session = Depends(get_db)):
    playlist = db.query(Playlist).filter(Playlist.id_playlist == playlist_id).first()
    video = db.query(Videos).filter(Videos.id_video == video_id).first()

    if not playlist or not video:
        raise HTTPException(status_code=404, detail="Playlist ou vídeo não encontrado")

    if video not in playlist.videos:
        raise HTTPException(status_code=400, detail="Vídeo não está na playlist")

    playlist.videos.remove(video)
    db.commit()
    return {"mensagem": "Vídeo removido da playlist com sucesso"}


# Listar todas as playlists
@router.get("/", status_code=200)
def listar_playlists(db: Session = Depends(get_db)):
    playlists = db.query(Playlist).all()

    return [
        {
            "id_playlist": p.id_playlist,
            "nome_playlist": p.nome_playlist,
            "descricao": p.descricao
        } for p in playlists
    ]
