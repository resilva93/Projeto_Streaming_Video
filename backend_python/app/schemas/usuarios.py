from pydantic import BaseModel

class SchemaUsuario(BaseModel):
    id_usuario: int
    nome_usuario: str
    login: str

    class Config:
        from_attributes = True  
