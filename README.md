# FastAPI Hello Word

API simples com FastAPI que retorna `Hello Word`.

## Endpoint

- `GET /` -> `{"message":"Hello Word"}`

## Rodar localmente (sem Docker)

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows PowerShell
pip install -r requirements.txt
uvicorn main:app --reload
```

Acesse: `http://localhost:8000`

## Rodar com Docker localmente

```bash
docker build -t hello-word-api .
docker run -d --name hello-word-api -p 8000:8000 hello-word-api
```

Teste:

```bash
curl http://localhost:8000/
```

## Deploy na VPS Hostinger usando EasyPanel

## 1) Subir código no GitHub

Crie um repositório com estes arquivos:

- `main.py`
- `requirements.txt`
- `Dockerfile`
- `.dockerignore`
- `README.md`

## 2) Criar o app no EasyPanel

1. No EasyPanel, clique em **New Project** (ou selecione um projeto existente).
2. Clique em **New Service**.
3. Escolha **App**.
4. Selecione **Deploy from Git Repository**.
5. Conecte o repositório.
6. Branch: `main` (ou a que você usar).

## 3) Configurar Build e Porta

- O EasyPanel vai detectar o `Dockerfile` automaticamente.
- Configure a porta do serviço para `8000` (porta interna do container).

Comando de start já está no `Dockerfile`:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

## 4) Publicar domínio

1. Abra o serviço criado.
2. Vá em **Domains**.
3. Adicione seu domínio/subdomínio.
4. Ative SSL (Let's Encrypt) no EasyPanel.

## 5) Verificação

Depois do deploy, teste:

- `https://seu-dominio/`

Resposta esperada:

```json
{"message":"Hello Word"}
```
