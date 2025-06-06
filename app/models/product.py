from sqlalchemy import Column, Integer, String, Float, Date
from app.config.database import Base
from pydantic import BaseModel, ConfigDict
from datetime import date

#herda a Base da config.database
class Produto(Base):
  #nomeia a tabela
  __tablename__ = "Produtos"
  
  #nomeia as colunas
  id_Produto = Column(Integer, primary_key=True, index = True)
  nome_Produto = Column(String(100), nullable = False)
  preco = Column(Float, nullable = False)
  validade_Produto = Column(Date, nullable = False)
  desconto_Produto = Column(Float)
  id_Supermercado = Column(Integer)
  

#modelo de "criação" de um produto (valida as entradas de dados)  
class CriaProduto(BaseModel):
  model_config =   model_config = ConfigDict(arbitrary_types_allowed=True)
  
  nome_Produto: str
  preco: float
  validade_Produto: date
  id_Supermercado: int



#modelo para resposta da API ()  
class RespostaProduto(BaseModel):
  model_config =     model_config = ConfigDict(
        arbitrary_types_allowed=True,
        from_attributes=True
    )
  
  id_Produto: int
  nome_Produto: str
  preco: float
  validade_Produto: date
  desconto_Produto: float | None
  id_Supermercado: int
  
  

  