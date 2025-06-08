from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from app.models.product import RespostaProduto
from app.models.supermercado import Supermercado, CriaSupermercado, RespostaSupermercado
from app.config.database import get_db
from typing import Optional

router = APIRouter(prefix="/supermercados", tags=["supermercados"])

#post supermercado
@router.post("/", response_model=RespostaSupermercado)
def cria_supermercado(supermercado: CriaSupermercado,db:Session = Depends(get_db)):
  
  try:
    
    required_fields = ['nome_supermercado', 'endereco', 'raio_entrega_km']
    for field in required_fields:
      if not hasattr(supermercado,field):
        raise HTTPException(status_code=422,detail=f"Fampo obrigatório faltando: {str(field)}")
      
    db_supermercado = Supermercado(
      nome_supermercado = supermercado.nome_supermercado,
      endereco = supermercado.endereco,
      raio_entrega_km = supermercado.raio_entrega_km
    )
  
    db.add(db_supermercado)
    db.commit()
    db.refresh(db_supermercado)
  
    return RespostaSupermercado.model_validate(db_supermercado)
    
  except Exception as e:
    db.rollback()
    raise HTTPException(status_code=500, detail=f"Erro ao criar supermercado {str(e)}")
  
#busca supermercado
@router.get("/busca", response_model=list[RespostaSupermercado])
def buscar_supermercados(
    raio_entrega_km: float | None = Query(None, description = "Filtro por raio de entrega em km"),
    nome_supermercado: str | None = None,
    endereco: str = None,
    db: Session = Depends(get_db)):
  try:
    query = db.query(Supermercado)
    
    #filtros
    if nome_supermercado:
      query = query.filter(Supermercado.nome_supermercado.ilike(f"%{nome_supermercado}"))
    if endereco:
      query = query.filter(Supermercado.endereco.ilike(f"%{endereco}"))
    if raio_entrega_km is not None:
      query = query.filter(Supermercado.raio_entrega_km <= raio_entrega_km)
    
    supermercados = query.order_by(Supermercado.nome_supermercado).all()
    
    return supermercados if supermercados else []
    
  except Exception as e:
    raise HTTPException(status_code=500, detail=f"Erro ao buscar supermercados: {str(e)}") 

#mostra os produtos de um supermercado especifico
@router.get("/{id_Supermercado}/produtos", response_model=list[RespostaProduto])
def listar_produtos_supermercado(
  id_Supermercado: int,
  db: Session = Depends(get_db)
):
  
  supermercado = db.query(Supermercado).options(joinedload(Supermercado.produtos)).filter(Supermercado.id_Supermercado == id_Supermercado).first()
  if not supermercado:
    raise HTTPException(status_code=404, detail="Supermercado não encontrado!")
  
  return supermercado.produtos

#atualiza supermercados
@router.put("/{id_Supermercado}", response_model=RespostaSupermercado)
def atualiza_supermercado(id_Supermercado: int, nome_supermercado: Optional[str] = Query(
                          None, 
                          description="Novo nome", example="Supermercado ABC",
                          min_length=3, max_length=100
                          ),
                          endereco: Optional[str] = Query(
                          None,
                          description="Novo endereço",
                          example="Rua dos dinossauros",
                          min_length=5
                          ),
                          raio_entrega_km: Optional[float] = Query(
                          None,
                          description="Novo raio de entrega em Kms",
                          example=5.0,
                          gt=0
                          ),
                          db: Session = Depends(get_db)
):
  
  
  try:
    db_supermercado = db.query(Supermercado).filter(Supermercado.id_Supermercado == id_Supermercado).first()
    if not db_supermercado:
      raise HTTPException(status_code=404, detail="Supermercado não encontrado")
    
    if nome_supermercado is not None:
      db_supermercado.nome_supermercado = nome_supermercado
      
    if endereco is not None:
      db_supermercado.endereco = endereco
    
    if raio_entrega_km is not None:
      db_supermercado.raio_entrega_km = raio_entrega_km
    
    db.commit()
    
    db.refresh(db_supermercado)
    
    return RespostaSupermercado.model_validate(db_supermercado)
  
  except Exception as e:
    db.rollback()
    raise HTTPException(status_code=500, detail =f"Erro ao atualizar supermercado: {str(e)}")

#deleta supermercado
@router.delete("/{id_Supermercado}")
def deleta_supermercado(id_Supermercado: int, db: Session = Depends(get_db)):
  
  try:
    supermercado = db.query(Supermercado).filter(Supermercado.id_Supermercado == id_Supermercado).first() 
    if not supermercado:
      raise HTTPException(status_code=404, detail="Supermercado não encontrado")
    
    db.delete(supermercado)
    db.commit()
    
    return {"message": "Supermercado deletado com sucesso!"}
  
  except Exception as e:
    db.rollback()
    raise HTTPException(status_code=500, detail=f"Erro ao deletar supermercado {str(e)}")
  
