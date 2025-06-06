from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()
#lê a url do banco no .env
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL não configurada no .env")

#cria um motor de conexão com o banco de dados
engine = create_engine(DATABASE_URL)

#configura uma fábriga de sessão, cada requisição criará uma nova
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#base para os modelos do sqlalchemy
Base = declarative_base()

# Função get_db para injetar a sessão nas rotas
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()