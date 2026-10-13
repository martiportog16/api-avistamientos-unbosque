# API de Avistamientos de Aves

API REST para registrar los avistamientos de aves que la gente observa en el campo. Permite crear, consultar, actualizar y eliminar avistamientos (especie, lugar, fecha y observador) y guardarlos en una base de datos, para llevar un registro ordenado en lugar de apuntes sueltos.

Trabajo individual de Ingeniería de Software 2.

## Características principales

- Registrar, listar, consultar, actualizar y eliminar avistamientos.
- Respuestas en JSON con el código de estado HTTP correcto (200, 201, 204, 400, 404).
- Validación de datos: si falta algún campo, responde 400.
- Datos guardados en una base de datos SQLite que se crea sola.
- Resumen de cuántos avistamientos hay por especie (bonus).
- Pruebas automáticas de los endpoints (bonus).

## Tecnologías utilizadas

- **Python 3.10+**
- **FastAPI** (framework de la API) y **Uvicorn** (servidor)
- **Pydantic** (validación de datos)
- **SQLite** 
- **pytest** y **httpx** (pruebas)
- **Git y GitHub**

**IA utilizada:** Claude (modelo Sonnet 5.5) como apoyo para estructurar y explicar el código. Hice mis propias pruebas para entender y explicar el código entregado.

## Instalación y ejecución

Requisitos: Python 3.10 o superior (probado con Python 3.13) y Git.

```bash
git clone https://github.com/martiportog16/api-avistamientos-unbosque.git
cd api-avistamientos-unbosque

# Crear y activar el entorno virtual
python -m venv venv
# Windows (CMD o PowerShell):
venv\Scripts\activate
# Mac / Linux:
source venv/bin/activate

# Instalar dependencias y ejecutar
pip install -r requirements.txt
uvicorn app.main:app --reload
```

- La API queda en http://127.0.0.1:8000
- Documentación interactiva para probar los endpoints desde el navegador: http://127.0.0.1:8000/docs
- La base de datos (`avistamientos.db`) se crea sola al iniciar.
- En Mac/Linux puede ser `python3` en lugar de `python`.

### Pruebas

```bash
pytest
```

## Modelo: avistamiento

| Campo | Tipo | Descripción |
|---|---|---|
| id | entero | Lo asigna el sistema |
| especie | texto | Nombre de la especie, ej. "colibrí" |
| lugar | texto | Dónde se observó |
| fecha | texto | Formato AAAA-MM-DD |
| observador | texto | Quién lo registró |

## Endpoints

| Método | Ruta | Respuestas |
|---|---|---|
| GET | `/avistamientos` | 200 |
| GET | `/avistamientos/{id}` | 200, 404 |
| POST | `/avistamientos` | 201, 400 |
| PUT | `/avistamientos/{id}` | 200, 400, 404 |
| DELETE | `/avistamientos/{id}` | 204, 404 |
| GET | `/avistamientos/resumen` | 200 (bonus) |

> Los ejemplos usan sintaxis de bash. En Windows, ejecútalos en **Git Bash** (se instala junto con Git) o usa la página `/docs`.

### Listar todos
```bash
curl http://127.0.0.1:8000/avistamientos
```

### Ver uno
```bash
curl http://127.0.0.1:8000/avistamientos/1
```

### Registrar
```bash
curl -X POST http://127.0.0.1:8000/avistamientos \
  -H "Content-Type: application/json" \
  -d '{"especie":"colibri","lugar":"Casa Fernando,"fecha":"2026-03-03","observador":"Fernando"}'
```
Respuesta: `201` con el avistamiento creado. Si faltan datos o se coloca un formato distinto de fecha: `400`.

### Actualizar
```bash
curl -X PUT http://127.0.0.1:8000/avistamientos/1 \
  -H "Content-Type: application/json" \
  -d '{"especie":"colibri","lugar":"Casa Martin","fecha":"2026-04-04","observador":"Martin"}'
```

### Eliminar
```bash
curl -X DELETE http://127.0.0.1:8000/avistamientos/1
```
Respuesta: `204` sin contenido, o `404` si no existe.

### Resumen por especie (bonus)
```bash
curl http://127.0.0.1:8000/avistamientos/resumen
```
Ejemplo de respuesta: `[{"especie":"colibri","total":3}]`

## Estructura del proyecto

```
app/
  database.py   conexión y tabla SQLite
  schemas.py    modelos y validación de datos
  main.py       endpoints
tests/          pruebas de los endpoints
requirements.txt
pytest.ini
```

## Autor

**Martin Daniel Porto Gutierrez**, estudiante de Ingeniería de Sistemas-Universidad El Bosque
GitHub: [@martiportog16](https://github.com/martiportog16)