from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.conexaoBD import SessionLocal
from app.models.usuarios import Usuarios
from pydantic import BaseModel
from passlib.context import CryptContext
from app.schemas import usuarios
from typing import List
from app.schemas.usuarios import SchemaUsuario


router = APIRouter(prefix="/api/usuarios", tags=["usuários"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Dependência para obter a sessão do banco
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Esquemas Pydantic
class UsuarioCreate(BaseModel):
    nome_usuario: str
    login: str
    senha: str


class UsuarioLogin(BaseModel):
    login: str
    senha: str


class TrocarSenhaRequest(BaseModel):
    login: str
    senha_atual: str
    nova_senha: str


# Criar novo usuário
@router.post("/criar")
def criar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    usuario_existente = db.query(Usuarios).filter(Usuarios.login == usuario.login).first()
    if usuario_existente:
        raise HTTPException(status_code=400, detail="Login já existe")

    novo_usuario = Usuarios(
        nome_usuario=usuario.nome_usuario,
        login=usuario.login,
        senha=pwd_context.hash(usuario.senha),
    )
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    return {"msg": "Usuário criado com sucesso", "id": novo_usuario.id_usuario}


#Login
@router.post("/login")
def login(usuario: UsuarioLogin, db: Session = Depends(get_db)):
    user = db.query(Usuarios).filter(Usuarios.login == usuario.login).first()
    if not user or not pwd_context.verify(usuario.senha, user.senha):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    return {
        "msg": f"Bem-vindo, {user.nome_usuario}",
        "usuario_id": user.id_usuario,
        "login": user.login
    }



# Trocar senha
@router.put("/perfil/trocar-senha")
def trocar_senha(req: TrocarSenhaRequest, db: Session = Depends(get_db)):
    user = db.query(Usuarios).filter(Usuarios.login == req.login).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    if not pwd_context.verify(req.senha_atual, user.senha):
        raise HTTPException(status_code=400, detail="Senha atual incorreta")

    user.senha = pwd_context.hash(req.nova_senha)
    db.commit()
    return {"msg": "Senha atualizada com sucesso"}


# Listar todos os usuários
@router.get("/listar", response_model=List[SchemaUsuario])
def listar_usuarios(db: Session = Depends(get_db)):
    return db.query(Usuarios).all()
