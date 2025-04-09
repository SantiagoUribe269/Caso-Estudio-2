from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import Annotated
import uvicorn
import os

from contextlib import asynccontextmanager
from sqlmodel import SQLModel, Session, create_engine

from user import route as user_router
from dueno import route as dueno_router
from pago import route as pago_router
from reserva import route as reserva_router
from distrito import route as distrito_router
from cochera import route as cochera_router


database_url = os.getenv("DATABASE_URL") | "postgresql://postgres:postgres@localhost:5432/kuadra_db"
engine = create_engine(url=database_url) #cambiar por create_engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)

####### TOOLS #######
def get_session():
    with Session(engine) as session:
        yield session
        
SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI(
    title="KUADRA",
    description="Servicio de Cocheras KUADRA",
    version="1.0.0",
    lifespan=lifespan
)

if __name__ == "__main__":
    
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
    
    uvicorn.run(app, host="0.0.0.0", port=8000)