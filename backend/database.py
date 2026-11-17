
import os
import sqlite3
from pathlib import Path

import psycopg
from psycopg.rows import dict_row

CAMINHO_BANCO = Path(__file__).parent / "database.db"


def conectar():
    database_url = os.getenv("DATABASE_URL")

    if database_url:
        return psycopg.connect(
            database_url,
            row_factory=dict_row
        )

    conexao = sqlite3.connect(CAMINHO_BANCO)
    conexao.row_factory = sqlite3.Row
    return conexao
