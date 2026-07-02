# FastAPI Todo API

API REST de tareas con autenticacion basica, CRUD completo y documentacion Swagger automatica.

## Caracteristicas

- CRUD completo de tareas (crear, listar, obtener, actualizar, eliminar)
- Autenticacion basica (usuario/contraseña)
- Base de datos SQLite
- Documentacion interactiva con Swagger UI
- Endpoint de health check
- Listo para deploy en Render

## Endpoints

| Metodo | Ruta | Descripcion |
|--------|------|-------------|
| GET | `/` | Informacion de la API |
| GET | `/health` | Health check |
| POST | `/todos` | Crear tarea |
| GET | `/todos` | Listar tareas (filtro: ?completed=true) |
| GET | `/todos/{id}` | Obtener tarea |
| PUT | `/todos/{id}` | Actualizar tarea |
| DELETE | `/todos/{id}` | Eliminar tarea |

## Uso local

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

Abrir http://localhost:8000/docs para Swagger UI.

## Credenciales por defecto

- Usuario: `admin`, Contraseña: `admin123`
- Usuario: `user`, Contraseña: `user123`

## Deploy en Render

1. Crear Web Service en Render
2. Conectar este repositorio
3. Build command: `pip install -r requirements.txt`
4. Start command: `uvicorn main:app --host=0.0.0.0 --port=$PORT`
