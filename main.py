from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine
import uvicorn

from contextlib import asynccontextmanager
from sqlmodel import SQLModel

from user import route as user_router
from dueno import route as dueno_router
from pago import route as pago_router
from reserva import route as reserva_router
from distrito import route as distrito_router
from cochera import route as cochera_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
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