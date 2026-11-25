
from pydantic import BaseModel, Field


class ContatoCadastro(BaseModel):
    nome: str = Field(min_length=2, max_length=100)
    telefone: str = Field(min_length=8, max_length=20)


class ContatoAtualizacao(BaseModel):
    nome: str = Field(min_length=2, max_length=100)
    telefone: str = Field(min_length=8, max_length=20)
