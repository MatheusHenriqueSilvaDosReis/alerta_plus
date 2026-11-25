from database import supabase

print("Viena iniciou!")

try:
    resposta = supabase.table("usuarios").select("*").execute()

    print("Conexão realizada com sucesso!")
    print("Usuários encontrados:", resposta.data)

except Exception as erro:
    print("Erro ao consultar banco:")
    print(erro)