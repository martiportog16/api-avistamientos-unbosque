from fastapi import FastAPI, HTTPException, Response, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.schemas import AvistamientoIn, AvistamientoOut
from dataclasses import asdict

from app.adaptadores.salida.reloj_sistema import RelojSistema
from app.adaptadores.salida.repositorio_sqlite import RepositorioSQLite
from app.nucleo.modelo import Avistamiento
from app.nucleo.validador import ValidadorDeAvistamiento

app = FastAPI(title="API de Avistamientos de Aves")
validador = ValidadorDeAvistamiento(reloj=RelojSistema())
repositorio = RepositorioSQLite()


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
    return [asdict(a) for a in repositorio.listar()]


# BONUS: debe ir ANTES de /avistamientos/{id}, si no FastAPI
# interpretaría la palabra "resumen" como un id.
@app.get("/avistamientos/resumen")
def resumen():
    return [{"especie": e, "total": t} for e, t in repositorio.contar_por_especie()]


@app.get("/avistamientos/{id}", response_model=AvistamientoOut)
def ver(id: int):
    encontrado = repositorio.obtener(id)
    if encontrado is None:
        raise HTTPException(status_code=404, detail="Avistamiento no encontrado")
    return asdict(encontrado)


@app.post("/avistamientos", response_model=AvistamientoOut, status_code=status.HTTP_201_CREATED)
def crear(datos: AvistamientoIn):
    try:
        validador.validar(
            especie=datos.especie,
            lugar=datos.lugar,
            fecha=datos.fecha,
            observador=datos.observador,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    creado = repositorio.guardar(Avistamiento(**datos.model_dump()))
    return asdict(creado)


@app.put("/avistamientos/{id}", response_model=AvistamientoOut)
def actualizar(id: int, datos: AvistamientoIn):
    try:
        validador.validar(
            especie=datos.especie,
            lugar=datos.lugar,
            fecha=datos.fecha,
            observador=datos.observador,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    if not repositorio.actualizar(Avistamiento(id=id, **datos.model_dump())):
        raise HTTPException(status_code=404, detail="Avistamiento no encontrado")
    return {"id": id, **datos.model_dump()}


@app.delete("/avistamientos/{id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar(id: int):
    if not repositorio.eliminar(id):
        raise HTTPException(status_code=404, detail="Avistamiento no encontrado")
    return Response(status_code=status.HTTP_204_NO_CONTENT)