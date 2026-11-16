
from fastapi import FastAPI

app = FastAPI(
    title="API - Divulgação de Serviços de Informática",
    description="API para disponibilizar os serviços de montagem e manutenção de computadores.",
    version="1.0.0"
)


@app.get("/")
def inicio():
    return {
        "mensagem": "API de divulgação de serviços de informática funcionando!"
    }


@app.get("/status")
def status():
    return {
        "status": "online"
    }
