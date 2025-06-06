from fastapi import FastAPI
from app.models.product import Produto
from app.config.database import engine 
from app.routes.products import router as rotas_produtos
from app.routes.users import router as rotas_usuarios
from dotenv import load_dotenv

load_dotenv()


app = FastAPI()

app.include_router(rotas_produtos)
app.include_router(rotas_usuarios)

@app.get("/")
def read_root():
  return {"mensagem": "API de produtos próximos à validade"}

Produto.metadata.create_all(bind=engine)