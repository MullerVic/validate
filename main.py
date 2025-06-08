from fastapi import FastAPI
from app.models.product import Produto
from app.models.user import Usuario
from app.models.supermercado import Supermercado
from app.config.database import engine,Base
from app.routes.products import router as rotas_produtos
from app.routes.users import router as rotas_usuarios
from app.routes.supermercado import router as rotas_supermercado
from dotenv import load_dotenv

load_dotenv()


app = FastAPI()

app.include_router(rotas_produtos)
app.include_router(rotas_usuarios)
app.include_router(rotas_supermercado)

@app.get("/")
def read_root():
  return {"mensagem": "API de produtos próximos à validade"}

#Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)