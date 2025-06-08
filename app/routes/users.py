from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.user import Usuario, CriaUsuario, RespostaUsuario, AtualizaUsuario
from app.config.database import get_db
#from bcrypt import bcrypt


router = APIRouter(prefix="/usuario", tags=["usuario"])

#criptografa a senha
#def hash_password(senha: str) -> str:
 # salt = bcrypt.gensalt()
#  return bcrypt.hashpw(senha.encode(),salt).decode()


#cria usuario
@router.post("/", response_model=RespostaUsuario)
def cria_usuario(usuario: CriaUsuario, db: Session = Depends(get_db)):
  try:    #hash/criptografia da senha
   # hashed_password = hash_password(usuario.senha)
    
    required_fields = ['nome', 'email', 'senha']
    for fields in required_fields:
      if not hasattr(usuario, fields):
        raise HTTPException(status_code=500,detail=f"Campo obrigatório faltando: {fields}")
    db_usuario = Usuario(
      nome = usuario.nome,
      email = usuario.email,
      senha = usuario.senha,
      is_admin = usuario.is_admin
      )
    
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    
    return  RespostaUsuario.model_validate(db_usuario)

  except Exception as e:
    raise HTTPException(status_code=500, detail=f"Erro ao criar usuario {str(e)}")
  
#busca usuario
@router.get("/{id_usuario}", response_model= RespostaUsuario)
def ler_usuario(id_usuario: int, db: Session = Depends(get_db)):
  
  try:
    usuario = db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
    return usuario
  
  except Exception as e:
    raise HTTPException(status_code=500, detail=f"Usuario não encontrado")  

#atualiza usuario
@router.put("/{id_usuario}", response_model=RespostaUsuario)
def atualiza_usuario(id_usuario: int, data_usuario: AtualizaUsuario, db: Session = Depends(get_db)):
  db_usuario = db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
  if not db_usuario:
    raise HTTPException(status_code=500, detail="Usuário não encontrado")
  
  #modifica apenas os dados que o usuario quiser/campos que o usuario fornece

  db_usuario.nome = data_usuario.nome
  db_usuario.email = data_usuario.email
  db_usuario.senha = data_usuario.senha
  
  db.commit()
  db.refresh(db_usuario)
    
  return db_usuario

#deleta usuario
@router.delete("/{id_usuario}")
def deleta_usuario(id_usuario: int,db: Session = Depends(get_db)):
  usuario = db.query(Usuario).filter(Usuario.id_usuario == id_usuario).first()
  if not usuario:
    raise HTTPException(status_code=500, detail="Usuário não encontrado")
  
  db.delete(usuario)
  db.commit()
  
  return {"message: Usuario deletado com sucesso" }
  