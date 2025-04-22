from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel

# Crear la clase base para los modelos de SQLAlchemy
Base = declarative_base()

# Definimos el modelo de vuelo
class Vuelo(Base):
    __tablename__ = "vuelos"

    id = Column(Integer, primary_key=True, index=True)
    origen = Column(String, index=True)
    destino = Column(String, index=True)
    duracion = Column(Integer)  # Duración en minutos

# Crear esquema para la entrada de nuevo vuelo
class CrearVuelo(BaseModel):
    origen: str
    destino: str
    duracion: int