from enum import Enum

class EstadoReserva(str, Enum):
    PENDIENTE = "pendiente"
    CONFIRMADA = "confirmada"
    CANCELADA = "cancelada"
    COMPLETADA = "completada"

class EstadoPago(str, Enum):
    PENDIENTE = "pendiente"
    COMPLETADO = "completado"
    RECHAZADO = "rechazado"