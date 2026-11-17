import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import conectar, liberar_conexao, iniciar_pool, encerrar_pool
from init_db import criar_tabelas
from seed import cadastrar_dados


@asynccontextmanager
async def lifespan(app: FastAPI):
    iniciar_pool()
    try:
        criar_tabelas()
        cadastrar_dados()
        yield
    finally:
        encerrar_pool()


app = FastAPI(
    title="API - Divulgação de Serviços de Informática",
    description="API para disponibilizar os serviços de montagem e manutenção de computadores.",
    version="1.0.0",
    lifespan=lifespan,
)

origens_permitidas = [
    "http://localhost:4200",
    "http://192.168.18.9:4200"
]

origens_hospedadas = os.getenv("FRONTEND_URL", "")

if origens_hospedadas:
    origens_permitidas.extend(
        origem.strip()
        for origem in origens_hospedadas.split(",")
        if origem.strip()
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=origens_permitidas,
    allow_origin_regex=r"^http://(localhost|127\.0.0.1):\d+$",
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
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


@app.get("/categorias")
def listar_categorias():
    conexao = conectar()
    try:
        categorias = conexao.execute("""
            SELECT id_categoria, nome, descricao
            FROM categorias
            ORDER BY nome
        """).fetchall()
        return [dict(categoria) for categoria in categorias]
    finally:
        liberar_conexao(conexao)


@app.get("/servicos")
def listar_servicos():
    conexao = conectar()
    try:
        servicos = conexao.execute("""
            SELECT
                s.id_servico,
                s.nome,
                s.descricao,
                s.categoria_id,
                c.nome AS categoria
            FROM servicos s
            INNER JOIN categorias c
                ON s.categoria_id = c.id_categoria
            WHERE s.ativo = 1
            ORDER BY c.nome, s.nome
        """).fetchall()
        return [dict(servico) for servico in servicos]
    finally:
        liberar_conexao(conexao)
