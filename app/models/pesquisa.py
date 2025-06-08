from pydantic import BaseModel
from datetime import date

class ResultadoSupermercado(BaseModel):
    id_supermercado: int
    nome: str
    endereco: str | None
    distancia_km: float | None = None

class ResultadoProduto(BaseModel):
    id_produto: int
    nome: str
    preco_original: float
    preco_com_desconto: float
    validade: date
    supermercado: ResultadoSupermercado

class ResultadoPesquisa(BaseModel):
    produtos: list[ResultadoProduto]
    supermercados_proximos: list[ResultadoSupermercado] | None