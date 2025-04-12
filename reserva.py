from fastapi.routing import APIRouter
from fastapi.exceptions import HTTPException
from models import Reserva, ReservaBase, Pago, PagoBase, Cochera, Usuario
from database import SessionDep
from sqlmodel import select
from datetime import datetime, timezone
from decimal import Decimal

route = APIRouter(prefix="/reserva")

@route.post("/")
async def create_reserva(reserva: ReservaBase, session: SessionDep):
    # Verificar que la cochera existe y está disponible
    cochera = session.get(Cochera, reserva.cochera_id)
    if not cochera:
        raise HTTPException(status_code=404, detail="Cochera no encontrada")
    if not cochera.disponible:
        raise HTTPException(status_code=400, detail="Cochera no disponible")
    
    # Verificar que el usuario existe
    usuario = session.get(Usuario, reserva.usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Calcular duración y monto
    duracion_horas = (reserva.fecha_fin - reserva.fecha_inicio).total_seconds() / 3600
    monto = round(Decimal(duracion_horas) * cochera.precio_hora, 2)
    comision = round(monto * Decimal('0.10'), 2)  # 10% de comisión
    
    # Crear la reserva
    db_reserva = Reserva.model_validate(reserva)
    session.add(db_reserva)
    session.commit()
    session.refresh(db_reserva)
    
    # Crear el pago asociado con zona horaria UTC
    pago = PagoBase(
        monto=monto,
        comision=comision,
        reserva_id=db_reserva.id,
        fecha=datetime.now(timezone.utc)
    )
    db_pago = Pago.model_validate(pago)
    session.add(db_pago)
    session.commit()
    session.refresh(db_pago)
    
    return {
        "reserva": db_reserva,
        "pago": db_pago
    }

@route.get("/{reserva_id}")
async def get_reserva(reserva_id: str, session: SessionDep):
    reserva = session.get(Reserva, reserva_id)
    if not reserva:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    return reserva

@route.get("/")
async def get_reservas(session: SessionDep, skip: int = 0, limit: int = 100):
    reservas = session.exec(select(Reserva).offset(skip).limit(limit)).all()
    return reservas