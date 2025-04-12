from fastapi.routing import APIRouter
from fastapi.exceptions import HTTPException
from models import Dueno, DuenoBase
from database import SessionDep
from sqlmodel import select

route = APIRouter(prefix="/dueno")

@route.post("/")
async def create_dueno(dueno: DuenoBase, session: SessionDep):
    db_dueno = Dueno.model_validate(dueno)
    session.add(db_dueno)
    session.commit()
    session.refresh(db_dueno)
    return db_dueno

@route.get("/{dueno_id}")
async def get_dueno(dueno_id: str, session: SessionDep):
    dueno = session.get(Dueno, dueno_id)
    if not dueno:
        raise HTTPException(status_code=404, detail="Dueño no encontrado")
    return dueno