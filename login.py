import os

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.middleware.sessions import SessionMiddleware

from ini import render_ini_page

app = FastAPI(title="Login Page")
app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SESSION_SECRET_KEY", "change-this-secret-key"),
)

VALID_USER = "admin"
VALID_PASSWORD = "admin"


def render_login_page(error: str = "") -> str:
    error_html = f'<div class="error">{error}</div>' if error else ""
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
  </main>
</body>
</html>
"""


@app.get("/", response_class=HTMLResponse)
def login_page(request: Request):
    if request.session.get("authenticated"):
        return RedirectResponse(url="/ini", status_code=303)
    return render_login_page()


@app.post("/login")
def login(request: Request, username: str = Form(...), password: str = Form(...)):
    if username == VALID_USER and password == VALID_PASSWORD:
        request.session["authenticated"] = True
        return RedirectResponse(url="/ini", status_code=303)
    return HTMLResponse(content=render_login_page("Usuario ou senha invalidos."), status_code=401)


@app.get("/ini", response_class=HTMLResponse)
def ini_page(request: Request):
    if not request.session.get("authenticated"):
        return RedirectResponse(url="/", status_code=303)
    return render_ini_page()


@app.post("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/", status_code=303)
