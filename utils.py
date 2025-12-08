from http import HTTPStatus
from fastapi import FastAPI, HTTPException, Depends
from schema import Create_Receita, Receita, Usuario
from models import User
from sqlalchemy import select
from sqlalchemy.orm import Session
from database import get_session
import re
import main
import schema
from sqlalchemy.exc import IntegrityError


# Funções do Back-End

def hello():
    return {"título": "Livro de Receitas"}

def get_todas_receitas(receitas):
    if len(receitas) == 0:
        return {"mensagem": "Não há receitas criadas"}
    return receitas

def get_receita_por_nome(receitas, nome_receita: str):
    for receita in receitas:
        if receita.nome.lower() == nome_receita.lower():
            return receita
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Receita não encontrada")

def get_receita(receitas, id: int):
    for receita in receitas:
        if receita.id == id:
            return receita
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Receita não encontrada")

def create_receita(receitas, id_receita,  dados: Create_Receita):
    for receita in receitas:
        if receita.nome.lower() == dados.nome.lower():
            raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="Receita já existe")

    if not (1 <= len(dados.ingredientes) <= 20):
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="A receita deve ter entre 1 e 20 ingredientes")
    
    if not (2 <= len(dados.nome) <= 50):
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="O nome da receita deve ter entre 2 e 50 caracteres")
    
    id_receita += 1
    nova_receita = Receita(
        id = id_receita,
        nome = dados.nome,
        ingredientes = dados.ingredientes,
        modo_de_preparo = dados.modo_de_preparo
    )
    receitas.append(nova_receita)
    return nova_receita

def update_receita(receitas, id: int, dados: Create_Receita):
    for i in range(len(receitas)):
        if receitas[i].id == id:
            for receita in receitas:
                if receita.nome.lower() == dados.nome.lower():
                    raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="Receita já existe")

                
                if receita.nome == "":
                    raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail= "O campo de nome não pode estar vazio")

            if not (1 <= len(dados.ingredientes) <= 20):
                raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail= "A receita deve ter entre 1 e 20 ingredientes")

            if not (2 <= len(dados.nome) <= 50):
                raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail= "O nome da receita deve ter entre 2 e 50 caracteres")

    
            receita_atualizada = Receita(
                id = id,
                nome = dados.nome,
                ingredientes = dados.ingredientes,
                modo_de_preparo = dados.modo_de_preparo
            )
            receitas[i] = receita_atualizada
            return receita_atualizada

    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Receita não encontrada")

def deletar_receita(receitas, id: int):
    if len(receitas) == 0:
         raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="A lista está vazia, não há receitas para excluir")
         
    for i in range(len(receitas)):
        if receitas[i].id == id:
            receita_removida = receitas.pop(i)
            return {"mensagem": f"A receita {receita_removida.nome} foi deletada"}
        
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Receita não encontrada")

# Funções de Usuário

def create_usuario(dados: schema.BaseUsuario, session: Session = Depends(get_session)):
    db_user = session.scalar(select(User).where((User.nome_usuario == dados.nome_usuario) | (User.email == dados.email)))

    if db_user:
        if db_user.nome_usuario == dados.nome_usuario:
            raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="Nome de usuário já existe",)
        elif db_user.email == dados.email:
            raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="Email já existe",)

    db_user = User(
        nome_ususario=dados.nome_usuario, senha=dados.senha, email=dados.email
    )
    session.add(db_user)
    session.commit()
    sesion.refresh(db_user)

    return db_user

    '''for usuario in main.usuarios:
        if usuario.email == dados.email:
            raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="Este email já existe")
    
    if not(re.search(r'[A-Za-z]', dados.senha)) and not(re.search(r'\d', dados.senha)):
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail= "A senha deve conter números e letras")
        
    novo_user = schema.Usuario(
        id = id_user,
        nome_usuario = dados.nome_usuario,
        email = dados.email,
        senha = dados.senha
    )
    main.usuarios.append(novo_user)
    return novo_user'''

def get_todos_usuarios(skip: int = 0, limit: int = 100, session: Session = Depends(get_session)):
    users = session.scalars(select(User).offset(skip).limit(limit)).all()

    return users

    '''if len(main.usuarios) == 0:
        return {"mensagem": "Não há usuários cadastrados"}
    return main.usuarios'''

def get_usuarios_por_nome(nome_usuario: str, sessio: Session = Depends(get_session)):
    db_user = session.scalar(
        select(User).where((User.nome_usuario == nome_usuario))
    )
    if db_user:
        return db_user

    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Usuário não encontrado")

    '''for usuario in main.usuarios:
        if usuario.nome_usuario == nome_usuario:
            return usuario
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Usuário não encontrado")'''

def get_usuarios_por_id(id: int, session: Session = Depends(get_session)):
    db_user = session.scalar(
        select(User).where((User.id == id))
    )
    if db_user:
        return db_user
    
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Usuário não encontrado")
        
    '''for usuario in main.usuarios:
        if usuario.id == id:
            return usuario
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Usuário não encontrado")'''

def update_usuario(id: int, dados: schema.BaseUsuario, session: Session = Depends(get_session)):

    db_user = session.scalar(select(User).where(User.id == id))
    if not db_user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Usuário não encontrado")
    
    try:
        db_user.nome_usuario = dados.nome_usuario
        db_user.senha = dados.senha
        db_user.email = dados.email
        session.commit()
        sesion.refresh(db_user)

        return db_user

    except IntegrityError:
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="Nome de usuário ou Email já existe")

    '''for i in main.usuarios:
        if i.email == dados.email:
            raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="Este email já existe")
        
        if not(re.search(r'[A-Za-z]', dados.senha)) and not(re.search(r'\d', dados.senha)):
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail= "A senha deve conter números e letras")

    usuario_atualizado = main.Usuario(
        id = id,
        nome_usuario = dados.nome_usuario,
        email = dados.email,
        senha = dados.senha
        )
    main.usuarios[i] = usuario_atualizado
    return usuario_atualizado'''

def delete_usuario(id: int, session: Session = Depends(get_session)):
    db_user = session.scalar(select(User).where(User.id == id))

    if not db_user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Usuário não encontrado")
    

    session.delete(db_user)
    session.commit()

    return db_user

    '''if len(main.usuarios) == 0:
         raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="A lista está vazia, não há usuários cadastrados")
         
    for i in range(len(main.usuarios)):
        if main.usuarios[i].id == id:
            usuario_removido = main.usuarios.pop(i)
            return {"mensagem": f"O usuário {usuario_removido.nome} foi deletado"}
        
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Usuário não encontrado")'''