from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.config.database import Base
from pydantic import BaseModel, ConfigDict, Field, model_validator
from datetime import date
from app.models.supermercado import Supermercado
from typing import Optional, Dict

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
  id_Supermercado = Column(Integer, ForeignKey("supermercados.id_Supermercado"))
  supermercado = relationship("Supermercado", back_populates="produtos")
  

#modelo de "criação" de um produto (valida as entradas de dados)  
class CriaProduto(BaseModel):
  model_config = ConfigDict(arbitrary_types_allowed=True)
  
  nome_Produto: str 
  preco: float
  validade_Produto: date
  id_Supermercado: int

class SupermercadoSimples(BaseModel):
  id_Supermercado: int
  nome_supermercado: str

#modelo para resposta da API ()  
class RespostaProduto(BaseModel):
  model_config = ConfigDict(
        arbitrary_types_allowed=True,
        from_attributes=True,
       )
  
  id_Produto: int
  nome_Produto: str
  preco: float
  validade_Produto: date
  desconto_Produto: float | None
  id_Supermercado: int
  supermercado: Optional[SupermercadoSimples] = None
 
  
class FiltroBusca(BaseModel):
    nome: str | None = None
    preco_min: float | None = None
    preco_max: float | None = None
    dias_validade: int | None = None
    id_supermercado: int | None = None

  