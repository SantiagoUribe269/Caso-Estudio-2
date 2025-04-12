from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, SessionLocal
import uvicorn
from contextlib import asynccontextmanager
from sqlmodel import SQLModel, select
from models import Distrito, Dueno, Cochera, Usuario
from decimal import Decimal
import uuid
from datetime import datetime, timedelta

from user import route as user_router
from dueno import route as dueno_router
from pago import route as pago_router
from reserva import route as reserva_router
from distrito import route as distrito_router
from cochera import route as cochera_router

def load_initial_data():
    with SessionLocal() as session:
        try:
            # Verificar si ya existen datos para no duplicar
            existing_distrito = session.query(Distrito).filter(Distrito.nombre == "Pueblo Libre").first()
            if not existing_distrito:
                # 1. Crear Distrito
                distrito = Distrito(
                    id=uuid.uuid4(),
                    nombre="Pueblo Libre"
                )
                session.add(distrito)
                session.commit()
                session.refresh(distrito)
                
                # 2. Crear Dueño
                dueno = Dueno(
                    id=uuid.uuid4(),
                    nombre="Carlos Dueño",
                    email="carlos@example.com",
                    telefono="987654321",
                    distrito_id=distrito.id
                )
                session.add(dueno)
                session.commit()
                session.refresh(dueno)
                
                # 3. Crear Cochera
                cochera = Cochera(
                    id=uuid.uuid4(),
                    direccion="Av. La Marina 123",
                    capacidad=2,
                    precio_hora=Decimal('10.50'),
                    disponible=True,
                    dueno_id=dueno.id
                )
                session.add(cochera)
                session.commit()
                session.refresh(cochera)
                
                # 4. Crear Usuario
                usuario = Usuario(
                    id=uuid.uuid4(),
                    nombre="Juan Usuario",
                    email="juan@example.com",
                    telefono="987654321"
                )
                session.add(usuario)
                session.commit()
        except Exception as e:
            session.rollback()
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Crear tablas
    SQLModel.metadata.create_all(engine)
    
    # Cargar datos iniciales (síncrono)
    load_initial_data()
    
    yield

app = FastAPI(
    title="KUADRA",
    description="Servicio de Cocheras KUADRA",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(dueno_router)
app.include_router(pago_router)
app.include_router(reserva_router)
app.include_router(distrito_router)
app.include_router(cochera_router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)