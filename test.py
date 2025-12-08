from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models import User, table_registry

app = FastAPI(title="Livro de Receitas")

engine = create_engine("sqlite:///:memory:", echo=False)

table_registry.metadata.create_all(engine)

with Session(engine) as session:
    maneu = User(
        nome_usuario="maneu", 
        senha="maneu.xp", 
        email="maneudapop100@gmail.com"
    )
    session.add(maneu)
    session.commit()
    session.refresh(maneu)

print(f"DADOS DO USUÁRIO: {maneu}")
print(f"ID: {maneu.id}")
print(f"Criado em: {maneu.created_at}")
