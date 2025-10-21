from pydantic import BaseModel
from typing import List
from http import HTTPStatus

app = FastAPI(title="Livro de Receitas")

class CreateReceita(BaseModel):
    nome: str
    ingredientes: List[str]
    modo_de_preparo: str

class Receita(BaseModel):
    id: int
    nome: str
    ingredientes: List[str]
    modo_de_preparo: str
