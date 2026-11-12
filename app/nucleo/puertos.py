"""Puertos del hexágono (Cockburn, 2005).

Un puerto es un contrato que define el NÚCLEO para hablar con el exterior.
El núcleo solo conoce estas interfaces; las implementaciones concretas
(adaptadores) viven en app/adaptadores y dependen de este archivo, nunca
al revés.
"""
from abc import ABC, abstractmethod
from datetime import date
from typing import Optional

from app.nucleo.modelo import Avistamiento


class Reloj(ABC):
    """Puerto de salida: le da al núcleo la fecha actual."""

    @abstractmethod
    def hoy(self) -> date:
        """Devuelve la fecha de hoy."""


class RepositorioAvistamientos(ABC):
    """Puerto de salida: guardar y recuperar avistamientos.
    El núcleo no sabe si detrás hay SQLite, PostgreSQL o una lista en memoria."""

    @abstractmethod
    def listar(self) -> list[Avistamiento]:
        """Devuelve todos los avistamientos."""

    @abstractmethod
    def obtener(self, id: int) -> Optional[Avistamiento]:
        """Devuelve el avistamiento o None si no existe."""

    @abstractmethod
    def guardar(self, avistamiento: Avistamiento) -> Avistamiento:
        """Guarda uno nuevo y lo devuelve con el id asignado."""

    @abstractmethod
    def actualizar(self, avistamiento: Avistamiento) -> bool:
        """Devuelve False si el id no existe."""

    @abstractmethod
    def eliminar(self, id: int) -> bool:
        """Devuelve False si el id no existe."""

    @abstractmethod
    def contar_por_especie(self) -> list[tuple[str, int]]:
        """Pares (especie, total)."""
