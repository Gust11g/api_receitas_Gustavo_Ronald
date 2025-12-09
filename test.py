from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from models import User, table_registry

app = FastAPI(title="Livro de Receitas")

engine = create_engine("sqlite:///:memory:", echo=False)

table_registry.metadata.create_all(engine)

with Session(engine) as session:
    Neymar = User(
        nome_usuario="Neymar", 
        senha="Neymar.xp", 
        email="Neymar100@gmail.com"
    )
    session.add(Neymar)
    session.commit()
    session.refresh(Neymar)

print(f"DADOS DO USUÁRIO: {Neymar}")
print(f"ID: {Neymar.id}")
print(f"Criado em: {Neymar.created_at}")
