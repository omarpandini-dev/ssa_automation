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

- `AUTH_API_URL`
- `AUTH_API_USER`
- `AUTH_API_PASSWORD`
- `AUTH_API_VERIFY_SSL`
- `SESSION_SECRET_KEY`
- `EMAIL_SMTP_HOST`
- `EMAIL_SMTP_PORT`
- `EMAIL_SMTP_USER`
- `EMAIL_SMTP_PASSWORD`
- `EMAIL_SMTP_FROM`
- `EMAIL_SMTP_STARTTLS`

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
- `GET /forgot-password`: formulario de recuperacao
- `POST /forgot-password`: envia email de recuperacao
- `GET /ini`: painel protegido por sessao
- `POST /logout`: encerra sessao
