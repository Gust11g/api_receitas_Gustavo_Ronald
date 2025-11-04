import schema 
import utils

app = utils.FastAPI(title="Livro de Receitas")

usuarios: schema.List[schema.Usuario] = []
receitas: schema.List[schema.Receita] = []

id_receita = 0
id_user = 0

#Back-End

@app.get("/")
def hello():
    return utils.hello()

@app.get("/receitas", response_model=schema.List[schema.Receita], status_code=utils.HTTPStatus.OK)
def get_todas_receitas():
    return utils.get_todas_receitas(receitas)

@app.get("/receitas/{nome_receita}", response_model=schema.Receita, status_code=utils.HTTPStatus.OK)
def get_receita_por_nome(nome_receita: str):
    return utils.get_receita_por_nome(receitas, nome_receita)

@app.get("/receitas/id/{id}", response_model=schema.Receita , status_code=utils.HTTPStatus.OK)
def get_receita(id: int):
    return utils.get_receita(receitas, id)

@app.post("/receitas" , response_model=schema.Receita, status_code=utils.HTTPStatus.CREATED)
def create_receita(dados: schema.Create_Receita):
    global id_receita
    id_receita += 1
    return utils.create_receita(receitas, id_receita, dados)

@app.put("/receitas/{id}" , response_model=schema.Receita, status_code=utils.HTTPStatus.OK)
def update_receita(id: int, dados: schema.Create_Receita):
    return utils.update_receita(receitas, id, dados)

@app.delete("/receitas/{id}" , response_model=schema.Receita , status_code=utils.HTTPStatus.OK)
def deletar_receita(id: int):
    return utils.deletar_receita(receitas, id)

#Usuário

@app.post("/usuarios" , response_model=schema.UsuarioPublic, status_code=utils.HTTPStatus.CREATED)
def create_usuario(dados: schema.BaseUsuario):
    global id_user
    id_user += 1
    return utils.create_usuario(dados)

@app.get("/Usuarios", status_code=utils.HTTPStatus.OK, response_model=schema.List[schema.UsuarioPublic])
def get_todos_usuarios():
    return utils.get_todos_usuarios()

@app.get("/Usuarios/{nome_usuario}", status_code=utils.HTTPStatus.OK, response_model=schema.UsuarioPublic)
def get_usuarios_por_nome(nome_usuario: str):
    return utils.get_usuarios_por_nome(nome_usuario)

@app.get("/Usuarios/{id}", status_code=utils.HTTPStatus.OK, response_model=schema.UsuarioPublic)
def get_usuarios_por_id(id: int):
    return utils.get_usuarios_por_id(id)

@app.put("/usuarios/{id}", response_model=schema.UsuarioPublic, status_code=utils.HTTPStatus.OK)
def update_usuario(id: int, dados: schema.BaseUsuario):
    return utils.update_usuario(id, dados)

@app.delete("/usuarios/{id}", response_model=schema.UsuarioPublic, status_code=utils.HTTPStatus.OK)
def delete_usuario(id: int):
    return utils.delete_usuario(id)