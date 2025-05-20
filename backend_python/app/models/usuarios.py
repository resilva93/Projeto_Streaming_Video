from sqlalchemy import Column, Integer, String
from app.core.conexaoBD import Base

class Usuarios(Base):
    __tablename__ = "t_usuarios"

    id_usuario = Column(Integer, primary_key=True, index=True)
    nome_usuario = Column(String, nullable=False)
    login = Column(String, unique=True, nullable=False)
    senha = Column(String, nullable=False)
