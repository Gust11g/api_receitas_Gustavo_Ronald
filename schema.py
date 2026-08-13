from typing import List

from pydantic import BaseModel, ConfigDict, EmailStr, Field, model_validator


class Receita(BaseModel):
    id: int
    nome: str
    ingredientes: List[str]
    modo_de_preparo: str


class Create_Receita(BaseModel):
    nome: str = Field(min_length=1, max_length=200)
    ingredientes: List[str] = Field(min_length=1)
    modo_de_preparo: str = Field(min_length=1)


class BaseUsuario(BaseModel):
    nome_usuario: str = Field(min_length=2, max_length=80)
    email: EmailStr
    senha: str = Field(min_length=8, max_length=128)
    first_name: str = ""
    last_name: str = ""


class UsuarioPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    nome_usuario: str
    email: EmailStr
    first_name: str = ""
    last_name: str = ""
    is_active: bool = True


class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    re_password: str = Field(min_length=8, max_length=128)
    nome_usuario: str | None = Field(default=None, min_length=2, max_length=80)
    first_name: str = ""
    last_name: str = ""

    @model_validator(mode="after")
    def passwords_match(self):
        if self.password != self.re_password:
            raise ValueError("As senhas não coincidem")
        return self


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=128)


class RefreshRequest(BaseModel):
    refresh: str


class TokenPair(BaseModel):
    access: str
    refresh: str


class AccessTokenResponse(BaseModel):
    access: str


class VerifyTokenRequest(BaseModel):
    token: str


class ProfileUpdate(BaseModel):
    first_name: str | None = Field(default=None, max_length=150)
    last_name: str | None = Field(default=None, max_length=150)
    email: EmailStr | None = None


class Usuario(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    nome_usuario: str
    email: EmailStr
    senha: str
