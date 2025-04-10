from fastapi.routing import APIRouter
from fastapi.exceptions import HTTPException
from models import Usuario, UsuarioBase
from database import SessionDep
from sqlmodel import select

route = APIRouter(
    prefix="/pago",
)

@route.get("/")
def get_pago(): pass

@route.post("/")
def verify_pago(): pass