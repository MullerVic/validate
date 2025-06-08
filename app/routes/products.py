from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from app.models.product import Produto, CriaProduto, RespostaProduto, FiltroBusca, SupermercadoSimples
from app.config.database import get_db
from datetime import date, timedelta
from app.models.supermercado import Supermercado

router = APIRouter(prefix="/produtos", tags=["produtos"])

    
#post produto
@router.post("/", response_model=RespostaProduto)
async def cria_produto(produto: CriaProduto, db: Session = Depends(get_db)):
  
  try:
    
    #verificando a existencia de um supermercado    
    supermercado = db.query(Supermercado).filter(Supermercado.id_Supermercado == produto.id_Supermercado).first()
        
    if not supermercado:
      raise HTTPException(status_code=422,detail="Supermercado não encontrado")
    
    #cria um objeto Produto (no sqlalchemy) com os dados recebidos
    db_produto = Produto(
      nome_Produto= produto.nome_Produto,
      preco = produto.preco,
      validade_Produto = produto.validade_Produto,
      id_Supermercado=produto.id_Supermercado,
      desconto_Produto = produto.preco *0.7,
      )
    db.add(db_produto) #adiciona ao banco
    db.commit() #confirma a operação
    db.refresh(db_produto) #atualiza o objeto com os dados do banco (ex:ID)
    
   
    return RespostaProduto(
      id_Produto=db_produto.id_Produto,
      nome_Produto=db_produto.nome_Produto,
      preco=db_produto.preco,
      validade_Produto=db_produto.validade_Produto,
      id_Supermercado=db_produto.id_Supermercado,
      desconto_Produto=db_produto.desconto_Produto,
      supermercado = SupermercadoSimples(
        id_Supermercado=db_produto.supermercado.id_Supermercado,
        nome_supermercado=db_produto.supermercado.nome_supermercado
      ) if db_produto.supermercado else None
    )
          
  except Exception as e:
      db.rollback()
      raise HTTPException(status_code=500, detail=f"Erro ao criar produto: {str(e)}")
    
#@router.get("/busca", response_model=list[RespostaProduto])
#async def buscar_produtos(
#    nome: str | None = None,
#    preco_min: float | None = None,
#    preco_max: float | None = None,
#    dias_validade: int | None = None,
#    id_supermercado: int | None = None,
#    db: Session = Depends(get_db)
#):
#    try:
   
#      query = db.query(Produto)
        
      # Filtros
#      if nome:
#            query = query.filter(Produto.nome_Produto.ilike(f"%{nome}%"))
#      if preco_min:
#            query = query.filter(Produto.preco >= preco_min)
#      if preco_max:
#            query = query.filter(Produto.preco <= preco_max)
#      if dias_validade:
#            data_limite = date.today() + timedelta(days=dias_validade)
#            query = query.filter(Produto.validade_Produto <= data_limite)
#      if id_supermercado:
#            query = query.filter(Produto.id_Supermercado == id_supermercado)
#        
#      produtos = query.order_by(Produto.validade_Produto).all()
#        
#      if not produtos:
#           return []
#           
#     return RespostaProduto.model_validate(produtos)
#        
 #   except Exception as e:
 #       raise HTTPException(
 #           status_code=500,
 #           detail=f"Erro ao buscar produtos: {str(e)}"
 #       )


#get produto
@router.get("/{id_Produto}", response_model=RespostaProduto)
async def ler_produto(id_Produto: int, db: Session = Depends(get_db)):
  try:
    #busca o produto pelo id

   db_produto = db.query(Produto).options(joinedload(Produto.supermercado)).filter(Produto.id_Produto == id_Produto).first()

    
    #se não existir, retorna um erro
   if not db_produto:
       raise HTTPException(status_code=404, detail=f"Produto com o ID {id_Produto}não encontrado")
   produto_dict = {
      "id_Produto": db_produto.id_Produto,
      "nome_Produto": db_produto.nome_Produto,
      "preco": db_produto.preco,
      "validade_Produto": db_produto.validade_Produto,
      "id_Supermercado": db_produto.id_Supermercado,
      "desconto_Produto": db_produto.desconto_Produto,
      "supermercado": {
        "id_Supermercado": db_produto.supermercado.id_Supermercado,
        "nome_supermercado": db_produto.supermercado.nome_supermercado
    } if db_produto.supermercado else None
}
    #retorna o produto, convertido para o RespostaProduto
   
   return RespostaProduto(**produto_dict) 
 
  except Exception as e:
    raise HTTPException(status_code=500, detail=f"Erro ao buscar produto: {str(e)}")  

#update produto
@router.put("/{id_Produto}", response_model=RespostaProduto)
async def atualiza_produto(id_Produto: int, data_produto: CriaProduto, db: Session = Depends(get_db)):
  #busca o produto existente
  db_produto = db.query(Produto).filter(Produto.id_Produto == id_Produto).first()
  if not db_produto:
    raise HTTPException(status_code=404, detail="Produto não encontrado")
  
  #atualiza apenas os campos permitidos
  db_produto.nome_Produto = data_produto.nome_Produto
  db_produto.preco = data_produto.preco
  db_produto.validade_Produto = data_produto.validade_Produto
  db_produto.id_Supermercado = data_produto.id_Supermercado
    
  #recalcula o desconto
  db_produto.desconto_Produto = db_produto.preco * 0.5 if db_produto.preco else None
  
  #confirma operação
  db.commit()
  #atualiza o banco
  db.refresh(db_produto)
  
  return db_produto

#delete produto
@router.delete("/{id_Produto}")
async def deleta_produto(id_Produto: int, db: Session = Depends(get_db)):
  #try:
    produto = db.query(Produto).filter(Produto.id_Produto == id_Produto).first()
    if not produto: 
      raise HTTPException(status_code=404, detail="Produto com não encontrado")
    
    db.delete(produto)
    db.commit()

    return {"message": "Produto deletado com sucesso"}
  