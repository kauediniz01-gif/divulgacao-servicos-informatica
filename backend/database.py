import os
import sqlite3
from pathlib import Path

from psycopg.rows import dict_row
from psycopg_pool import ConnectionPool

CAMINHO_BANCO = Path(__file__).parent / "database.db"
DATABASE_URL = os.getenv("DATABASE_URL")

# Mantém conexões PostgreSQL reutilizáveis no ambiente hospedado.
# O limite reduz a quantidade de conexões simultâneas abertas no Supabase.
pool = (
    ConnectionPool(
        conninfo=DATABASE_URL,
        min_size=1,
        max_size=5,
        timeout=10,
        kwargs={"row_factory": dict_row},
        open=False,
    )
    if DATABASE_URL
    else None
)


def iniciar_pool():
    if pool is not None:
        pool.open(wait=True, timeout=10)


def encerrar_pool():
    if pool is not None:
        pool.close()


def conectar():
    if pool is not None:
        return pool.getconn()

    conexao = sqlite3.connect(CAMINHO_BANCO)
    conexao.row_factory = sqlite3.Row
    return conexao


def liberar_conexao(conexao):
    if pool is not None:
        pool.putconn(conexao)
    else:
        conexao.close()
