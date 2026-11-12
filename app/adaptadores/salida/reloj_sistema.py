from datetime import date

from app.nucleo.puertos import Reloj


class RelojSistema(Reloj):
    """Adaptador de salida: implementa el puerto Reloj con la fecha del sistema.
    En las pruebas se reemplaza por otro adaptador (RelojFijoStub)."""

    def hoy(self) -> date:
        return date.today()
