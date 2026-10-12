# API de Avistamientos de Aves

API REST para registrar avistamientos de aves. Trabajo individual de Ingeniería de Software 2. Universidad El Bosque.

**Tecnologías:** Python, FastAPI, SQLite.

**IA utilizada:** Use Claude modelo Sonnet 5.5 como apoyo para estructurar y explicar el código. 

## Requisitos

- Python 3.10 o superior
- Git

## Instalación y ejecución

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
- Documentación interactiva (probar endpoints desde el navegador): http://127.0.0.1:8000/docs
- La base de datos SQLite (`avistamientos.db`) se crea sola al iniciar.
- En Mac/Linux puede ser `python3` en lugar de `python`.

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
  -d '{"especie":"colibrí","lugar":"Parque Simón Bolívar","fecha":"2026-09-20","observador":"Ana"}'
```
Respuesta: `201` con el avistamiento creado. Si faltan datos: `400`.

### Actualizar
```bash
curl -X PUT http://127.0.0.1:8000/avistamientos/1 \
  -H "Content-Type: application/json" \
  -d '{"especie":"colibrí","lugar":"Jardín Botánico","fecha":"2026-09-21","observador":"Ana"}'
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
Ejemplo de respuesta: `[{"especie":"colibrí","total":3}]`

## Pruebas (bonus)

```bash
pytest
```

## Estructura

```
app/
  database.py   conexión y tabla SQLite
  schemas.py    modelos y validación de datos
  main.py       endpoints
tests/          pruebas de integración
```