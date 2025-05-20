
# 🎬 Plataforma de Streaming de Vídeos

Este projeto é uma aplicação web full-stack para upload, exibição, pesquisa e organização de vídeos, com gerenciamento de playlists. É composto por:

- Backend em **Python (FastAPI)**
- Frontend em **Vue.js + Vite**
- Banco de dados **SQLite**
- Containerização com **Podman**

---

## 📁 Estrutura do Projeto

```
.
├── backend_python/         # API REST com FastAPI
│   ├── app/                # Código principal da aplicação
│   ├── static/videos/      # Repositório dos vídeos
│   ├── BDStreamingVideo.db # Banco de dados SQLite
│   ├── Dockerfile          # Dockerfile do backend
│   └── requirements.txt    # Dependências Python
│
├── frontend_vue/           # Interface web com Vue.js
│   ├── src/                # Código Vue (componentes, views, router, etc)
│   ├── public/             # Arquivos públicos (favicon, etc)
│   ├── Dockerfile          # Dockerfile do frontend
│   ├── package.json        # Dependências do frontend
│   └── vite.config.js      # Configuração do Vite
```

---

## ⚙️ Instalação

### ✅ Pré-requisitos

- [Podman](https://podman.io/)
- [Node.js](https://nodejs.org/) (para desenvolvimento local do frontend, opcional)
- Python 3.11 (para desenvolvimento local do backend, opcional)

---

### 🐳 Execução com Podman

1. **Build do backend:**

```bash
cd backend_python
podman build -t backend-streaming .
```

2. **Build do frontend:**

```bash
cd frontend_vue
podman build -t frontend-streaming .
```

3. **Execução dos containers:**

```bash
podman run -d -p 8000:8000 backend-streaming
podman run -d -p 5173:5173 frontend-streaming
```

---

## 🌐 Rotas Principais

### 🔙 Backend (FastAPI)

- `POST /api/videos/upload` — Upload de vídeos
- `GET /api/videos/` — Listar vídeos
- `GET /api/videos/{id}` — Buscar vídeo por ID
- `POST /api/playlists/` — Criar nova playlist
- `GET /api/playlists/` — Listar playlists
- `POST /api/usuarios/` — Criar usuário
- `POST /api/usuarios/login` — Login de usuário
- `PUT /api/usuarios/alterar_senha` — Alterar senha
- `GET /apiexterna_consulta` — Buscar vídeos na API externa (YouTube)

---

### 🎨 Frontend (Vue.js)

- `/` — Página inicial com vídeos recentes
- `/search` — Página de pesquisa de vídeos
- `/upload` — Upload de vídeos
- `/videos` — Galeria de vídeos com paginação
- `/playlists` — Criação de playlists
- `/minhas-playlists` — Gerenciar playlists
- `/perfil` — Alteração de senha e informações do usuário
- `/login` — Login e criação de conta

---

## 🧪 Testes

Execute os testes do backend com:

```bash
cd backend_python
pytest
```

---

## 🧰 Tecnologias Utilizadas

### Backend
- FastAPI
- SQLAlchemy
- SQLite
- Uvicorn
- Passlib
- Pydantic

### Frontend
- Vue.js 3
- Vite
- Axios
- TailwindCSS

---

## 🗃️ Banco de Dados

O banco de dados **SQLite** é utilizado para armazenar:
- Usuários
- Vídeos (título, descrição, arquivo)
- Playlists (com relação muitos-para-muitos com vídeos)

---

## 🚀 Funcionalidades

- Upload de vídeos via formulário
- Reprodução de vídeos na interface
- Criação e edição de playlists personalizadas
- Busca por vídeos e playlists
- Autenticação de usuários com senha criptografada
- Layout responsivo e agradável com TailwindCSS
- Integração com API do YouTube
