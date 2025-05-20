from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.conexaoBD import Base
from app.models.associacoes import t_playlist_videos

class Videos(Base):
    __tablename__ = "t_video"

    id_video = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String, nullable=False)
    descricao = Column(String, nullable=False)
    categoria = Column(String)
    url = Column(String, nullable=False)

    playlists = relationship(
        "Playlist",  
        secondary=t_playlist_videos,
        back_populates="videos"
    )
