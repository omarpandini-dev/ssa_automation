import os
from pathlib import Path

from playwright.sync_api import sync_playwright

url = "https://the-internet.herokuapp.com/secure"
session_path = Path("session.json")
headless = os.getenv("PLAYWRIGHT_HEADLESS", "false").lower() in {"1", "true", "yes"}

with sync_playwright() as p:
    browser = p.chromium.launch(headless=headless)

    if session_path.exists():
        context = browser.new_context(storage_state=str(session_path))
        print(f"Sessao carregada de: {session_path}")
    else:
        context = browser.new_context()
        print("Nenhuma sessao salva encontrada.")

    page = context.new_page()
    response = page.goto(url, wait_until="domcontentloaded")
    if not response or response.status >= 400:
        print("Erro ao efetuar login")
    else:
        logout_button = page.get_by_role("link", name="Logout")
        ja_logado = page.url.rstrip("/").endswith("/secure") and logout_button.count() > 0

        if not ja_logado:
            page.get_by_role("textbox", name="Username").fill("tomsmith")
            page.get_by_role("textbox", name="Password").fill("SuperSecretPassword!")
            page.get_by_role("button", name="Login").click()
            page.wait_for_url("**/secure")
            page.get_by_role("link", name="Logout").wait_for(timeout=5000)
            context.storage_state(path=str(session_path))
            print(f"Sessao salva em: {session_path}")
        else:
            print("Sessao ativa, login reaproveitado.")

        contexto_logado = page.url.rstrip("/").endswith("/secure") and page.get_by_role(
            "link", name="Logout"
        ).count() > 0

        if contexto_logado:
            print(page.title())
        else:
            print("Erro ao efetuar login")

    page.wait_for_timeout(5000)
    context.close()
    browser.close()
