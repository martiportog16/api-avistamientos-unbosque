"""Adaptador de salida: implementa el puerto RepositorioAvistamientos con SQLite.
Todo el SQL de la aplicación vive aquí y en ningún otro lugar."""
import os
import sqlite3
from typing import Optional

from app.nucleo.modelo import Avistamiento
from app.nucleo.puertos import RepositorioAvistamientos

DB_PATH = os.environ.get("AVISTAMIENTOS_DB", "avistamientos.db")


def get_connection(db_path: str = None):
    conn = sqlite3.connect(db_path or DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path: str = None):
    conn = get_connection(db_path)
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


def _a_modelo(fila) -> Avistamiento:
    """Traduce una fila de SQLite al modelo del núcleo."""
    return Avistamiento(
        id=fila["id"],
        especie=fila["especie"],
        lugar=fila["lugar"],
        fecha=fila["fecha"],
        observador=fila["observador"],
    )


class RepositorioSQLite(RepositorioAvistamientos):
    def __init__(self, db_path: str = None):
        self.db_path = db_path or DB_PATH
        init_db(self.db_path)

    def listar(self) -> list[Avistamiento]:
        conn = get_connection(self.db_path)
        filas = conn.execute("SELECT * FROM avistamientos").fetchall()
        conn.close()
        return [_a_modelo(f) for f in filas]

    def obtener(self, id: int) -> Optional[Avistamiento]:
        conn = get_connection(self.db_path)
        fila = conn.execute("SELECT * FROM avistamientos WHERE id = ?", (id,)).fetchone()
        conn.close()
        return _a_modelo(fila) if fila else None

    def guardar(self, avistamiento: Avistamiento) -> Avistamiento:
        conn = get_connection(self.db_path)
        cur = conn.execute(
            "INSERT INTO avistamientos (especie, lugar, fecha, observador) VALUES (?, ?, ?, ?)",
            (avistamiento.especie, avistamiento.lugar, avistamiento.fecha, avistamiento.observador),
        )
        conn.commit()
        nuevo_id = cur.lastrowid
        conn.close()
        avistamiento.id = nuevo_id
        return avistamiento

    def actualizar(self, avistamiento: Avistamiento) -> bool:
        conn = get_connection(self.db_path)
        cur = conn.execute(
            "UPDATE avistamientos SET especie = ?, lugar = ?, fecha = ?, observador = ? WHERE id = ?",
            (avistamiento.especie, avistamiento.lugar, avistamiento.fecha,
             avistamiento.observador, avistamiento.id),
        )
        conn.commit()
        conn.close()
        return cur.rowcount > 0

    def eliminar(self, id: int) -> bool:
        conn = get_connection(self.db_path)
        cur = conn.execute("DELETE FROM avistamientos WHERE id = ?", (id,))
        conn.commit()
        conn.close()
        return cur.rowcount > 0

    def contar_por_especie(self) -> list[tuple[str, int]]:
        conn = get_connection(self.db_path)
        filas = conn.execute(
            "SELECT especie, COUNT(*) AS total FROM avistamientos GROUP BY especie"
        ).fetchall()
        conn.close()
        return [(f["especie"], f["total"]) for f in filas]
