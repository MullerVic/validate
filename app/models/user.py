from sqlalchemy import Column, Integer, String,  Boolean
from app.config.database import Base
from pydantic import BaseModel, ConfigDict


class Usuario(Base):
    __tablename__ = "Usuario"
    
    id_usuario = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    senha = Column(String(100), nullable=False)  # Armazenaremos o hash
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    
class CriaUsuario(BaseModel):
  model_config = ConfigDict(arbitrary_types_allowed=True)
  
  nome: str
  email: str
  senha: str
  is_admin: bool = False
  
class RespostaUsuario(BaseModel):
  model_config = ConfigDict(from_attributes=True,arbitrary_types_allowed=True)
  
  id_usuario:int
  nome: str
  email: str
  is_active: bool | None
  is_admin: bool | None
  
class AtualizaUsuario(BaseModel):
  model_config = ConfigDict(arbitrary_types_allowed=True, from_attributes=True)
  
  nome: str | None = None
  email: str
  senha: str | None = None
  is_admin: bool | None = None

  