from pydantic import BaseModel, ConfigDict

class UsuarioCrear(BaseModel):
    nombre: str
    apellido: str
    email: str

class UsuarioActualizar(BaseModel):
    nombre: str
    apellido: str
    email: str
    
class UsuarioRespuesta(BaseModel):
    model_config = ConfigDict(from_attributes=True)
            
    id: int
    nombre: str
    apellido: str
    email: str

class MensajeRespuesta(BaseModel):
    mensaje: str