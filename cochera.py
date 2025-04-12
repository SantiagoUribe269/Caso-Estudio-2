from fastapi.routing import APIRouter
from fastapi.exceptions import HTTPException
from models import Cochera, CocheraBase
from database import SessionDep
from sqlmodel import select

route = APIRouter(prefix="/cochera")

@route.post("/")
async def create_cochera(cochera: CocheraBase, session: SessionDep):
    db_cochera = Cochera.model_validate(cochera)
    session.add(db_cochera)
    session.commit()
    session.refresh(db_cochera)
    return db_cochera

@route.get("/")
async def get_cocheras(session: SessionDep):
    cocheras = session.exec(select(Cochera)).all()
    return cocheras

@route.get("/disponibles")
async def get_cocheras_disponibles(session: SessionDep):
    cocheras = session.exec(select(Cochera).where(Cochera.disponible == True)).all()
    return cocheras 