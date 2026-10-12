import os
import sqlite3

DB_PATH = os.environ.get("AVISTAMIENTOS_DB", "avistamientos.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS avistamientos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            especie TEXT NOT NULL,
            lugar TEXT NOT NULL,
            fecha TEXT NOT NULL,
            observador TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()