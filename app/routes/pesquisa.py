from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from datetime import date, timedelta
from app.models.product import Produto
from app.config.database import get_db
from app.models.pesquisa import ResultadoPesquisa, ResultadoProduto, ResultadoSupermercado
from app.models.supermercado import Supermercado


router = APIRouter(prefix="/pesquisa", tags=["pesquisa"])

@router.get("/", response_model=ResultadoPesquisa)
def menu_pesquisa(
    nome_produto: Optional[str] = None,
    dias_validade: Optional[int] = 7,
    id_supermercado: Optional[int] = None,
    raio_km: Optional[float] = 5.0,
    db: Session = Depends(get_db)
):
    # 1. Busca produtos
    query_produtos = db.query(Produto)
    
    if nome_produto:
        query_produtos = query_produtos.filter(Produto.nome_Produto.ilike(f"%{nome_produto}%"))
    
    if dias_validade:
        data_limite = date.today() + timedelta(days=dias_validade)
        query_produtos = query_produtos.filter(Produto.validade_Produto <= data_limite)
    
    if id_supermercado:
        query_produtos = query_produtos.filter(Produto.id_Supermercado == id_supermercado)
    
    produtos = query_produtos.order_by(Produto.desconto_Produto.desc()).limit(50).all()
    
    # 2. Busca supermercados (exemplo simplificado)
    query_supermercados = db.query(Supermercado)
    
    if raio_km:
    #    # Aqui você implementaria a lógica de geolocalização real
        supermercados = query_supermercados.limit(5).all()
    else:
        supermercados = query_supermercados.all()
    
    # 3. Formata resposta
    return {
        "produtos": [
            {
                "id_produto": p.id_Produto,
                "nome": p.nome_Produto,
                "preco_original": p.preco,
                "preco_com_desconto": p.desconto_Produto or p.preco,
                "validade": p.validade_Produto,
                "supermercado": {
                    "id_supermercado": p.supermercado.id_Supermercado,
                    "nome": p.supermercado.nome,
                    "endereco": p.supermercado.endereco
                }
            } for p in produtos
        ],
        "supermercados_proximos": [
            {
                "id_supermercado": s.id_Supermercado,
                "nome": s.nome,
                "endereco": s.endereco
            } for s in supermercados
        ]
    }