"""Modelo del núcleo: qué es un avistamiento, sin FastAPI, Pydantic ni SQL."""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Avistamiento:
    especie: str
    lugar: str
    fecha: str
    observador: str
    id: Optional[int] = None  # None mientras no se ha guardado
