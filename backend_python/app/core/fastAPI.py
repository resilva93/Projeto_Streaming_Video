from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.models.videos import Videos
from app.core.conexaoBD import get_db
import os
import shutil

router = APIRouter(
    prefix="/api/upload",
    tags=["upload"],
)

UPLOAD_DIR = "app/static/videos"


@router.post("/", status_code=201)
async def carregar_videos(
    nome: str = Form(...),
    artista: str = Form(...),
    genero: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    try:
        if not os.path.exists(UPLOAD_DIR):
            os.makedirs(UPLOAD_DIR)

        file_location = os.path.join(UPLOAD_DIR, file.filename)

        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        nova_video = Videos(
            nome=nome,
            artista=artista,
            genero=genero,
            url=f"/static/videos/{file.filename}"
        )
        db.add(nova_video)
        db.commit()
        db.refresh(nova_video)

        return JSONResponse(status_code=201, content={"mensagem": "Video enviado com sucesso!"})

    except Exception as e:
        print("Erro no upload:", str(e))
        raise HTTPException(
            status_code=500, detail=f"Erro no upload: {str(e)}")
