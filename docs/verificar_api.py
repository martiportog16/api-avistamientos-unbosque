"""Hace las 8 peticiones de la evidencia contra la API que está corriendo
(uvicorn app.main:app) e imprime una tabla con los códigos obtenidos.

Uso: con el servidor encendido, en otra terminal con el venv activo:
    python verificar_api.py
"""
import httpx

URL = "http://127.0.0.1:8000"
DATOS = {"especie": "colibrí", "lugar": "Bogotá", "fecha": "2026-09-20", "observador": "Ana"}

c = httpx.Client(base_url=URL)
filas = []


def pedir(metodo, ruta, esperado, json=None):
    r = c.request(metodo, ruta, json=json)
    cuerpo = r.text if r.text else "(sin contenido)"
    filas.append((f"{metodo} {ruta}", esperado, r.status_code, cuerpo))
    return r


creado = pedir("POST", "/avistamientos", 201, DATOS).json()
id_ = creado["id"]
pedir("POST", "/avistamientos", 400, {**DATOS, "especie": "ab"})
pedir("GET", "/avistamientos", 200)
pedir("GET", f"/avistamientos/{id_}", 200)
pedir("GET", "/avistamientos/999999", 404)
pedir("PUT", f"/avistamientos/{id_}", 200, {**DATOS, "lugar": "Medellín"})
pedir("GET", "/avistamientos/resumen", 200)
pedir("DELETE", f"/avistamientos/{id_}", 204)

print(f"\n{'Petición':34} {'Esperado':>9} {'Obtenido':>9}  ")
print("-" * 58)
for peticion, esp, obt, _ in filas:
    print(f"{peticion:34} {esp:>9} {obt:>9}  {'OK' if esp == obt else 'DIFERENTE'}")
print("\nCuerpos de respuesta:")
for peticion, _, _, cuerpo in filas:
    print(f"  {peticion}: {cuerpo[:110]}")
