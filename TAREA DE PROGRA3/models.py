# models.py
from sqlalchemy import Column, Integer, String, Boolean, Enum
from database import Base
import enum

class EstadoVuelo(enum.Enum):
    programado = "programado"
    en_vuelo = "en vuelo"
    aterrizado = "aterrizado"
    cancelado = "cancelado"

class Vuelo(Base):
    __tablename__ = 'vuelos'

    id = Column(Integer, primary_key=True, index=True)
    numero_vuelo = Column(String, unique=True, index=True)
    emergencia = Column(Boolean, default=False)
    estado = Column(Enum(EstadoVuelo), default=EstadoVuelo.programado)

class CrearVuelo(Base):
    """Clase para la creación de un vuelo sin ID (a utilizar para las peticiones de creación de vuelo)"""
    numero_vuelo: str
    emergencia: bool = False
    estado: EstadoVuelo = EstadoVuelo.programado