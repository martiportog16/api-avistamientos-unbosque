from pydantic import BaseModel


class AvistamientoIn(BaseModel):
    """Lo que el cliente envía. El id lo asigna el sistema."""
    especie: str
    lugar: str
    fecha: str
    observador: str


class AvistamientoOut(AvistamientoIn):
    """Lo que la API devuelve: los mismos campos más el id."""
    id: int