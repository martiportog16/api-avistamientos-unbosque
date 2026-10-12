import os
import tempfile

# La base temporal se define ANTES de importar la app,
# así las pruebas no tocan tu base de datos real.
_tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
_tmp.close()
os.environ["AVISTAMIENTOS_DB"] = _tmp.name

from fastapi.testclient import TestClient  # noqa: E402
from app.main import app  # noqa: E402

client = TestClient(app)

DATOS = {"especie": "colibrí", "lugar": "Bogotá", "fecha": "2026-09-20", "observador": "Ana"}


def test_listar_200():
    assert client.get("/avistamientos").status_code == 200


def test_crear_201():
    r = client.post("/avistamientos", json=DATOS)
    assert r.status_code == 201
    assert r.json()["id"] > 0


def test_crear_sin_observador_400():
    datos = {k: v for k, v in DATOS.items() if k != "observador"}
    assert client.post("/avistamientos", json=datos).status_code == 400


def test_ver_200_y_404():
    creado = client.post("/avistamientos", json=DATOS).json()
    assert client.get(f"/avistamientos/{creado['id']}").status_code == 200
    assert client.get("/avistamientos/99999").status_code == 404


def test_actualizar_200_y_404():
    creado = client.post("/avistamientos", json=DATOS).json()
    nuevo = {**DATOS, "lugar": "Medellín"}
    r = client.put(f"/avistamientos/{creado['id']}", json=nuevo)
    assert r.status_code == 200
    assert r.json()["lugar"] == "Medellín"
    assert client.put("/avistamientos/99999", json=nuevo).status_code == 404


def test_eliminar_204_y_404():
    creado = client.post("/avistamientos", json=DATOS).json()
    assert client.delete(f"/avistamientos/{creado['id']}").status_code == 204
    assert client.delete(f"/avistamientos/{creado['id']}").status_code == 404


def test_resumen_200():
    client.post("/avistamientos", json=DATOS)
    r = client.get("/avistamientos/resumen")
    assert r.status_code == 200
    assert any(item["especie"] == "colibrí" for item in r.json())