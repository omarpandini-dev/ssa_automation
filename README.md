# SSA Automation - FastAPI Login

Aplicacao FastAPI com pagina de login e painel protegido por sessao.

## Estrutura principal

- `login.py`: app principal (`login:app`) com rotas de login, logout e protecao de sessao.
- `ini.py`: renderizacao da pagina de painel (`/ini`).
- `.env`: credenciais e chave de sessao.

## Requisitos

- Python 3.10+ (recomendado)
- `pip`

## Configuracao de ambiente

Copie o exemplo e ajuste as credenciais:

```powershell
Copy-Item .env.example .env
```

Variaveis usadas:

- `APP_LOGIN_USER`
- `APP_LOGIN_PASSWORD`
- `SESSION_SECRET_KEY`

## Rodar localmente (Windows PowerShell)

```powershell
cd c:\Users\mzo_p\OneDrive\Documentos\python\ssa_automation
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn login:app --reload
```

Abra:

- `http://127.0.0.1:8000/`

## Rodar localmente (Linux/Mac)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn login:app --reload
```

## Rodar com Docker

```bash
docker build -t ssa-automation .
docker run --rm -p 8000:8000 --env-file .env ssa-automation
```

Abra:

- `http://127.0.0.1:8000/`

## Rotas principais

- `GET /`: pagina de login
- `POST /login`: autentica usuario/senha
- `GET /ini`: painel protegido por sessao
- `POST /logout`: encerra sessao
