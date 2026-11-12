"""Puertos del hexágono (Cockburn, 2005).

Un puerto es un contrato que define el NÚCLEO para hablar con el exterior.
El núcleo solo conoce estas interfaces; las implementaciones concretas
(adaptadores) viven en app/adaptadores y dependen de este archivo, nunca
al revés.
"""
from abc import ABC, abstractmethod
from datetime import date


class Reloj(ABC):
    """Puerto de salida: le da al núcleo la fecha actual."""

    @abstractmethod
    def hoy(self) -> date:
        ...
