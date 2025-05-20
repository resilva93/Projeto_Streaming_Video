from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.core.conexaoBD import create_db

# Imports para registrar as rotas
from app.route import routeusuarios as usuarios
from app.route import routevideos as videos
from app.route import routeplaylists as playlist

# Imports para registrar as tabelas no SQLAlchemy (com nomes únicos!)
from app.models import associacoes
from app.models import videos as video_models
from app.models import playlists as playlist_models

app = FastAPI(title="Streaming Videos API")

# Configuração CORS
origins = [
    "http://localhost:5173", 
    "http://localhost:5173/", 
    "http://127.0.0.1:5173", 
    "http://127.0.0.1:5173/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Monta a pasta de arquivos estáticos
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Inicializa banco de dados com todas as tabelas
create_db()

# Registro de rotas
app.include_router(usuarios.router)
app.include_router(videos.router)
app.include_router(playlist.router)

@app.get("/")
async def root():
    return {"message": "Streaming de Vídeos executando"}

# Ativar log detalhado
import logging
logging.basicConfig(level=logging.DEBUG)
