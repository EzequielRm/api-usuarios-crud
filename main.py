import os
from datetime import datetime, timedelta, timezone

import jwt
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pwdlib import PasswordHash
from sqlalchemy.orm import Session
from base_de_datos import SessionLocal, engine, inicializar_db
import modelos, schemas

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("Debes configurar la variable de entorno JWT_SECRET_KEY")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
password_hash = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

inicializar_db()

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def crear_access_token(usuario_id: int) -> str:
    expiracion = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode({"sub": str(usuario_id), "exp": expiracion}, SECRET_KEY, algorithm=ALGORITHM)

def obtener_usuario_actual(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credenciales_invalidas = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        usuario_id = int(payload.get("sub", ""))
    except (jwt.InvalidTokenError, TypeError, ValueError):
        raise credenciales_invalidas

    usuario = db.query(modelos.Usuario).filter(modelos.Usuario.id == usuario_id).first()
    if usuario is None:
        raise credenciales_invalidas
    return usuario

@app.post("/token", response_model=schemas.Token)
def iniciar_sesion(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    usuario = db.query(modelos.Usuario).filter(modelos.Usuario.email == form_data.username).first()
    if usuario is None or usuario.password_hash is None or not password_hash.verify(form_data.password, usuario.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {
        "access_token": crear_access_token(usuario.id),
        "token_type": "bearer",
    }
        
@app.post("/usuarios/", response_model=schemas.UsuarioRespuesta)
async def crear_usuario(usuario: schemas.UsuarioCrear, db: Session = Depends(get_db)):
    
    existe = db.query(modelos.Usuario).filter(modelos.Usuario.email == usuario.email).first()
    if existe:
        raise HTTPException(status_code=400, detail="El email ya está registrado")
    
    db_usuario = modelos.Usuario(
        nombre=usuario.nombre,
        apellido=usuario.apellido,
        email=usuario.email,
        password_hash=password_hash.hash(usuario.password),
    )
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

@app.get("/usuarios/", response_model=list[schemas.UsuarioRespuesta], dependencies=[Depends(obtener_usuario_actual)])
def leer_usuarios(db: Session = Depends(get_db)):
    return db.query(modelos.Usuario).all()

@app.get("/usuarios/{usuario_id}", response_model=schemas.UsuarioRespuesta, dependencies=[Depends(obtener_usuario_actual)])
async def leer_usuario_id(usuario_id: int, db: Session = Depends(get_db)):
    db_usuario = db.query(modelos.Usuario).filter(modelos.Usuario.id == usuario_id).first()
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_usuario

@app.put("/usuarios/{usuario_id}", response_model=schemas.UsuarioRespuesta, dependencies=[Depends(obtener_usuario_actual)])
async def actualizar_usuario(usuario_id: int, usuario: schemas.UsuarioActualizar, db: Session = Depends(get_db)):
    db_usuario = db.query(modelos.Usuario).filter(modelos.Usuario.id == usuario_id).first()
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    db_usuario.nombre = usuario.nombre
    db_usuario.apellido = usuario.apellido
    db_usuario.email = usuario.email
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

@app.delete("/usuarios/{usuario_id}", response_model=schemas.MensajeRespuesta, dependencies=[Depends(obtener_usuario_actual)])
async def eliminar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    db_usuario = db.query(modelos.Usuario).filter(modelos.Usuario.id == usuario_id).first()
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    db.delete(db_usuario)
    db.commit()
    return schemas.MensajeRespuesta(mensaje="Usuario eliminado exitosamente")
