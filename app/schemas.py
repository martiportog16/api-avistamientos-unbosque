from pydantic import BaseModel, Field


class AvistamientoIn(BaseModel):
    """Lo que el cliente envía. El id lo asigna el sistema."""
    especie: str = Field(min_length=1)
    lugar: str = Field(min_length=1)
    fecha: str = Field(pattern=r"^\d{4}-\d{2}-\d{2}$")  # AAAA-MM-DD
    observador: str = Field(min_length=1)


class AvistamientoOut(AvistamientoIn):
    """Lo que la API devuelve: los mismos campos más el id."""
    id: int