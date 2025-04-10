from fastapi.routing import APIRouter
from fastapi.exceptions import HTTPException
from models import Usuario
from database import SessionDep
from sqlmodel import select

route = APIRouter(
    prefix="/user",
)

@route.get("/")
async def get_user(session: SessionDep):
    users = session.exec(select(Usuario).limit(100)).all()
    return users
    
@route.get("/{user_id}")
async def get_user(user_id: str, session: SessionDep):
    user = session.get(Usuario, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@route.post("/")
async def new_user(user: Usuario, session: SessionDep):
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

@route.put("/{user_id}")
async def update_user(user_id: str, user_update: Usuario, session: SessionDep):
    user = session.get(Usuario, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    for key, value in user_update.model_dump(exclude_unset=True).items():
        setattr(user, key, value)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user
    
@route.patch("/")
async def update_partial_user(session: SessionDep): pass

@route.delete("/{user_id}")
async def delete_user(user_id: str, session: SessionDep):
    user = session.get(Usuario, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    session.delete(user)
    session.commit()
    return {"message": "User deleted successfully"}
    