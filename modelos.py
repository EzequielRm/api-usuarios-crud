from sqlalchemy import Column, Integer, String
from base_de_datos import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    apellido = Column(String)
    email = Column(String, unique=True, index=True)