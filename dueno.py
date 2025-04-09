from fastapi.routing import APIRouter
from fastapi.exceptions import HTTPException
from models import Usuario, UsuarioBase
from main import SessionDep
from sqlmodel import select

route = APIRouter(
    prefix="/dueno",
)