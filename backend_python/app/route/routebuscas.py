from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session

from app.core.conexaoBD import get_db
from app.models.videos import Video
from app.models.playlists import Playlist
from app.schemas.videos import SchemaVideos, SchemaBuscaYT
from typing import List


router = APIRouter(
    prefix="/api/busca",
    tags=["Busca"]
)

@router.get("/videos", response_model=List[SchemaVideos])
def buscar_musicas(termo: str, db: Session = Depends(get_db)):
    termo_busca = f"%{termo}%"
    videos = db.query(Video).filter(
        Video.nome.ilike(termo_busca) |
        Video.artista.ilike(termo_busca) |
        Video.genero.ilike(termo_busca)
    ).all()

    if not videos:
        raise HTTPException(status_code=404, detail="Nenhuma videos encontrada.")

    return videos

@router.get("/playlists")
def buscar_playlists(
    termo: str = Query(..., description="Termo de busca no nome ou descrição da playlist"),
    db: Session = Depends(get_db)
):
    """Busca playlists filtrando por nome ou descrição."""
    termo_formatado = f"%{termo.lower()}%"
    playlists = db.query(Playlist).filter(
        (Playlist.NOME.ilike(termo_formatado)) |
        (Playlist.DESCRICAO.ilike(termo_formatado))
    ).all()
    return playlists


