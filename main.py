from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from base_de_datos import SessionLocal, engine, inicializar_db
import modelos, schemas

inicializar_db()

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@app.post("/usuarios/", response_model=schemas.UsuarioRespuesta)
async def crear_usuario(usuario: schemas.UsuarioCrear, db: Session = Depends(get_db)):
    
    existe = db.query(modelos.Usuario).filter(modelos.Usuario.email == usuario.email).first()
    if existe:
        raise HTTPException(status_code=400, detail="El email ya está registrado")
    
    db_usuario = modelos.Usuario(nombre=usuario.nombre, apellido=usuario.apellido, email=usuario.email)
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

@app.get("/usuarios/", response_model=list[schemas.UsuarioRespuesta])
def leer_usuarios(db: Session = Depends(get_db)):
    return db.query(modelos.Usuario).all()

@app.get("/usuarios/{usuario_id}", response_model=schemas.UsuarioRespuesta)
async def leer_usuario_id(usuario_id: int, db: Session = Depends(get_db)):
    db_usuario = db.query(modelos.Usuario).filter(modelos.Usuario.id == usuario_id).first()
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_usuario

@app.put("/usuarios/{usuario_id}", response_model=schemas.UsuarioRespuesta)
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

@app.delete("/usuarios/{usuario_id}", response_model=schemas.MensajeRespuesta)
async def eliminar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    db_usuario = db.query(modelos.Usuario).filter(modelos.Usuario.id == usuario_id).first()
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    db.delete(db_usuario)
    db.commit()
    return schemas.MensajeRespuesta(mensaje="Usuario eliminado exitosamente")
