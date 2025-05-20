from sqlalchemy import Column, Integer, String, ARRAY
from sqlalchemy.orm import relationship
from app.core.conexaoBD import Base
from app.models.associacoes import t_playlist_videos

class Playlist(Base):
    __tablename__ = "t_playlist"

    id_playlist = Column(Integer, primary_key=True, autoincrement=True)
    nome_playlist = Column(String, nullable=False)
    descricao = Column(String)

    videos = relationship(
        "Videos",
        secondary=t_playlist_videos,
        back_populates="playlists"
    )


