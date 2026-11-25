
import os
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from routes.auth import router as auth_router
from routes.contatos import router as contatos_router

app = FastAPI()

STATIC_DIR = Path(
    os.getenv("STATIC_DIR", Path(__file__).resolve().parent / "static")
).resolve()
INDEX_FILE = STATIC_DIR / "index.html"
RESERVED_PATHS = ("/docs", "/redoc", "/openapi.json", "/health")

# Configuração de acesso pelo Expo Web e origens extras via CORS_ORIGINS
default_origins = [
    "http://localhost:8081",
    "http://127.0.0.1:8081",
    "http://192.168.1.82:8081",
    "http://localhost:19006",
    "http://192.168.1.82:19006",
]
extra_origins = [
    o.strip() for o in os.getenv("CORS_ORIGINS", "").split(",") if o.strip()
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=default_origins + extra_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def spa_html_fallback(request: Request, call_next):
    """Serve o index.html do Expo Web quando o navegador acessa rotas da SPA."""
    if INDEX_FILE.is_file() and request.method == "GET":
        path = request.url.path
        accept = request.headers.get("accept", "")
        is_reserved = any(
            path == prefix or path.startswith(f"{prefix}/")
            for prefix in RESERVED_PATHS
        )
        if "text/html" in accept and not is_reserved:
            candidate = (STATIC_DIR / path.lstrip("/")).resolve()
            if not (candidate.is_relative_to(STATIC_DIR) and candidate.is_file()):
                return FileResponse(INDEX_FILE)
    return await call_next(request)


# Rotas da API
app.include_router(auth_router)
app.include_router(contatos_router)


@app.get("/health")
def health():
    return {"status": "ok", "mensagem": "API Alerta+ funcionando!"}


@app.get("/")
def inicio():
    if INDEX_FILE.is_file():
        return FileResponse(INDEX_FILE)
    return {"mensagem": "API Alerta+ funcionando!"}


if STATIC_DIR.is_dir():
    app.mount("/", StaticFiles(directory=STATIC_DIR), name="static")
