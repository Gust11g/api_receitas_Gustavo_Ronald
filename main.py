from http import HTTPStatus
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import schema
import utils

app = FastAPI(title="Livro de Receitas")

usuarios:List[Usuario] = []
receitas: List[Receita] = []

id_receita = 0
id_user = 0

#Back-End

@app.get("/")
def hello():
    return utils.hello()

@app.get("/receitas", response_model=List[Receita], status_code=HTTPStatus.OK)
def get_todas_receitas():
    return utils.get_todas_receitas(receitas)

@app.get("/receitas/{nome_receita}", response_model=Receita, status_code=HTTPStatus.OK)
def get_receita_por_nome(nome_receita: str):
    return utils.get_receita_por_nome(receitas, nome_receita)

@app.get("/receitas/id/{id}", response_model=Receita , status_code=HTTPStatus.OK)
def get_receita(id: int):
    return utils.get_receita(receitas, id)

@app.post("/receitas" , response_model=Receita, status_code=HTTPStatus.CREATED)
def create_receita(dados: Create_Receita):
    global id_receita
    id_receita += 1
    return utils.create_receita(receitas, id_receita, dados)

@app.put("/receitas/{id}" , response_model=Receita, status_code=HTTPStatus.OK)
def update_receita(id: int, dados: Create_Receita):
    return utils.update_receita(receitas, id, dados)

@app.delete("/receitas/{id}" , response_model=Receita , status_code=HTTPStatus.OK)
def deletar_receita(id: int):
    return utils.deletar_receita(receitas, id)

#Usuário

@app.post("/usuarios" , response_model=UsuarioPublic, status_code=HTTPStatus.CREATED)
def create_usuario(dados: BaseUsuario):
    for usuario in List[Usuario]:
        if usuario.email == dados.email:
             raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="Este email já existe")

@app.get("/Usuarios", status_code=HTTPStatus.OK, response_model=List[UsuarioPublic])
def get_todos_usuarios():

@app.get("/Usuarios/{nome_usuario}", status_code=HTTPStatus.OK, response_model=UsuarioPublic)
def get_usuarios_por_nome(nome_usuario:str):

@app.get("/Usuarios/{id}", status_code=HTTPStatus.OK, response_model=UsuarioPublic)
def get_usuarios_por_id(id:int):

@app.put("/usuarios/{id}", response_model=UsuarioPublic, status_code=HTTPStatus.OK)
def update_usuario(id: int, dados: BaseUsuario):

@app.delete("/usuarios/{id}", response_model=UsuarioPublic, status_code=HTTPStatus.OK)
def delete_usuario(id: int):


