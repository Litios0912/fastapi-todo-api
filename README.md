# FastAPI Todo API

API REST de tareas con autenticacion basica, CRUD completo, base de datos SQLite y documentacion Swagger automatica. Lista para desplegar en Render.

[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688?logo=fastapi)](https://fastapi.tiangolo.com)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-red)](https://sqlalchemy.org)
[![Swagger](https://img.shields.io/badge/Swagger-UI-85EA2D?logo=swagger)](https://swagger.io)
[![Deploy](https://img.shields.io/badge/Render-Ready-46E3B7?logo=render)](https://render.com)

## Caracteristicas

- CRUD completo de tareas (crear, listar, obtener, actualizar, eliminar)
- Autenticacion basica por usuario/contraseña
- Base de datos SQLite (intercambiable por PostgreSQL)
- Documentacion interactiva con Swagger UI y ReDoc
- Filtro de tareas por estado (completadas/pendientes)
- Endpoint de health check
- Arquitectura modular y limpia

## Endpoints

| Metodo | Ruta | Auth | Descripcion |
|---|---|---|---|
| GET | `/` | No | Informacion de la API |
| GET | `/health` | No | Health check |
| GET | `/docs` | No | Swagger UI |
| POST | `/todos` | Basic | Crear tarea |
| GET | `/todos` | Basic | Listar tareas |
| GET | `/todos?completed=true` | Basic | Filtrar por completadas |
| GET | `/todos/{id}` | Basic | Obtener tarea por ID |
| PUT | `/todos/{id}` | Basic | Actualizar tarea |
| DELETE | `/todos/{id}` | Basic | Eliminar tarea |

## Instalacion y uso

```bash
git clone https://github.com/Litios0912/fastapi-todo-api.git
cd fastapi-todo-api
pip install -r requirements.txt
uvicorn main:app --reload
```

Abrir `http://localhost:8000/docs` para la documentacion interactiva.

## Credenciales por defecto

| Usuario | Contraseña |
|---|---|
| `admin` | `admin123` |
| `user` | `user123` |

## Ejemplos con curl

```bash
# Crear tarea
curl -u admin:admin123 -X POST http://localhost:8000/todos \
  -H "Content-Type: application/json" \
  -d '{"title": "Aprender FastAPI", "description": "Hacer el tutorial oficial"}'

# Listar tareas
curl -u admin:admin123 http://localhost:8000/todos

# Listar solo completadas
curl -u admin:admin123 "http://localhost:8000/todos?completed=true"

# Actualizar tarea
curl -u admin:admin123 -X PUT http://localhost:8000/todos/1 \
  -H "Content-Type: application/json" \
  -d '{"completed": true}'

# Eliminar tarea
curl -u admin:admin123 -X DELETE http://localhost:8000/todos/1
```

## Despliegue en Render

1. Crear Web Service en [render.com](https://render.com)
2. Conectar este repositorio
3. Build command: `pip install -r requirements.txt`
4. Start command: `uvicorn main:app --host=0.0.0.0 --port=$PORT`
5. Opcional: agregar `DATABASE_URL` para usar PostgreSQL en vez de SQLite

## Variables de entorno

| Variable | Default | Descripcion |
|---|---|---|
| `DATABASE_URL` | `sqlite:///./todos.db` | URL de base de datos |

## Licencia

MIT
