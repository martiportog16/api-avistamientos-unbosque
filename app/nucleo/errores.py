"""Errores del núcleo. No son errores HTTP: el adaptador de entrada decide
cómo traducirlos (por ejemplo, a un 404)."""


class AvistamientoNoEncontrado(Exception):
    pass
