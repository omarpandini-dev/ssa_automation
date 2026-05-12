from fastapi import FastAPI
from aut_site import acessar_secure_page

app = FastAPI(title="Hello Word API")


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "Hello Word"}


@app.get("/imprimeNome")
def imprime_nome(p_nome: str) -> dict[str, str]:
    return {"message": f"O nome é: {p_nome}"}


@app.get("/autSite")
def aut_site() -> dict[str, str]:
    return {"message": acessar_secure_page()}
