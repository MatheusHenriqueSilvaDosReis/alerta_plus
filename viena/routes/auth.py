
from fastapi import APIRouter, HTTPException
from models.usuario import UsuarioCadastro, LoginUsuario
from database import supabase

router = APIRouter()


@router.post("/cadastro", status_code=201)
def cadastrar_usuario(usuario: UsuarioCadastro):
    try:
        resposta = supabase.auth.sign_up({
            "email": usuario.email,
            "password": usuario.senha,
            "options": {
                "data": {
                    "nome": usuario.nome
                }
            }
        })

        if not resposta.user:
            raise HTTPException(
                status_code=400,
                detail="Não foi possível criar a conta."
            )

        return {
            "mensagem": "Conta criada com sucesso!",
            "usuario": {
                "id": str(resposta.user.id),
                "email": resposta.user.email,
                "nome": usuario.nome
            }
        }

    except HTTPException:
        raise

    except Exception as erro:
        print("ERRO REAL NO CADASTRO:", repr(erro))

        raise HTTPException(
            status_code=400,
            detail="Erro ao realizar cadastro. Confira os dados."
        )


@router.post("/login")
def fazer_login(dados: LoginUsuario):
    try:
        resposta = supabase.auth.sign_in_with_password({
            "email": dados.email.strip(),
            "password": dados.senha
        })

        if not resposta.user or not resposta.session:
            raise HTTPException(
                status_code=401,
                detail="Não foi possível autenticar. Verifique seu e-mail e senha."
            )

        return {
            "mensagem": "Login realizado com sucesso!",
            "access_token": resposta.session.access_token,
            "refresh_token": resposta.session.refresh_token,
            "usuario": {
                "id": str(resposta.user.id),
                "email": resposta.user.email
            }
        }

    except HTTPException:
        raise

    except Exception as erro:
        print("ERRO REAL NO LOGIN:", repr(erro))

        raise HTTPException(
            status_code=401,
            detail="Falha na autenticação. Verifique o e-mail, a senha e a confirmação da conta."
        )
