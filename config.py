from sqlmodel import SQLModel, create_engine
from dotenv import load_dotenv
import os

load_dotenv()

# Configuración de la base de datos
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/kuadra_db")

# Crear el motor de la base de datos
engine = create_engine(
    DATABASE_URL,
    echo=True,  # Set to False in production
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10
)

def init_db():
    SQLModel.metadata.create_all(engine) 