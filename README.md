# API Livro de Receitas

Backend FastAPI com persistência SQLAlchemy e autenticação JWT. A integração implementada segue o fluxo descrito em `Backend_pt2.pdf`: registro, login, access/refresh tokens, proteção de rotas, renovação de access token e edição de perfil.

## Execução local

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
uvicorn main:app --reload
```

Sem `.env`, a aplicação usa `database.db` e uma chave JWT de desenvolvimento. Em ambiente compartilhado, defina `DATABASE_URL` e `JWT_SECRET_KEY`. Também podem ser configurados `ACCESS_TOKEN_EXPIRE_MINUTES`, `REFRESH_TOKEN_EXPIRE_DAYS` e `CORS_ORIGINS`.

## Autenticação

O registro é feito em `POST /auth/users/` com `email`, `password`, `re_password`, `nome_usuario` opcional, `first_name` e `last_name`. O login ocorre em `POST /auth/jwt/create/` e retorna `access` e `refresh`. Para renovar o access token, use `POST /auth/jwt/refresh/`; para validar um token, use `POST /auth/jwt/verify/`.

As rotas `GET /auth/users/me/` e `PATCH /auth/users/me/` exigem `Authorization: Bearer <access_token>`. A criação, edição e exclusão de receitas também exigem autenticação. Senhas são armazenadas exclusivamente com hash Argon2id e nunca aparecem nas respostas públicas.

A documentação interativa está disponível em `/docs`.

## Testes

```bash
pytest -q
```

A suíte cobre registro, hash de senha, login, rejeição de credenciais inválidas, proteção de rota, consulta do usuário autenticado, criação de receita autenticada e refresh de token.