from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Livro de Receitas")

class Receita(BaseModel):
    id: int
    nome: str
    ingredientes: List[str]
    modo_de_preparo: str

class CreateReceita(BaseModel):
    nome: str
    ingredientes: List[str]
    modo_de_preparo: str

receitas: List[Receita] = []

@app.get("/")
def hello():
    return {"título": "Livro de Receitas"}

@app.get("/receitas/")
def listar_receitas():
    return receitas

@app.get("/receitas/id/{id}")
def buscar_receita(id: int):
    for r in receitas: 
        if r.id == id:
            return r
    raise HTTPException(status_code=404, detail="Receita não encontrada")

@app.post("/receitas")
def criar_receita(dados: CreateReceita):
    for r in receitas:
        if r.nome.lower() == dados.nome.lower():
            raise HTTPException(status_code=400, detail="Já existe uma receita com esse nome.")
    nova_receita =Receita(id=, nome=dados.nome, ingredientes = dados.nome)
    receitas.append(dados)
    return dados

@app.put("/receitas/{id}", response_model=Receita)
def update_receita(id: int, dados: CreateReceita):
    for i in range(len(receitas)):
        if receitas[i].id == id:
            receita_atualizada = Receita(
                id=id,
                nome=dados.nome,
                ingredientes=dados.ingredientes,
                modo_de_preparo=dados.modo_de_preparo,
            )
            receitas[i] = receita_atualizada
            return receita_atualizada
    raise HTTPException(status_code=404, detail="Receita não encontrada")

