## 🚀 API Deployada - Live Demo
**Link:** https://api-usuarios-crud.onrender.com/docs

---
# API de usuarios con FastAPI

API REST para gestionar usuarios usando FastAPI, SQLAlchemy y SQLite.

## Descripción

Este proyecto permite:
- crear usuarios
- listar todos los usuarios
- consultar un usuario por su ID
- actualizar datos de un usuario
- eliminar un usuario
- evitar emails duplicados

## Tecnologías utilizadas

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- pytest

## Requisitos

- Python 3.10 o superior
- pip

## Instalación

1. Clona el repositorio
2. Entra en la carpeta del proyecto
3. Crea un entorno virtual:

```bash
python -m venv .venv
```

4. Activa el entorno virtual:

En Windows PowerShell:
```powershell
.\.venv\Scripts\Activate.ps1
```

En Windows CMD:
```cmd
.venv\Scripts\activate.bat
```

En macOS/Linux:
```bash
source .venv/bin/activate
```

5. Instala las dependencias:

```bash
pip install -r requirements.txt
```

## Ejecución

Desde la raíz del proyecto:

```bash
uvicorn main:app --reload
```

La aplicación queda disponible en:
- http://127.0.0.1:8000

La documentación interactiva queda en:
- http://127.0.0.1:8000/docs
- http://127.0.0.1:8000/redoc

## Endpoints

| Método | Endpoint | Descripción |
|---|---|---|
| POST | `/usuarios/` | Crear un usuario |
| GET | `/usuarios/` | Listar usuarios |
| GET | `/usuarios/{usuario_id}` | Obtener un usuario por ID |
| PUT | `/usuarios/{usuario_id}` | Actualizar un usuario |
| DELETE | `/usuarios/{usuario_id}` | Eliminar un usuario |

## Ejemplo de creación

```json
{
  "nombre": "Ana",
  "apellido": "García",
  "email": "ana@example.com"
}
```

## Validación

La API valida que el email no esté duplicado. Si ya existe, devuelve un error `400`.

## Pruebas

Ejecuta las pruebas con:

```bash
pytest -q
```

La base de datos SQLite se crea automáticamente al iniciar la aplicación.
