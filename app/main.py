"""Punto de arranque (raíz de composición).

Es el único lugar que conoce a la vez el núcleo y los adaptadores concretos:
crea los adaptadores de salida, se los entrega al servicio del núcleo por
sus puertos, y conecta el servicio al adaptador de entrada (FastAPI).
Para cambiar SQLite por otra base solo habría que cambiar una línea aquí.
"""
from app.adaptadores.entrada.api_fastapi import crear_app
from app.adaptadores.salida.reloj_sistema import RelojSistema
from app.adaptadores.salida.repositorio_sqlite import RepositorioSQLite
from app.nucleo.servicio import ServicioAvistamientos
from app.nucleo.validador import ValidadorDeAvistamiento

servicio = ServicioAvistamientos(
    repositorio=RepositorioSQLite(),
    validador=ValidadorDeAvistamiento(reloj=RelojSistema()),
)

app = crear_app(servicio)
