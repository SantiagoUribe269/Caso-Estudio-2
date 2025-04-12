from fastapi.routing import APIRouter
from fastapi.exceptions import HTTPException
from models import Pago, Reserva
from database import SessionDep
from sqlmodel import select

route = APIRouter(prefix="/pago")

@route.get("/{pago_id}")
async def get_pago(pago_id: str, session: SessionDep):
    pago = session.get(Pago, pago_id)
    if not pago:
        raise HTTPException(status_code=404, detail="Pago no encontrado")
    return pago

@route.get("/")
async def get_pagos(session: SessionDep, skip: int = 0, limit: int = 100):
    pagos = session.exec(select(Pago).offset(skip).limit(limit)).all()
    return pagos

@route.post("/{pago_id}/completar")
async def completar_pago(pago_id: str, session: SessionDep):
    pago = session.get(Pago, pago_id)
    if not pago:
        raise HTTPException(status_code=404, detail="Pago no encontrado")
    
    pago.estado = "completado"
    session.add(pago)
    
    # Actualizar estado de la reserva
    reserva = session.get(Reserva, pago.reserva_id)
    if reserva:
        reserva.estado = "confirmada"
        session.add(reserva)
    
    session.commit()
    session.refresh(pago)
    return pago

@route.get("/")
async def get_pagos(session: SessionDep, skip: int = 0, limit: int = 100):
    pagos = session.exec(select(Pago).offset(skip).limit(limit)).all()
    return pagos