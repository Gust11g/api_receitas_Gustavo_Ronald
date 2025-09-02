from fastapi import FastAPI, status
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Livro de Receitas")

class Receita(BaseModel):
    nome: str
    ingredientes: List[str]
    modo_d_preparo: str


'''
receitas = [
    {
        "nome": "Brigadeiro Tradicional",
        "descricao": "O doce mais amado do Brasil, perfeito para festas e para qualquer momento!",
        "ingredientes": [
            "1 lata de leite condensado",
            "1 colher de sopa de manteiga sem sal",
            "4 colheres de sopa de chocolate em pó",
            "Chocolate granulado para decorar"
        ],
        "utensílios": [
            "panela",
            "prato",
            "forminhas de papel"
        ],
        "modo de preparo": "Em uma panela, coloque o leite condensado, a manteiga e o chocolate em pó. Cozinhe em fogo médio, mexendo sempre, até a mistura desgrudar do fundo da panela (cerca de 10 minutos). Despeje em um prato untado com manteiga e deixe esfriar. Com as mãos untadas, enrole pequenas bolinhas e passe no chocolate granulado. Sirva em forminhas de papel."
    },
    {
        "nome": "Bolo de Fubá da Vovó",
        "descricao": "Um bolo simples, fofinho e perfeito para o café da tarde.",
        "ingredientes": [
            "2 xícaras de açúcar",
            "3 xícaras de fubá",
            "2 xícaras de farinha de trigo",
            "1 xícara de óleo",
            "4 ovos",
            "2 xícaras de leite",
            "1 colher de sopa de fermento em pó"
        ],
        "utensílios": [
            "liquidificador",
            "tigela",
            "forma"
        ],
        "modo de preparo": "No liquidificador, bata os ovos, o açúcar, o óleo e o leite. Em uma tigela, misture o fubá, a farinha de trigo e o fermento. Despeje a mistura líquida na tigela com os ingredientes secos e mexa bem até a massa ficar homogênea. Coloque a massa em uma forma untada e enfarinhada. Leve ao forno pré-aquecido a 180°C por aproximadamente 40 minutos, ou até dourar."
    },
    {
        "nome": "Mousse de Maracujá Rápido",
        "descricao": "Uma sobremesa refrescante, fácil e que leva apenas 3 ingredientes.",
        "ingredientes": [
            "1 lata de leite condensado",
            "1 lata de creme de leite",
            "1 lata (use a mesma medida) de suco de maracujá concentrado"
        ],
        "utensílios": [
            "liquidificador",
            "taças individuais",
            "refratário"
        ],
        "modo de preparo": "Coloque todos os ingredientes no liquidificador. Bata por aproximadamente 3 minutos, até obter uma mistura cremosa e consistente. Despeje em taças individuais ou em um refratário. Leve à geladeira por pelo menos 2 horas antes de servir."
    },
    {
        "nome": "Pão de Queijo Mineiro",
        "descricao": "Aquele pão de queijo quentinho e delicioso, com a receita tradicional de Minas Gerais.",
        "ingredientes": [
            "500g de polvilho azedo",
            "1 copo (americano) de água",
            "1 copo (americano) de leite",
            "1/2 copo (americano) de óleo",
            "2 ovos",
            "250g de queijo parmesão ralado",
            "Sal a gosto"
        ],
        "utensílios": [
            "panela",
            "tigela grande",
            "colher",
            "assadeira"
        ],
        "modo de preparo": "Em uma panela, ferva a água, o leite, o óleo e o sal. Despeje essa mistura sobre o polvilho em uma tigela grande e misture bem com uma colher. Deixe amornar. Adicione os ovos um a um, mexendo bem a cada adição. Por último, acrescente o queijo parmesão ralado e amasse com as mãos até obter uma massa homogênea. Faça bolinhas do tamanho desejado e coloque em uma assadeira (não precisa untar). Asse em forno pré-aquecido a 180°C por cerca de 30 minutos, ou até dourarem."
    },
    {
        "nome": "Salada",
        "descricao": "Uma opção leve, saudável e deliciosa para qualquer hora do dia.",
        "ingredientes": [
            "1 mamão papaia picado",
            "1 manga picada",
            "2 bananas picadas",
            "1 cacho de uvas sem sementes",
            "4 fatias de abacaxi picado",
            "1 maçã picada",
            "Suco de 2 laranjas"
        ],
        "utensílios": [
            "tigela grande",
            "faca",
            "tábua de corte"
        ],
        "modo de preparo": "Em uma tigela grande, misture delicadamente todas as frutas picadas. Regue com o suco de laranja para evitar que as frutas escureçam e para dar mais sabor. Leve à geladeira por pelo menos 30 minutos antes de servir. Opcional: sirva com iogurte natural ou uma bola de sorvete."
    },
    {
        "nome": "Strogonoff",
        "descricao": "Um clássico do dia a dia, cremoso e muito saboroso.",
        "ingredientes": [
            "1 kg de peito de frango em cubos",
            "2 colheres de sopa de manteiga",
            "1 cebola média picada",
            "2 dentes de alho picados",
            "2 latas de creme de leite",
            "2 colheres de sopa de ketchup",
            "1 colher de sopa de mostarda",
            "Sal e pimenta do reino a gosto",
            "Batata palha para acompanhar"
        ],
        "utensílios": [
            "panela grande",
            "faca",
            "tábua de corte"
        ],
        "modo de preparo": "Tempere o frango com sal e pimenta. Em uma panela grande, derreta a manteiga e doure o frango. Adicione a cebola e o alho e refogue até ficarem macios. Junte o ketchup e a mostarda, misturando bem. Desligue o fogo, adicione o creme de leite e mexa até incorporar. Sirva quente, acompanhado de arroz branco e batata palha."
    }
]

@app.get("/receitas")
def listar_receitas():
    return receitas


@app.get("/receitas/{nome}")
def buscar_receitas (nome: str):
    for receita in receitas:
        if receita['nome'].lower() == nome.lower():
            return receita
    return {"erro": "Receita nao encontrada"}          
'''

receitas: List[Receita] = []
@app.get("/receitas/")
def get_todas_receitas():
    return receitas

@app.post("/receitas", response_model=Receita, status_code=status.HTTP_201_CREATED)
def criar_receita(dados: Receita):
    novo_id = len(receitas) + 1
    nova_receita = Receita(
        id=novo_id,
        nome=dados.nome,
        ingredientes=dados.ingredientes,
        modo_d_preparo=dados.modo_d_preparo
    )
    
    receitas.append(nova_receita)
    return nova_receita
@app.get("/receitas/id/{id}")
def get_receita_por_id():