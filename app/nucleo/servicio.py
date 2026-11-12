"""Servicio de aplicación del núcleo: los casos de uso de la API.

Es el puerto de entrada del hexágono: cualquier adaptador de entrada
(FastAPI hoy, una consola o una prueba mañana) maneja la aplicación
llamando a estos métodos. Solo depende de otros elementos del núcleo:
el modelo, el validador y los puertos de salida.
"""
from app.nucleo.errores import AvistamientoNoEncontrado
from app.nucleo.modelo import Avistamiento
from app.nucleo.puertos import RepositorioAvistamientos
from app.nucleo.validador import ValidadorDeAvistamiento


class ServicioAvistamientos:
    def __init__(self, repositorio: RepositorioAvistamientos, validador: ValidadorDeAvistamiento):
        self.repositorio = repositorio
        self.validador = validador

    def listar(self) -> list[Avistamiento]:
        return self.repositorio.listar()

    def ver(self, id: int) -> Avistamiento:
        avistamiento = self.repositorio.obtener(id)
        if avistamiento is None:
            raise AvistamientoNoEncontrado(id)
        return avistamiento

    def crear(self, avistamiento: Avistamiento) -> Avistamiento:
        self._validar(avistamiento)  # lanza ValueError si no cumple la regla
        return self.repositorio.guardar(avistamiento)

    def actualizar(self, id: int, avistamiento: Avistamiento) -> Avistamiento:
        self._validar(avistamiento)
        avistamiento.id = id
        if not self.repositorio.actualizar(avistamiento):
            raise AvistamientoNoEncontrado(id)
        return avistamiento

    def eliminar(self, id: int) -> None:
        if not self.repositorio.eliminar(id):
            raise AvistamientoNoEncontrado(id)

    def resumen(self) -> list[tuple[str, int]]:
        return self.repositorio.contar_por_especie()

    def _validar(self, a: Avistamiento) -> None:
        self.validador.validar(
            especie=a.especie, lugar=a.lugar, fecha=a.fecha, observador=a.observador
        )
