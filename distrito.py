from fastapi.routing import APIRouter
from fastapi.exceptions import HTTPException
from models import Distrito, DistritoBase
from database import SessionDep
from sqlmodel import select

route = APIRouter(prefix="/distrito")

@route.post("/")
async def create_distrito(distrito: DistritoBase, session: SessionDep):
    db_distrito = Distrito.model_validate(distrito)
    session.add(db_distrito)
    session.commit()
    session.refresh(db_distrito)
    return db_distrito

@route.get("/")
async def get_distritos(session: SessionDep):
    distritos = session.exec(select(Distrito)).all()
    return distritos