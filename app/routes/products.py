from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.product import Produto, CriaProduto, RespostaProduto
from app.config.database import get_db

router = APIRouter(prefix="/produtos", tags=["produtos"])

    
#post produto
@router.post("/", response_model=RespostaProduto)
def cria_produto(produto: CriaProduto, db: Session = Depends(get_db)):
  
  try:
   #calculando o desconto
    desconto = produto.preco * 0.7 
    
    # Verifique se todos os campos necessários estão presentes
    required_fields = ['nome_Produto', 'preco', 'validade_Produto', 'id_Supermercado']
    for field in required_fields:
        if not hasattr(produto, field):
            raise HTTPException(
                    status_code=422,
                    detail=f"Campo obrigatório faltando: {field}"
                )
  
    #cria um objeto Produto (no sqlalchemy) com os dados recebidos
    db_produto = Produto(
      nome_Produto= produto.nome_Produto,
      preco = produto.preco,
      validade_Produto = produto.validade_Produto,
      id_Supermercado=produto.id_Supermercado,
      desconto_Produto = desconto
    )
    db.add(db_produto) #adiciona ao banco
    db.commit() #confirma a operação
    db.refresh(db_produto) #atualiza o objeto com os dados do banco (ex:ID)
    return RespostaProduto.model_validate(db_produto)#RespostaProduto(
           # id_Produto=db_produto.id_Produto,
            #nome_Produto=db_produto.nome_Produto,
            #preco=db_produto.preco,
            #desconto_Produto=db_produto.desconto_Produto,
            #validade_Produto=db_produto.validade_Produto,
            #id_Supermercado=db_produto.id_Supermercado
        #) #retorna o produto criado (no formato RespostaProduto)
  except Exception as e:
      db.rollback()
      raise HTTPException(status_code=500, detail=f"Erro ao criar produto: {str(e)}")
    
#get produto
@router.get("/{id_Produto}", response_model=RespostaProduto)
def ler_produto(id_Produto: int, db: Session = Depends(get_db)):
  try:
    #busca o produto pelo id
    produto = db.query(Produto).filter(Produto.id_Produto == id_Produto).first()
    
    #se não existir, retorna um erro
    if not produto:
      raise HTTPException(status_code=404, detail="Produto com o ID {id_Produto}não encontrado")
    
    return RespostaProduto(
              id_Produto=produto.id_Produto,
              nome_Produto=produto.nome_Produto,
              preco=produto.preco,
              validade_Produto=produto.validade_Produto,
              desconto_Produto=produto.desconto_Produto,
              id_Supermercado=produto.id_Supermercado
          )#RespostaProduto.model_validate(produto) #retorna o produto, convertido para o RespostaProduto
  except Exception as e:
    raise HTTPException(status_code=500, detail=f"Erro ao buscar produto: {str(e)}")  

#update produto
@router.put("/{id_Produto}", response_model=RespostaProduto)
def atualiza_produto(id_Produto: int, data_produto: CriaProduto, db: Session = Depends(get_db)):
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
def deleta_produto(id_Produto: int, db: Session = Depends(get_db)):
  #try:
    produto = db.query(Produto).filter(Produto.id_Produto == id_Produto).first()
    if not produto: 
      raise HTTPException(status_code=404, detail="Produto com não encontrado")
    
    db.delete(produto)
    db.commit()
  #except Exception as e:
    #raise HTTPException(status_code=500, detail=f"Erro ao excluir produto: {str(e)}")
    return {"message": "Produto deletado com sucesso"}
  