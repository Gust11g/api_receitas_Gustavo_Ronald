from fastapi import FastAPI, HTTPException
from schema import CreateReceita, Receita

receitas: List[Receita] = []
proximo_id = 1 

@app.get("/")
def hello():
    return {"título": "Livro de Receitas"}

@app.get("/receitas/")
def listar_receitas():
    return receitas

@app.get("/receitas/id/{id}")
def buscar_receita_por_id(id: int):
    for r in receitas: 
        if r.id == id:
            return r
    raise HTTPException(status_code=404, detail="Receita não encontrada")

@app.get("/receitas/nome/{nome}")
def buscar_receita_por_nome(nome: str):
    for r in receitas:
        if r.nome.lower() == nome.lower():
            return r
    raise HTTPException(status_code=404, detail="Receita não encontrada")

@app.post("/receitas")
def criar_receita(dados: CreateReceita):
    global proximo_id

    for r in receitas:
        if r.nome.lower() == dados.nome.lower():
            raise HTTPException(status_code=400, detail="Já existe uma receita com esse nome.")
    nova_receita =Receita(id = proximo_id , nome = dados.nome, ingredientes = dados.ingredientes, modo_de_preparo = dados.modo_de_preparo)
    receitas.append(nova_receita)
    proximo_id += 1
    return nova_receita

@app.put("/receitas/{id}", response_model=Receita)
def update_receita(id: int, dados: CreateReceita):
    for i in range(len(receitas)):
        if receitas[i].id == id:
            # Verificar se o novo nome já existe em outra receita
            for j, r in enumerate(receitas):
                if j != i and r.nome.lower() == dados.nome.lower():
                    raise HTTPException(status_code=400, detail="Já existe uma receita com esse nome.")

            receita_atualizada = Receita(
                id= id,
                nome= dados.nome,
                ingredientes = dados.ingredientes,
                modo_de_preparo = dados.modo_de_preparo,
            )
            receitas[i] = receita_atualizada
            return receita_atualizada
    raise HTTPException(status_code=404, detail="Receita não encontrada")

@app.delete("/receitas/{id}")
def deletar_receita(id: int):
    if not receitas:
       raise HTTPException(status_code=404, detail="Não há receitas para excluir.")
     
    for i in range(len(receitas)):
        if receitas[i].id == id:
            receita_deletada = receitas.pop(i)
            return {"mensagem": "Receita deletada", "receita": receita_deletada}
    raise HTTPException(status_code=404, detail="Receita não encontrada")