import html
import os
import json
import base64
import ssl
from urllib import request as urllib_request
from urllib.error import URLError, HTTPError

from fastapi import APIRouter, Form, Query
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

AUTH_API_USER = os.getenv("AUTH_API_USER")
AUTH_API_PASSWORD = os.getenv("AUTH_API_PASSWORD")
AUTH_API_VERIFY_SSL = os.getenv("AUTH_API_VERIFY_SSL", "true").lower() == "true"
RESET_TOKEN_VALIDATE_URL = os.getenv(
    "RESET_TOKEN_VALIDATE_URL"
)
RESET_PASSWORD_UPDATE_URL = os.getenv(
    "RESET_PASSWORD_UPDATE_URL"
)

if (
    not AUTH_API_USER
    or not AUTH_API_PASSWORD
    or not RESET_TOKEN_VALIDATE_URL
    or not RESET_PASSWORD_UPDATE_URL
):
    raise RuntimeError(
        "Defina AUTH_API_USER, AUTH_API_PASSWORD, RESET_TOKEN_VALIDATE_URL e RESET_PASSWORD_UPDATE_URL no arquivo .env antes de iniciar a aplicacao."
    )


def render_reset_password_page(
    token: str = "",
    message: str = "",
    is_error: bool = False,
) -> str:
    message_html = ""
    if message:
        css_class = "error" if is_error else "info"
        message_html = f'<div class="{css_class}">{html.escape(message)}</div>'

    escaped_token = html.escape(token, quote=True)
    show_form = bool(token.strip())
    form_html = ""
    back_to_login_html = ""
    subtitle_html = "<p>Defina a nova senha para concluir a recuperacao.</p>"
    if show_form:
        form_html = f"""
    <form method="post" action="/reset-password">
      <input type="hidden" name="token" value="{escaped_token}" />

      <label for="password_1">Senha</label>
      <input id="password_1" name="password_1" type="password" autocomplete="new-password" required />

      <label for="password_2">Repita a senha</label>
      <input id="password_2" name="password_2" type="password" autocomplete="new-password" required />

      <button type="submit">Enviar</button>
    </form>
"""
    elif message and not is_error:
        subtitle_html = ""
        back_to_login_html = """
    <p style="margin-top:12px;margin-bottom:0;">
      <a href="/" style="display:inline-block;text-decoration:none;background:var(--accent);color:#fff;padding:10px 14px;border-radius:10px;font-weight:600;">
        Voltar ao login
      </a>
    </p>
"""

    return f"""<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Alterar senha</title>
  <style>
    :root {{
      --bg-1: #071429;
      --bg-2: #0b1f3a;
      --text: #e8f1ff;
      --muted: #a8bfdc;
      --accent: #2f6df6;
      --accent-hover: #2458c8;
      --error: #ff8f8f;
      --info: #9cd5ff;
      --border: #1b3c64;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      min-height: 100vh;
      display: grid;
      place-items: center;
      font-family: "Segoe UI", "Helvetica Neue", sans-serif;
      color: var(--text);
      background:
        radial-gradient(circle at 15% 20%, #15365f 0%, transparent 38%),
        radial-gradient(circle at 85% 80%, #113059 0%, transparent 40%),
        linear-gradient(135deg, var(--bg-1), var(--bg-2));
      padding: 20px;
    }}
    .card {{
      width: 100%;
      max-width: 420px;
      background: linear-gradient(180deg, rgba(255,255,255,0.06), rgba(255,255,255,0.02));
      border: 1px solid var(--border);
      border-radius: 16px;
      padding: 28px;
      box-shadow: 0 24px 50px rgba(0, 0, 0, 0.35);
    }}
    h1 {{ margin: 0 0 8px; font-size: 28px; }}
    p {{ margin: 0 0 22px; color: var(--muted); font-size: 14px; }}
    label {{ display: block; margin: 12px 0 6px; font-size: 14px; color: #d5e4ff; }}
    input {{
      width: 100%;
      border: 1px solid var(--border);
      border-radius: 10px;
      background: #0c223d;
      color: var(--text);
      padding: 12px 14px;
      font-size: 15px;
      outline: none;
    }}
    button {{
      width: 100%;
      margin-top: 18px;
      border: 0;
      border-radius: 10px;
      background: var(--accent);
      color: #fff;
      font-size: 15px;
      font-weight: 600;
      padding: 12px 14px;
      cursor: pointer;
    }}
    button:hover {{ background: var(--accent-hover); }}
    .error {{
      margin: 0 0 14px;
      border: 1px solid rgba(255, 143, 143, 0.45);
      background: rgba(255, 143, 143, 0.12);
      color: var(--error);
      font-size: 14px;
      border-radius: 8px;
      padding: 10px 12px;
    }}
    .info {{
      margin: 0 0 14px;
      border: 1px solid rgba(156, 213, 255, 0.45);
      background: rgba(156, 213, 255, 0.12);
      color: var(--info);
      font-size: 14px;
      border-radius: 8px;
      padding: 10px 12px;
    }}
  </style>
</head>
<body>
  <main class="card">
    <h1>Alterar senha</h1>
    {subtitle_html}
    {message_html}
    {form_html}
    {back_to_login_html}
  </main>
</body>
</html>
"""


def _validate_reset_token_with_api(token: str) -> tuple[bool, str]:
    if not AUTH_API_USER or not AUTH_API_PASSWORD:
        return False, "Credenciais da API de validacao nao configuradas."

    credentials = f"{AUTH_API_USER}:{AUTH_API_PASSWORD}".encode("utf-8")
    auth_header = base64.b64encode(credentials).decode("utf-8")
    payload = json.dumps({"token": token}).encode("utf-8")

    req = urllib_request.Request(
        RESET_TOKEN_VALIDATE_URL,
        data=payload,
        method="POST",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Basic {auth_header}",
        },
    )

    handlers = [urllib_request.ProxyHandler({})]
    if not AUTH_API_VERIFY_SSL:
        insecure_context = ssl._create_unverified_context()
        handlers.append(urllib_request.HTTPSHandler(context=insecure_context))
    opener = urllib_request.build_opener(*handlers)

    try:
        with opener.open(req, timeout=15) as response:
            body = response.read().decode("utf-8")
    except HTTPError as exc:
        body = exc.read().decode("utf-8", errors="ignore")
        try:
            data = json.loads(body) if body else {}
            return False, str(data.get("msg", "Falha ao validar token."))
        except json.JSONDecodeError:
            return False, "Falha ao validar token."
    except (URLError, TimeoutError):
        return False, "Servico de validacao de token indisponivel."

    try:
        data = json.loads(body) if body else {}
    except json.JSONDecodeError:
        return False, "Resposta invalida do servico de validacao."

    is_valid = bool(data.get("ret"))
    message = str(data.get("msg", ""))
    if is_valid:
        return True, message or "Token valido"
    return False, message or "Token invalido ou expirado"


def _update_password_with_api(token: str, password: str) -> tuple[bool, str]:
    if not AUTH_API_USER or not AUTH_API_PASSWORD:
        return False, "Credenciais da API de alteracao nao configuradas."

    credentials = f"{AUTH_API_USER}:{AUTH_API_PASSWORD}".encode("utf-8")
    auth_header = base64.b64encode(credentials).decode("utf-8")
    payload = json.dumps({"token": token, "senha": password}).encode("utf-8")

    req = urllib_request.Request(
        RESET_PASSWORD_UPDATE_URL,
        data=payload,
        method="POST",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Basic {auth_header}",
        },
    )

    handlers = [urllib_request.ProxyHandler({})]
    if not AUTH_API_VERIFY_SSL:
        insecure_context = ssl._create_unverified_context()
        handlers.append(urllib_request.HTTPSHandler(context=insecure_context))
    opener = urllib_request.build_opener(*handlers)

    try:
        with opener.open(req, timeout=15) as response:
            body = response.read().decode("utf-8")
    except HTTPError as exc:
        body = exc.read().decode("utf-8", errors="ignore")
        try:
            data = json.loads(body) if body else {}
            return False, str(data.get("msg", "Erro ao alterar senha."))
        except json.JSONDecodeError:
            return False, "Erro ao alterar senha."
    except (URLError, TimeoutError):
        return False, "Servico de alteracao de senha indisponivel."

    try:
        data = json.loads(body) if body else {}
    except json.JSONDecodeError:
        return False, "Resposta invalida do servico de alteracao."

    is_ok = bool(data.get("ret"))
    message = str(data.get("msg", ""))
    if is_ok:
        return True, message or "Senha alterada com sucesso."
    return False, message or "Erro ao alterar senha."


@router.get("/reset-password", response_class=HTMLResponse)
def reset_password_page(token: str = Query(default="")):
    if not token:
        return HTMLResponse(
            content=render_reset_password_page(
                message="Token nao informado no link de recuperacao.",
                is_error=True,
            ),
            status_code=400,
        )
    is_valid, message = _validate_reset_token_with_api(token=token.strip())
    if not is_valid:
        return HTMLResponse(
            content=render_reset_password_page(
                message=message or "Token invalido ou expirado.",
                is_error=True,
            ),
            status_code=400,
        )
    return HTMLResponse(content=render_reset_password_page(token=token), status_code=200)


@router.get("/recuperacao_senha", response_class=HTMLResponse)
def reset_password_page_alias(token: str = Query(default="")):
    return reset_password_page(token=token)


@router.post("/reset-password", response_class=HTMLResponse)
def reset_password_submit(
    token: str = Form(...),
    password_1: str = Form(...),
    password_2: str = Form(...),
):
    if not token.strip():
        return HTMLResponse(
            content=render_reset_password_page(
                message="Token nao informado no link de recuperacao.",
                is_error=True,
            ),
            status_code=400,
        )

    if password_1 != password_2:
        return HTMLResponse(
            content=render_reset_password_page(
                token=token,
                message="As senhas informadas nao sao iguais.",
                is_error=True,
            ),
            status_code=400,
        )

    is_valid, validation_message = _validate_reset_token_with_api(token=token.strip())
    if not is_valid:
        return HTMLResponse(
            content=render_reset_password_page(
                message=validation_message or "Token invalido ou expirado.",
                is_error=True,
            ),
            status_code=400,
        )

    changed, api_message = _update_password_with_api(
        token=token.strip(),
        password=password_1,
    )
    if not changed:
        return HTMLResponse(
            content=render_reset_password_page(
                token=token.strip(),
                message=api_message,
                is_error=True,
            ),
            status_code=400,
        )

    return HTMLResponse(
        content=render_reset_password_page(
            message=api_message,
            is_error=False,
        ),
        status_code=200,
    )
