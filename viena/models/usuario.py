from pydantic import BaseModel, EmailStr, Field

class UsuarioCadastro(BaseModel):
    nome: str = Field(min_length=2, max_length=100)
    email: EmailStr
    senha: str = Field(min_length=8)

class LoginUsuario(BaseModel):
    email: str
    senha: str