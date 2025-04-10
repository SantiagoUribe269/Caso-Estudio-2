from sqlmodel import Field, SQLModel, Relationship, UniqueConstraint
from typing import Optional, List
from datetime import datetime
from datetime import timezone
from decimal import Decimal
from enums import EstadoPago, EstadoReserva
import uuid

########  DISTRITO MODEL ########
class DistritoBase(SQLModel):
    nombre: str = Field(unique=True, index=True)

class Distrito(DistritoBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    duenos: List["Dueno"] = Relationship(back_populates="distrito")

########  DUENO MODEL ########
class DuenoBase(SQLModel):
    nombre: str
    email: str = Field(unique=True, index=True)
    telefono: str
    distrito_id: uuid.UUID = Field(foreign_key="distrito.id")

class Dueno(DuenoBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    distrito: Distrito = Relationship(back_populates="duenos")
    cocheras: List["Cochera"] = Relationship(back_populates="dueno")

########  COCHERA MODEL ########
class CocheraBase(SQLModel):
    direccion: str
    capacidad: int
    precio_hora: Decimal = Field(max_digits=10, decimal_places=2)
    disponible: bool = Field(default=True)
    dueno_id: uuid.UUID = Field(foreign_key="dueno.id")

class Cochera(CocheraBase, table=True):
    __table_args__ = (
        UniqueConstraint("direccion", "dueno_id", name="_unique_direccion_dueno_id"),
    )
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    dueno: Dueno = Relationship(back_populates="cocheras")
    reservas: List["Reserva"] = Relationship(back_populates="cochera")
    
########  USUARIO MODEL ########
class UsuarioBase(SQLModel):
    nombre: str
    email: str = Field(unique=True, index=True)
    telefono: str

class Usuario(UsuarioBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    reservas: List["Reserva"] = Relationship(back_populates="usuario")

########  RESERVA MODEL ########
class ReservaBase(SQLModel):
    fecha_inicio: datetime
    fecha_fin: datetime
    estado: EstadoReserva = Field(default=EstadoReserva.PENDIENTE)
    cochera_id: uuid.UUID = Field(foreign_key="cochera.id")
    usuario_id: uuid.UUID = Field(foreign_key="usuario.id")

class Reserva(ReservaBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    cochera: Cochera = Relationship(back_populates="reservas")
    usuario: Usuario = Relationship(back_populates="reservas")
    pago: Optional["Pago"] = Relationship(back_populates="reserva")

########  PAGO MODEL ########
class PagoBase(SQLModel):
    monto: Decimal = Field(max_digits=10, decimal_places=2)
    comision: Decimal = Field(max_digits=10, decimal_places=2)
    fecha: datetime = Field(default_factory=lambda: datetime.now(timezone.UTC))
    estado: EstadoPago = Field(default=EstadoPago.PENDIENTE)
    reserva_id: uuid.UUID = Field(foreign_key="reserva.id", unique=True)

class Pago(PagoBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    reserva: Reserva = Relationship(back_populates="pago")