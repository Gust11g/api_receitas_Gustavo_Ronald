from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Livro de Receitas")

class Receita(BaseModel):
    id: int
    nome: str
    ingredientes: List[str]
    modo_d_preparo: str

receitas: List[Receita] = []

@app.get("/")
def hello():
    return {"título": "Livro de Receitas"}

@app.get("/receitas/")
def listar_receitas():
    return receitas

@app.get("/receitas/{id}")
def buscar_receita(id: int):
    for r in receitas: 
        if r.id == id:
            return r
    raise HTTPException(status_code=404, detail="Receita não encontrada")

@app.post("/receitas", response_model=Receita, status_code=201)
def criar_receita(dados: Receita):
    for r in receitas:
        if r.nome.lower() == dados.nome.lower():
            raise HTTPException(status_code=400, detail="Já existe uma receita com esse nome.")
    receitas.append(dados)
    return dados
