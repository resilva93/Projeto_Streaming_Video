from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from app.core.conexaoBD import get_db
from app.models.videos import Videos
from app.schemas.videos import SchemaVideos, SchemaCriarVideos
from typing import List
import os
import shutil
import requests as rq
import streamlit as st
from dotenv import load_dotenv

# Carrega variáveis de ambiente do .env
load_dotenv()

router = APIRouter(
    prefix="/api/videos",
    tags=["videos"]
)

UPLOAD_DIR = "app/static/videos"

# Upload de vídeo
@router.post("/upload", status_code=201)
async def upload_video(
    titulo: str = Form(...),
    descricao: str = Form(...),
    categoria: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    try:
        if not os.path.exists(UPLOAD_DIR):
            os.makedirs(UPLOAD_DIR)

        file_location = os.path.join(UPLOAD_DIR, file.filename)

        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        novo_video = Videos(
            titulo=titulo,
            descricao=descricao,
            categoria=categoria,
            url=f"/static/videos/{file.filename}"
        )
        db.add(novo_video)
        db.commit()
        db.refresh(novo_video)

        return JSONResponse(
            status_code=201,
            content={
                "mensagem": "Vídeo armazenado com sucesso!",
                "id": novo_video.id_video
            }
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro no upload: {str(e)}")


# Listar todos os vídeos
@router.get("/", response_model=List[SchemaVideos])
def carregar_videos(db: Session = Depends(get_db)):
    return db.query(Videos).all()

#Consulta no API do Youtube
@router.get("/apiexterna_consulta")
def consultaExterna(txtPesquisa: str):
    chaveAcessoYT = os.getenv('YOUTUBE_API_KEY')
    url_consulta = f"https://www.googleapis.com/youtube/v3/search?key={chaveAcessoYT}&q={txtPesquisa}&type=video&part=snippet&maxResults=5"
    try:
        response = rq.get(url_consulta)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Erro na API do YouTube")
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na consulta externa: {str(e)}")
    
# Obter vídeo por ID
@router.get("/{video_id}", response_model=SchemaVideos)
def selecionar_video(video_id: int, db: Session = Depends(get_db)):
    video = db.query(Videos).filter(Videos.id_video == video_id).first()
    if not video:
        raise HTTPException(status_code=404, detail="Vídeo não localizado!")
    return video


# Atualizar vídeo por ID
@router.put("/{video_id}", response_model=SchemaVideos)
def atualizar_video(video_id: int, video_data: SchemaCriarVideos, db: Session = Depends(get_db)):
    db_video = db.query(Videos).filter(Videos.id_video == video_id).first()
    if not db_video:
        raise HTTPException(status_code=404, detail="Vídeo não localizado!")

    for campo, valor in video_data.dict().items():
        if campo == "url" and not valor.startswith("/static/videos/"):
            valor = f"/static/videos/{valor}"
        setattr(db_video, campo, valor)

    db.commit()
    db.refresh(db_video)
    return db_video


# Excluir vídeo por ID
@router.delete("/{video_id}")
def excluir_video(video_id: int, db: Session = Depends(get_db)):
    db_video = db.query(Videos).filter(Videos.id_video == video_id).first()
    if not db_video:
        raise HTTPException(status_code=404, detail="Vídeo não localizado!")

    db.delete(db_video)
    db.commit()
    return {"mensagem": "Vídeo deletado com sucesso"}
