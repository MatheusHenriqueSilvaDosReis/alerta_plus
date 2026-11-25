
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from supabase import create_client

from database import SUPABASE_URL, SUPABASE_KEY
from models.contato import ContatoCadastro, ContatoAtualizacao


router = APIRouter(prefix="/contatos", tags=["Contatos"])

security = HTTPBearer()


# AUTENTICAÇÃO
def obter_usuario(
    credenciais: HTTPAuthorizationCredentials = Depends(security)
):
    token = credenciais.credentials

    try:
        cliente = create_client(SUPABASE_URL, SUPABASE_KEY)

        resposta = cliente.auth.get_user(token)

        if not resposta.user:
            raise HTTPException(
                status_code=401,
                detail="Usuário não autenticado"
            )

        cliente.postgrest.auth(token)

        return cliente, str(resposta.user.id)

    except HTTPException:
        raise

    except Exception as erro:
        print("ERRO NA AUTENTICAÇÃO:", repr(erro))

        raise HTTPException(
            status_code=401,
            detail="Token inválido ou expirado"
        )


# CADASTRAR CONTATO
@router.post("/", status_code=201)
def cadastrar_contato(
    dados: ContatoCadastro,
    autenticacao=Depends(obter_usuario)
):
    cliente, usuario_id = autenticacao

    try:
        resposta = cliente.table("contatos").insert({
            "usuario_id": usuario_id,
            "nome": dados.nome,
            "telefone": dados.telefone
        }).execute()

        return {
            "mensagem": "Contato cadastrado com sucesso!",
            "contato": resposta.data
        }

    except Exception as erro:
        print("ERRO AO CADASTRAR CONTATO:", repr(erro))

        raise HTTPException(
            status_code=400,
            detail="Não foi possível cadastrar o contato"
        )


# LISTAR CONTATOS
@router.get("/")
def listar_contatos(
    autenticacao=Depends(obter_usuario)
):
    cliente, usuario_id = autenticacao

    try:
        resposta = (
            cliente.table("contatos")
            .select("*")
            .eq("usuario_id", usuario_id)
            .execute()
        )

        return resposta.data

    except Exception as erro:
        print("ERRO AO LISTAR CONTATOS:", repr(erro))

        raise HTTPException(
            status_code=400,
            detail="Não foi possível listar os contatos"
        )


# EDITAR CONTATO
@router.put("/{contato_id}")
def editar_contato(
    contato_id: int,
    dados: ContatoAtualizacao,
    autenticacao=Depends(obter_usuario)
):
    cliente, usuario_id = autenticacao

    try:
        resposta = (
            cliente.table("contatos")
            .update({
                "nome": dados.nome,
                "telefone": dados.telefone
            })
            .eq("id", contato_id)
            .eq("usuario_id", usuario_id)
            .select("*")
            .execute()
        )

        if not resposta.data:
            raise HTTPException(
                status_code=404,
                detail="Contato não encontrado"
            )

        return {
            "mensagem": "Contato atualizado com sucesso!",
            "contato": resposta.data
        }

    except HTTPException:
        raise

    except Exception as erro:
        print("ERRO AO EDITAR CONTATO:", repr(erro))

        raise HTTPException(
            status_code=400,
            detail="Não foi possível editar o contato"
        )


# EXCLUIR CONTATO
@router.delete("/{contato_id}")
def excluir_contato(
    contato_id: int,
    autenticacao=Depends(obter_usuario)
):
    cliente, usuario_id = autenticacao

    try:
        resposta = (
            cliente.table("contatos")
            .delete()
            .eq("id", contato_id)
            .eq("usuario_id", usuario_id)
            .select("id")
            .execute()
        )

        if not resposta.data:
            raise HTTPException(
                status_code=404,
                detail="Contato não encontrado"
            )

        return {
            "mensagem": "Contato excluído com sucesso!"
        }

    except HTTPException:
        raise

    except Exception as erro:
        print("ERRO AO EXCLUIR CONTATO:", repr(erro))

        raise HTTPException(
            status_code=400,
            detail="Não foi possível excluir o contato"
        )
