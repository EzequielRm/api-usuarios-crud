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

Configura una clave secreta para firmar los tokens (usa una clave aleatoria y mantenla privada):

En Windows PowerShell:
```powershell
$env:JWT_SECRET_KEY = "<clave-aleatoria-larga>"
```

En Windows CMD:
```cmd
set JWT_SECRET_KEY=<clave-aleatoria-larga>
```

Luego inicia la API:
```bash
uvicorn main:app --reload
```

La aplicación queda disponible en:
- http://127.0.0.1:8000

La documentación interactiva queda en:
- http://127.0.0.1:8000/docs
- http://127.0.0.1:8000/redoc

## Docker

Con Docker Desktop instalado, desde la raíz del proyecto configura la clave JWT y levanta la API:

En Windows CMD:
```cmd
set JWT_SECRET_KEY=una-clave-local-larga
docker compose up --build
```

En PowerShell:
```powershell
$env:JWT_SECRET_KEY = "una-clave-local-larga"
docker compose up --build
```

La API queda disponible en `http://localhost:8000`. Compose guarda SQLite en un volumen persistente llamado `usuarios_data`, así que los datos sobreviven a la recreación del contenedor. Para detenerlo, pulsa `Ctrl+C` o ejecuta `docker compose down`. No subas una clave real al repositorio; en Render configúrala como variable de entorno del servicio.

## Endpoints

| Método | Endpoint | Descripción |
|---|---|---|
| POST | `/usuarios/` | Crear un usuario |
| GET | `/usuarios/` | Listar usuarios |
| GET | `/usuarios/{usuario_id}` | Obtener un usuario por ID |
| PUT | `/usuarios/{usuario_id}` | Actualizar un usuario |
| DELETE | `/usuarios/{usuario_id}` | Eliminar un usuario |
| POST | `/token` | Iniciar sesión y obtener un JWT |

El registro solicita `nombre`, `apellido`, `email` y `password` (mínimo 8 caracteres). Para iniciar sesión, envía `username` con el email y `password` como formulario a `/token`. Las rutas de consulta, actualización y eliminación requieren un token bearer; en `/docs`, usa **Authorize** para iniciar sesión. Los tokens expiran en 30 minutos.

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
