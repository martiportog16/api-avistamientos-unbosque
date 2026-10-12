from fastapi import FastAPI, HTTPException, Response, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.database import get_connection, init_db
from app.schemas import AvistamientoIn, AvistamientoOut

app = FastAPI(title="API de Avistamientos de Aves")

init_db()


# FastAPI responde 422 por defecto cuando faltan datos.
# El enunciado pide 400, por eso se cambia aquí.
@app.exception_handler(RequestValidationError)
async def datos_invalidos(request, exc):
    return JSONResponse(status_code=400, content={"detail": "Faltan datos o son inválidos"})


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