from pydantic import BaseModel
from typing import List

class Receita(BaseModel):
    id: int
    nome: str
    ingredientes: List[str]
    modo_de_preparo: str

class Create_Receita(BaseModel):
    nome: str
    ingredientes: List[str]  # lista normal
    modo_de_preparo: str

class Usuario(BaseModel):
    id: int
    nome_usuario: str
    email: str
    senha: str

class BaseUsuario(BaseModel):
    nome_usuario: str
    email: str
    senha: str

class UsuarioPublic(BaseModel):
    id:int
    nome_usuario:str
    email:str
    

