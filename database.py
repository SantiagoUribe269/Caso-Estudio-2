from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.orm import sessionmaker
from typing import Annotated
from fastapi import Depends
import os

# Configuración de la base de datos
database_url = os.getenv("DATABASE_URL") or "postgresql://postgres:postgres@localhost:5432/kuadra_db"
engine = create_engine(database_url, echo=True)

# SessionLocal para operaciones normales
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Función para inyección de dependencias (FastAPI)
def get_session():
    with Session(engine) as session:
        yield session

# Tipo para inyección de dependencias
SessionDep = Annotated[Session, Depends(get_session)]