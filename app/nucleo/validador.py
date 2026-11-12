from datetime import datetime

from app.nucleo.puertos import Reloj


class ValidadorDeAvistamiento:
    """Regla de negocio del núcleo. No sabe qué reloj usa: lo recibe por el
    puerto Reloj (en producción RelojSistema, en pruebas RelojFijoStub)."""

    def __init__(self, reloj: Reloj):
        self.reloj = reloj

    def validar(self, especie: str, lugar: str, fecha: str, observador: str) -> None:
        # Regla 1: la especie tiene entre 3 y 50 caracteres
        if not especie or len(especie.strip()) < 3 or len(especie.strip()) > 50:
            raise ValueError("El campo 'especie' debe tener entre 3 y 50 caracteres")

        # Regla 2: el lugar no está vacío
        if not lugar or not lugar.strip():
            raise ValueError("El campo 'lugar' no puede estar vacío")

        # Regla 3: el observador no está vacío
        if not observador or not observador.strip():
            raise ValueError("El campo 'observador' no puede estar vacío")
        
        # Regla 4: la fecha tiene formato AAAA-MM-DD y no es posterior a hoy
        if not fecha or not fecha.strip():
            raise ValueError("El campo 'fecha' no puede estar vacío")

        try:
            fecha_parsed = datetime.strptime(fecha.strip(), "%Y-%m-%d").date()
        except ValueError:
            raise ValueError("El campo 'fecha' debe tener el formato AAAA-MM-DD")

        if fecha_parsed > self.reloj.hoy():
            raise ValueError("El campo 'fecha' no puede ser posterior a hoy")