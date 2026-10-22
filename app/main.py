from fastapi import FastAPI, HTTPException, Response, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.database import get_connection, init_db
from app.schemas import AvistamientoIn, AvistamientoOut
from app.validador import ValidadorDeAvistamiento

app = FastAPI(title="API de Avistamientos de Aves")
validador = ValidadorDeAvistamiento()

init_db()


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
    conn = get_connection()
    filas = conn.execute("SELECT * FROM avistamientos").fetchall()
    conn.close()
    return [dict(f) for f in filas]


# BONUS: debe ir ANTES de /avistamientos/{id}, si no FastAPI
# interpretaría la palabra "resumen" como un id.
@app.get("/avistamientos/resumen")
def resumen():
    conn = get_connection()
    filas = conn.execute(
        "SELECT especie, COUNT(*) AS total FROM avistamientos GROUP BY especie"
    ).fetchall()
    conn.close()
    return [dict(f) for f in filas]


@app.get("/avistamientos/{id}", response_model=AvistamientoOut)
def ver(id: int):
    conn = get_connection()
    fila = conn.execute("SELECT * FROM avistamientos WHERE id = ?", (id,)).fetchone()
    conn.close()
    if fila is None:
        raise HTTPException(status_code=404, detail="Avistamiento no encontrado")
    return dict(fila)


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

    conn = get_connection()
    cur = conn.execute(
        "INSERT INTO avistamientos (especie, lugar, fecha, observador) VALUES (?, ?, ?, ?)",
        (datos.especie, datos.lugar, datos.fecha, datos.observador),
    )
    conn.commit()
    nuevo_id = cur.lastrowid
    conn.close()
    return {"id": nuevo_id, **datos.model_dump()}


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

    conn = get_connection()
    cur = conn.execute(
        "UPDATE avistamientos SET especie = ?, lugar = ?, fecha = ?, observador = ? WHERE id = ?",
        (datos.especie, datos.lugar, datos.fecha, datos.observador, id),
    )
    conn.commit()
    conn.close()
    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail="Avistamiento no encontrado")
    return {"id": id, **datos.model_dump()}


@app.delete("/avistamientos/{id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar(id: int):
    conn = get_connection()
    cur = conn.execute("DELETE FROM avistamientos WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail="Avistamiento no encontrado")
    return Response(status_code=status.HTTP_204_NO_CONTENT)