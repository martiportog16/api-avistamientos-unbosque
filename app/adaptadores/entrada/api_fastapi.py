"""Adaptador de entrada: expone el servicio del núcleo como API REST con FastAPI.

Traduce JSON <-> modelo del núcleo y errores del núcleo <-> códigos HTTP.
No contiene reglas de negocio ni SQL. No crea sus dependencias:
recibe el servicio ya armado desde app/main.py.
"""
from dataclasses import asdict

from fastapi import FastAPI, HTTPException, Response, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.adaptadores.entrada.esquemas import AvistamientoIn, AvistamientoOut
from app.nucleo.errores import AvistamientoNoEncontrado
from app.nucleo.modelo import Avistamiento
from app.nucleo.servicio import ServicioAvistamientos


def crear_app(servicio: ServicioAvistamientos) -> FastAPI:
    app = FastAPI(title="API de Avistamientos de Aves")

    NO_ENCONTRADO = "Avistamiento no encontrado"

    # Si falta por completo una llave en el JSON (ej. no envían "observador"),
    # responde 400 indicando qué campo falló.
    @app.exception_handler(RequestValidationError)
    async def datos_invalidos(request, exc):
        errores = exc.errors()
        campo = errores[0]["loc"][-1] if errores and "loc" in errores[0] else "datos"
        return JSONResponse(
            status_code=400,
            content={"detail": f"El campo '{campo}' es obligatorio o inválido"},
        )

    @app.get("/avistamientos", response_model=list[AvistamientoOut])
    def listar():
        return [asdict(a) for a in servicio.listar()]

    # BONUS: debe ir ANTES de /avistamientos/{id}, si no FastAPI
    # interpretaría la palabra "resumen" como un id.
    @app.get("/avistamientos/resumen")
    def resumen():
        return [{"especie": e, "total": t} for e, t in servicio.resumen()]

    @app.get("/avistamientos/{id}", response_model=AvistamientoOut)
    def ver(id: int):
        try:
            return asdict(servicio.ver(id))
        except AvistamientoNoEncontrado:
            raise HTTPException(status_code=404, detail=NO_ENCONTRADO)

    @app.post("/avistamientos", response_model=AvistamientoOut, status_code=status.HTTP_201_CREATED)
    def crear(datos: AvistamientoIn):
        try:
            return asdict(servicio.crear(Avistamiento(**datos.model_dump())))
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))

    @app.put("/avistamientos/{id}", response_model=AvistamientoOut)
    def actualizar(id: int, datos: AvistamientoIn):
        try:
            return asdict(servicio.actualizar(id, Avistamiento(**datos.model_dump())))
        except ValueError as e:
            raise HTTPException(status_code=400, detail=str(e))
        except AvistamientoNoEncontrado:
            raise HTTPException(status_code=404, detail=NO_ENCONTRADO)

    @app.delete("/avistamientos/{id}", status_code=status.HTTP_204_NO_CONTENT)
    def eliminar(id: int):
        try:
            servicio.eliminar(id)
        except AvistamientoNoEncontrado:
            raise HTTPException(status_code=404, detail=NO_ENCONTRADO)
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    return app
