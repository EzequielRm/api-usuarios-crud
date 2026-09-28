from pydantic import BaseModel, ConfigDict, Field

class UsuarioCrear(BaseModel):
    nombre: str
    apellido: str
    email: str
    password: str = Field(min_length=8)

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

class Token(BaseModel):
    access_token: str
    token_type: str