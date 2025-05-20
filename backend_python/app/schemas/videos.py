from pydantic import BaseModel
from typing import Optional

class SchemaCriarVideos(BaseModel):
    titulo: str
    descricao: str
    categoria: Optional[str] = None
    url: str

class SchemaVideos(SchemaCriarVideos):
    id_video: int

    class Config:
        from_attributes = True
