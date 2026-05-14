import os
import html
import time
import json
import base64
import ssl
import secrets
import smtplib
from urllib import request as urllib_request
from urllib.error import URLError, HTTPError
from email.message import EmailMessage

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
from dotenv import load_dotenv

from ini import render_ini_page

load_dotenv()

app = FastAPI(title="Login Page")
app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SESSION_SECRET_KEY", "change-this-secret-key"),
)

AUTH_API_URL = os.getenv("AUTH_API_URL")
AUTH_API_USER = os.getenv("AUTH_API_USER")
AUTH_API_PASSWORD = os.getenv("AUTH_API_PASSWORD")
AUTH_API_VERIFY_SSL = os.getenv("AUTH_API_VERIFY_SSL", "true").lower() == "true"
EMAIL_SMTP_HOST = os.getenv("EMAIL_SMTP_HOST")
EMAIL_SMTP_PORT = int(os.getenv("EMAIL_SMTP_PORT", "587"))
EMAIL_SMTP_USER = os.getenv("EMAIL_SMTP_USER")
EMAIL_SMTP_PASSWORD = os.getenv("EMAIL_SMTP_PASSWORD")
EMAIL_SMTP_FROM = os.getenv("EMAIL_SMTP_FROM")
EMAIL_SMTP_STARTTLS = os.getenv("EMAIL_SMTP_STARTTLS", "true").lower() == "true"
SESSION_IDLE_TIMEOUT_SECONDS = 30 * 60

if not AUTH_API_URL or not AUTH_API_USER or not AUTH_API_PASSWORD:
    raise RuntimeError(
        "Defina AUTH_API_URL, AUTH_API_USER e AUTH_API_PASSWORD no arquivo .env antes de iniciar a aplicacao."
    )


def render_login_page(error: str = "") -> str:
    error_html = f'<div class="error">{html.escape(error)}</div>' if error else ""
    return f"""<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Login</title>
  <style>
    :root {{
      --bg-1: #071429;
      --bg-2: #0b1f3a;
      --card: #102845;
      --text: #e8f1ff;
      --muted: #a8bfdc;
      --accent: #2f6df6;
      --accent-hover: #2458c8;
      --error: #ff8f8f;
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
      backdrop-filter: blur(6px);
      border-radius: 16px;
      padding: 28px;
      box-shadow: 0 24px 50px rgba(0, 0, 0, 0.35);
      animation: rise 400ms ease-out;
    }}
    @keyframes rise {{
      from {{ transform: translateY(8px); opacity: 0; }}
      to {{ transform: translateY(0); opacity: 1; }}
    }}
    h1 {{
      margin: 0 0 8px;
      font-size: 28px;
      letter-spacing: 0.4px;
    }}
    p {{
      margin: 0 0 22px;
      color: var(--muted);
      font-size: 14px;
    }}
    label {{
      display: block;
      margin: 12px 0 6px;
      font-size: 14px;
      color: #d5e4ff;
    }}
    input {{
      width: 100%;
      border: 1px solid var(--border);
      border-radius: 10px;
      background: #0c223d;
      color: var(--text);
      padding: 12px 14px;
      font-size: 15px;
      outline: none;
      transition: border-color .2s ease, box-shadow .2s ease;
    }}
    input:focus {{
      border-color: var(--accent);
      box-shadow: 0 0 0 3px rgba(47, 109, 246, 0.2);
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
      transition: transform .08s ease, background .2s ease;
    }}
    button:hover {{ background: var(--accent-hover); }}
    button:active {{ transform: translateY(1px); }}
    .error {{
      margin: 0 0 14px;
      border: 1px solid rgba(255, 143, 143, 0.45);
      background: rgba(255, 143, 143, 0.12);
      color: var(--error);
      font-size: 14px;
      border-radius: 8px;
      padding: 10px 12px;
    }}
  </style>
</head>
<body>
  <main class="card">
    <h1>Entrar</h1>
    <p>Acesse o painel com suas credenciais.</p>
    {error_html}
    <form method="post" action="/login">
      <label for="username">Usuario</label>
      <input id="username" name="username" type="text" autocomplete="username" required />

      <label for="password">Senha</label>
      <input id="password" name="password" type="password" autocomplete="current-password" required />

      <button type="submit">Login</button>
    </form>
    <p style="margin-top:12px;margin-bottom:0;">
      <a href="/forgot-password" style="color:#9cc0ff;text-decoration:none;">Esqueci minha senha</a>
    </p>
  </main>
</body>
</html>
"""


def render_forgot_password_page(message: str = "", is_error: bool = False) -> str:
    message_html = ""
    if message:
        css_class = "error" if is_error else "info"
        message_html = f'<div class="{css_class}">{html.escape(message)}</div>'

    return f"""<!doctype html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Recuperar senha</title>
  <style>
    :root {{
      --bg-1: #071429;
      --bg-2: #0b1f3a;
      --card: #102845;
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
      backdrop-filter: blur(6px);
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
    .back {{
      display: inline-block;
      margin-top: 14px;
      color: #9cc0ff;
      text-decoration: none;
      font-size: 14px;
    }}
  </style>
</head>
<body>
  <main class="card">
    <h1>Recuperar senha</h1>
    <p>Informe seu e-mail para receber as instrucoes.</p>
    {message_html}
    <form method="post" action="/forgot-password">
      <label for="email">E-mail</label>
      <input id="email" name="email" type="email" autocomplete="email" required />
      <button type="submit">Enviar e-mail</button>
    </form>
    <a class="back" href="/">Voltar para o login</a>
  </main>
</body>
</html>
"""


def _send_forgot_password_email(email: str) -> None:
    random_text = secrets.token_urlsafe(32)
    body = (
        "Solicitacao de recuperacao de senha recebida.\n\n"
        f"Texto aleatorio temporario: {random_text}\n"
    )

    msg = EmailMessage()
    msg["Subject"] = "Recuperacao de senha"
    msg["From"] = EMAIL_SMTP_FROM or "no-reply@example.com"
    msg["To"] = email
    msg.set_content(body)

    smtp_is_configured = all(
        [EMAIL_SMTP_HOST, EMAIL_SMTP_USER, EMAIL_SMTP_PASSWORD, EMAIL_SMTP_FROM]
    )
    if not smtp_is_configured:
        print(f"[forgot-password] SMTP nao configurado. Email gerado para {email}.")
        print(body)
        return

    with smtplib.SMTP(EMAIL_SMTP_HOST, EMAIL_SMTP_PORT, timeout=10) as server:
        if EMAIL_SMTP_STARTTLS:
            server.starttls()
        server.login(EMAIL_SMTP_USER, EMAIL_SMTP_PASSWORD)
        server.send_message(msg)


def _authenticate_with_api(username: str, password: str) -> tuple[bool, str]:
    credentials = f"{AUTH_API_USER}:{AUTH_API_PASSWORD}".encode("utf-8")
    auth_header = base64.b64encode(credentials).decode("utf-8")
    payload = json.dumps({"user": username, "password": password}).encode("utf-8")

    req = urllib_request.Request(
        AUTH_API_URL,
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
        with opener.open(req, timeout=10) as response:
            body = response.read().decode("utf-8")
    except HTTPError as exc:
        body = exc.read().decode("utf-8", errors="ignore")
        try:
            data = json.loads(body) if body else {}
            return False, data.get("msg", "Falha ao validar login.")
        except json.JSONDecodeError:
            return False, "Falha ao validar login."
    except (URLError, TimeoutError) as exc:
        ssl_error = isinstance(getattr(exc, "reason", None), ssl.SSLError) or isinstance(exc, ssl.SSLError)
        if ssl_error:
            return False, "Falha SSL na autenticacao. Configure AUTH_API_VERIFY_SSL=false no .env."
        return False, "Servico de autenticacao indisponivel. Tente novamente."

    try:
        data = json.loads(body) if body else {}
    except json.JSONDecodeError:
        return False, "Resposta invalida do servico de autenticacao."

    status = bool(data.get("status"))
    message = data.get("msg", "")

    if status:
        return True, message or "Login efetuado com sucesso."
    return False, message or "Usuario ou senha invalidos."


def _is_session_active(request: Request) -> bool:
    if not request.session.get("authenticated"):
        return False

    last_activity = request.session.get("last_activity")
    if not isinstance(last_activity, (int, float)):
        request.session.clear()
        return False

    now = int(time.time())
    if now - int(last_activity) > SESSION_IDLE_TIMEOUT_SECONDS:
        request.session.clear()
        return False

    request.session["last_activity"] = now
    return True


@app.get("/", response_class=HTMLResponse)
def login_page(request: Request):
    if _is_session_active(request):
        return RedirectResponse(url="/ini", status_code=303)
    return render_login_page()


@app.post("/login")
def login(request: Request, username: str = Form(...), password: str = Form(...)):
    is_valid, message = _authenticate_with_api(username=username, password=password)
    if is_valid:
        request.session["authenticated"] = True
        request.session["last_activity"] = int(time.time())
        return RedirectResponse(url="/ini", status_code=303)
    return HTMLResponse(content=render_login_page(message), status_code=401)


@app.get("/forgot-password", response_class=HTMLResponse)
def forgot_password_page():
    return render_forgot_password_page()


@app.post("/forgot-password", response_class=HTMLResponse)
def forgot_password(email: str = Form(...)):
    if "@" not in email:
        return HTMLResponse(
            content=render_forgot_password_page("Informe um e-mail valido.", is_error=True),
            status_code=400,
        )

    try:
        _send_forgot_password_email(email=email.strip())
    except Exception:
        return HTMLResponse(
            content=render_forgot_password_page(
                "Nao foi possivel enviar o e-mail agora. Tente novamente em instantes.",
                is_error=True,
            ),
            status_code=502,
        )

    return HTMLResponse(
        content=render_forgot_password_page(
            "Se o e-mail existir, voce recebera as instrucoes em alguns minutos."
        ),
        status_code=200,
    )


@app.get("/ini", response_class=HTMLResponse)
def ini_page(request: Request):
    if not _is_session_active(request):
        return RedirectResponse(url="/", status_code=303)
    return render_ini_page()


@app.post("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/", status_code=303)
