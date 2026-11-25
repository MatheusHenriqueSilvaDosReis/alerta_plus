
# Alerta+ — Back-end

API desenvolvida em Python com FastAPI, responsável pela autenticação dos usuários e pelo gerenciamento dos contatos de confiança do aplicativo Alerta+.

## Tecnologias
- Python
- FastAPI
- Uvicorn
- Supabase
- PostgreSQL
- python-dotenv

## Funcionalidades
- Cadastro de usuários.
- Login e geração de token de acesso.
- Cadastro de contatos.
- Listagem de contatos.
- Edição de contatos.
- Exclusão de contatos.
- Autenticação das rotas por Bearer Token.

## Como executar

### 1. Clonar o repositório
```bash
git clone https://github.com/MatheusHenriqueSilvaDosReis/Viena.git
```

### 2. Acessar a pasta
```bash
cd Viena
```

### 3. Criar ambiente virtual
```bash
python -m venv venv
```

### 4. Ativar ambiente virtual

Windows PowerShell:
```powershell
.\venv\Scripts\Activate.ps1
```

Windows CMD:
```cmd
venv\Scripts\activate
```

### 5. Instalar dependências

Se existir o arquivo requirements.txt:
```bash
pip install -r requirements.txt
```

Caso não exista:
```bash
pip install fastapi "uvicorn[standard]" supabase python-dotenv
```

### 6. Configurar o arquivo .env

Crie um arquivo `.env` na pasta principal do projeto:

```env
SUPABASE_URL=sua_url_do_supabase
SUPABASE_KEY=sua_chave_do_supabase
```

Confira os nomes das variáveis no código da aplicação e utilize as credenciais do seu projeto Supabase. Não publique esse arquivo no GitHub.

### 7. Executar a API
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 8. Acessar a documentação

Swagger:
```text
http://127.0.0.1:8000/docs
```

Redoc:
```text
http://127.0.0.1:8000/redoc
```

## Autenticação

As rotas protegidas recebem o token no cabeçalho:

```http
Authorization: Bearer SEU_ACCESS_TOKEN
```

O token é obtido após o login do usuário.

## Integração com o aplicativo

Para conectar o front-end à API:
1. Inicie o back-end.
2. Consulte o IPv4 do computador com `ipconfig`.
3. Configure o endereço da API no front-end.
4. Mantenha computador e celular na mesma rede Wi-Fi.
5. Verifique se o Firewall permite conexões pela porta 8000.
