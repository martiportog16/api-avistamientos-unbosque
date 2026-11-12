import os
import tempfile
import pytest

# La base temporal se define ANTES de importar la app,
# así las pruebas no tocan tu base de datos real.
_tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
_tmp.close()
os.environ["AVISTAMIENTOS_DB"] = _tmp.name

from fastapi.testclient import TestClient  # noqa: E402
from app.adaptadores.salida.repositorio_sqlite import get_connection  # noqa: E402
from app.main import app  # noqa: E402

client = TestClient(app)

DATOS = {
    "especie": "colibrí",
    "lugar": "Bogotá",
    "fecha": "2026-09-20",
    "observador": "Ana",
}


@pytest.fixture(autouse=True)
def limpiar_base_de_datos():
    """Garantiza independencia (Punto 7): limpia la base SQLite antes de cada prueba."""
    conn = get_connection()
    conn.execute("DELETE FROM avistamientos")
    conn.commit()
    conn.close()


def test_listar_avistamientos_retorna_200_y_cuerpo_esperado():
    # Arrange
    client.post("/avistamientos", json=DATOS)

    # Act
    r = client.get("/avistamientos")

    # Assert
    assert r.status_code == 200
    cuerpo = r.json()
    assert len(cuerpo) == 1
    assert cuerpo[0]["especie"] == "colibrí"
    assert cuerpo[0]["lugar"] == "Bogotá"


def test_crear_avistamiento_valido_retorna_201_y_persiste_en_get():
    # Act
    r_post = client.post("/avistamientos", json=DATOS)

    # Assert: estado y cuerpo completo
    assert r_post.status_code == 201
    creado = r_post.json()
    assert creado["id"] > 0
    assert creado["especie"] == "colibrí"
    assert creado["lugar"] == "Bogotá"
    assert creado["fecha"] == "2026-09-20"
    assert creado["observador"] == "Ana"

    # Assert de efecto (Punto 6): un GET al nuevo id debe devolverlo
    r_get = client.get(f"/avistamientos/{creado['id']}")
    assert r_get.status_code == 200
    assert r_get.json() == creado


def test_crear_avistamiento_con_especie_invalida_retorna_400_y_campo():
    # Arrange
    datos_invalidos = {**DATOS, "especie": "ab"}

    # Act
    r = client.post("/avistamientos", json=datos_invalidos)

    # Assert
    assert r.status_code == 400
    assert "especie" in r.json()["detail"].lower()


def test_crear_sin_observador_retorna_400():
    # Arrange
    datos = {k: v for k, v in DATOS.items() if k != "observador"}

    # Act
    r = client.post("/avistamientos", json=datos)

    # Assert
    assert r.status_code == 400
    assert "observador" in r.json()["detail"].lower()


def test_ver_avistamiento_por_id_retorna_200_si_existe_y_404_si_no_existe():
    # Arrange
    creado = client.post("/avistamientos", json=DATOS).json()

    # Act & Assert (200 y cuerpo)
    r_ok = client.get(f"/avistamientos/{creado['id']}")
    assert r_ok.status_code == 200
    assert r_ok.json()["especie"] == "colibrí"

    # Act & Assert (404)
    r_404 = client.get("/avistamientos/99999")
    assert r_404.status_code == 404


def test_actualizar_avistamiento_retorna_200_y_persiste_efecto_o_404():
    # Arrange
    creado = client.post("/avistamientos", json=DATOS).json()
    nuevo = {**DATOS, "lugar": "Medellín"}

    # Act
    r_put = client.put(f"/avistamientos/{creado['id']}", json=nuevo)

    # Assert estado, cuerpo y efecto en GET
    assert r_put.status_code == 200
    assert r_put.json()["lugar"] == "Medellín"
    r_get = client.get(f"/avistamientos/{creado['id']}")
    assert r_get.json()["lugar"] == "Medellín"

    # Assert 404 cuando el id no existe
    assert client.put("/avistamientos/99999", json=nuevo).status_code == 404


def test_actualizar_avistamiento_con_fecha_futura_retorna_400_y_campo():
    # Arrange
    creado = client.post("/avistamientos", json=DATOS).json()
    invalido = {**DATOS, "fecha": "2099-01-01"}

    # Act
    r_put = client.put(f"/avistamientos/{creado['id']}", json=invalido)

    # Assert
    assert r_put.status_code == 400
    assert "fecha" in r_put.json()["detail"].lower()


def test_eliminar_avistamiento_retorna_204_y_get_posterior_retorna_404():
    # Arrange
    creado = client.post("/avistamientos", json=DATOS).json()

    # Act
    r_del = client.delete(f"/avistamientos/{creado['id']}")

    # Assert estado y efecto (Punto 6): después del DELETE, GET debe responder 404
    assert r_del.status_code == 204
    assert client.get(f"/avistamientos/{creado['id']}").status_code == 404
    assert client.delete("/avistamientos/99999").status_code == 404


def test_resumen_retorna_200_y_conteo_por_especie():
    # Arrange
    client.post("/avistamientos", json=DATOS)

    # Act
    r = client.get("/avistamientos/resumen")

    # Assert
    assert r.status_code == 200
    assert r.json() == [{"especie": "colibrí", "total": 1}]