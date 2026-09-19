from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite:///./usuarios.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def inicializar_db():
    Base.metadata.create_all(bind=engine)

    with engine.begin() as conn:
        columnas = conn.execute(text("PRAGMA table_info(usuarios)")).fetchall()
        if columnas and not any(columna[1] == "apellido" for columna in columnas):
            conn.execute(text("DROP TABLE usuarios"))
            Base.metadata.create_all(bind=engine)

