from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from app.config.database import Base
from pydantic import BaseModel, ConfigDict, model_validator
from typing import Optional, List
from datetime import date

class Supermercado(Base):
    __tablename__ = "supermercados"
    
    id_Supermercado = Column(Integer, primary_key=True, index=True)
    nome_supermercado = Column(String(100), nullable=False)
    endereco = Column(String(200))
   #latitude = Column(Float)  # Para geolocalização
    #longitude = Column(Float) # Para geolocalização
    raio_entrega_km = Column(Float, default=5.0)
    produtos = relationship("Produto", back_populates="supermercado")
    

class CriaSupermercado(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True,from_attributes=True)
    #latitude: float
    #longitude: float
    nome_supermercado: str
    endereco: str
    raio_entrega_km: float
 
    

class ProdutoSimplificado(BaseModel):
    id_Produto: int
    nome_Produto: str
    preco: float
    validade_Produto: date
    desconto_Produto: float | None = None
    id_Supermercado: int | None = None

    class Config:
        from_attributes = True
        
class RespostaSupermercado(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, from_attributes=True)
  
    id_Supermercado: int
    raio_entrega_km: float 
    nome_supermercado: str 
    endereco: str 
    produtos: List[ProdutoSimplificado] = []
    
    @model_validator(mode = 'before')
    def adiciona_produtos_a_supermercado(cls, values):
        if hasattr(values, 'produtos'):
            if values.produtos is not None:
             values.produtos = sorted(values.produtos, key= lambda p: p.nome_Produto)
            
        return values


