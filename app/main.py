from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.search_routes import router as search_router
from app.database.connection import Base, engine

# 👇 IMPORTANTE: importar models para registrar no metadata
from app.models.product import Product
from app.models.subcategory import SubCategory
from app.models.category import Category
from app.models.search import Search  # caso exista

app = FastAPI(title="E-commerce API")

# --- Configuração CORS ---
origins = [
    "http://localhost:3000",  # front local
    "http://127.0.0.1:3000",
    "https://nexorashopx.vercel.app"   # produção
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Inicializar banco de dados ---
async def init_db():
    async with engine.begin() as conn:
        # Cria todas as tabelas registradas no metadata
        await conn.run_sync(Base.metadata.create_all)

@app.on_event("startup")
async def startup():
    await init_db()

# --- Rotas ---
app.include_router(search_router)