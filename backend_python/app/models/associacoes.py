from sqlalchemy import Table, Column, Integer, ForeignKey
from app.core.conexaoBD import Base

t_playlist_videos = Table(
    "t_playlist_videos",
    Base.metadata,
    Column("id_playlist", Integer, ForeignKey("t_playlist.id_playlist")),
    Column("id_video", Integer, ForeignKey("t_video.id_video"))
)
