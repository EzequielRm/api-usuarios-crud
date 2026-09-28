import os

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./usuarios.db")

connect_args = {"check_same_thread": False} if SQLALCHEMY_DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args=connect_args)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def inicializar_db():
    Base.metadata.create_all(bind=engine)

    with engine.begin() as conn:
        columnas = conn.execute(text("PRAGMA table_info(usuarios)")).fetchall()
        nombres_columnas = {columna[1] for columna in columnas}
        if columnas and "apellido" not in nombres_columnas:
            conn.execute(text("ALTER TABLE usuarios ADD COLUMN apellido VARCHAR"))
        if columnas and "password_hash" not in nombres_columnas:
            conn.execute(text("ALTER TABLE usuarios ADD COLUMN password_hash VARCHAR"))


