from dataclasses import asdict

from fastapi import FastAPI, HTTPException, Response, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.adaptadores.salida.reloj_sistema import RelojSistema
from app.adaptadores.salida.repositorio_sqlite import RepositorioSQLite
from app.nucleo.errores import AvistamientoNoEncontrado
from app.nucleo.modelo import Avistamiento
from app.nucleo.servicio import ServicioAvistamientos
from app.nucleo.validador import ValidadorDeAvistamiento
from app.schemas import AvistamientoIn, AvistamientoOut

app = FastAPI(title="API de Avistamientos de Aves")
servicio = ServicioAvistamientos(
    repositorio=RepositorioSQLite(),
    validador=ValidadorDeAvistamiento(reloj=RelojSistema()),
)

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
