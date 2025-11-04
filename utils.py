from http import HTTPStatus
from fastapi import FastAPI, HTTPException
from schema import Create_Receita, Receita

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

def create_receita(receitas, id_receita, dados: Create_Receita):
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

    return {"mensagem": "Receita não encontrada"}

def deletar_receita(receitas, id: int):
    if len(receitas) == 0:
         raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="A lista está vazia, não há receitas para excluir")
         
    for i in range(len(receitas)):
        if receitas[i].id == id:
            receita_removida = receitas.pop(i)
            return {"mensagem": f"A receita {receita_removida.nome} foi deletada"}
        
    return {"mensagem": "Receita não encontrada"}