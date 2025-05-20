from pydantic import BaseModel
from typing import List, Optional


class PlaylistCreate(BaseModel):
    nome_playlist: str
    descricao: Optional[str] = None
    videos_ids: List[int] = []

    class Config:
        from_attributes = True


class SchemaVideo(BaseModel):
    id_video: int
    titulo: str
    descricao: str
    categoria: Optional[str]
    url: str

    class Config:
        from_attributes = True


class SchemaPlaylist(BaseModel):
    id_playlist: int
    nome_playlist: str
    descricao: Optional[str]
    videos: List[SchemaVideo]

    class Config:
        from_attributes = True
