from fastapi.routing import APIRouter
from fastapi.exceptions import HTTPException
from models import Usuario, UsuarioBase
from database import SessionDep
from sqlmodel import select

route = APIRouter(
    prefix="/cochera",
)