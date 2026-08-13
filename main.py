from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

import schema
import utils
from auth import (create_token_pair, decode_token, find_user_by_email, get_current_user,
                  hash_password, verify_password)
from database import get_session
from models import User
from settings import settings

app = FastAPI(title="Livro de Receitas", version="2.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

receitas: list[schema.Receita] = []
id_receita = 0


@app.get("/")
def hello():
    return {"mensagem": "API Livro de Receitas online", "docs": "/docs"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/auth/jwt/create/", response_model=schema.TokenPair)
def login(dados: schema.LoginRequest, session: Session = Depends(get_session)):
    user = find_user_by_email(session, str(dados.email).lower())
    if not user or not user.is_active or not verify_password(dados.password, user.senha):
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Email ou senha inválidos")
    return create_token_pair(user.id)


@app.post("/auth/jwt/refresh/", response_model=schema.TokenPair)
def refresh(dados: schema.RefreshRequest, session: Session = Depends(get_session)):
    payload = decode_token(dados.refresh, "refresh")
    user = session.get(User, int(payload["sub"]))
    if not user or not user.is_active:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail="Usuário inválido ou inativo")
    return create_token_pair(user.id)


@app.post("/auth/jwt/verify/")
def verify(dados: schema.VerifyTokenRequest):
    decode_token(dados.token)
    return {"detail": "Token válido"}


@app.post("/auth/users/", response_model=schema.UsuarioPublic, status_code=HTTPStatus.CREATED)
@app.post("/usuarios", response_model=schema.UsuarioPublic, status_code=HTTPStatus.CREATED)
def create_usuario(dados: schema.UserRegister | schema.BaseUsuario, session: Session = Depends(get_session)):
    email = str(dados.email).lower()
    nome = dados.nome_usuario or email.split("@")[0]
    password = getattr(dados, "password", None) or dados.senha
    if find_user_by_email(session, email) or session.scalar(select(User).where(User.nome_usuario == nome)):
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="Nome de usuário ou email já existe")
    user = User(nome_usuario=nome, senha=hash_password(password), email=email,
                first_name=dados.first_name, last_name=dados.last_name, is_active=True)
    session.add(user)
    try:
        session.commit()
        session.refresh(user)
    except IntegrityError as exc:
        session.rollback()
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="Nome de usuário ou email já existe") from exc
    return user


@app.get("/auth/users/me/", response_model=schema.UsuarioPublic)
def get_me(user: User = Depends(get_current_user)):
    return user


@app.patch("/auth/users/me/", response_model=schema.UsuarioPublic)
def update_me(dados: schema.ProfileUpdate, user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    if dados.email is not None:
        existing = find_user_by_email(session, str(dados.email).lower())
        if existing and existing.id != user.id:
            raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="Email já existe")
        user.email = str(dados.email).lower()
    if dados.first_name is not None:
        user.first_name = dados.first_name
    if dados.last_name is not None:
        user.last_name = dados.last_name
    session.commit()
    session.refresh(user)
    return user


@app.get("/receitas", response_model=list[schema.Receita])
def get_todas_receitas():
    return utils.get_todas_receitas(receitas)


@app.get("/receitas/{nome_receita}", response_model=schema.Receita)
def get_receita_por_nome(nome_receita: str):
    return utils.get_receita_por_nome(receitas, nome_receita)


@app.get("/receitas/id/{id}", response_model=schema.Receita)
def get_receita(id: int):
    return utils.get_receita(receitas, id)


@app.post("/receitas", response_model=schema.Receita, status_code=HTTPStatus.CREATED)
def create_receita(dados: schema.Create_Receita, _: User = Depends(get_current_user)):
    global id_receita
    id_receita += 1
    return utils.create_receita(receitas, id_receita, dados)


@app.put("/receitas/{id}", response_model=schema.Receita)
def update_receita(id: int, dados: schema.Create_Receita, _: User = Depends(get_current_user)):
    return utils.update_receita(receitas, id, dados)


@app.delete("/receitas/{id}", response_model=schema.Receita)
def deletar_receita(id: int, _: User = Depends(get_current_user)):
    return utils.deletar_receita(receitas, id)


@app.get("/usuarios", response_model=list[schema.UsuarioPublic])
def get_todos_usuarios(session: Session = Depends(get_session), _: User = Depends(get_current_user)):
    return session.scalars(select(User)).all()


@app.get("/usuarios/{id}", response_model=schema.UsuarioPublic)
def get_usuario(id: int, session: Session = Depends(get_session), _: User = Depends(get_current_user)):
    user = session.get(User, id)
    if not user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Usuário não encontrado")
    return user
