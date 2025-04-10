from sqlmodel import Session, create_engine
from typing import Annotated
from fastapi import Depends
import os

database_url = os.getenv("DATABASE_URL") or "postgresql://postgres:postgres@localhost:5432/kuadra_db"
engine = create_engine(url=database_url) #cambiar por create_engine

####### TOOLS #######
def get_session():
    with Session(engine) as session:
        yield session
        
SessionDep = Annotated[Session, Depends(get_session)]
