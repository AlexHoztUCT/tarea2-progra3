# main.py
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session

from database import SessionLocal, engine
from models import CrearVuelo, Vuelo
from listadoble import ListaDobleEnlazada


app = FastAPI()


lista_vuelos = ListaDobleEnlazada()


from models import Base
Base.metadata.create_all(bind=engine)

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/vuelos/", response_model=Vuelo)
def crear_vuelo(vuelo: CrearVuelo, db: Session = Depends(get_db)):

    vuelo_db = Vuelo(**vuelo.dict())
    db.add(vuelo_db)
    lista_vuelos.insertar_al_final(vuelo_db)

    db.commit()
    db.refresh(vuelo_db)
    return vuelo_db

@app.get("/vuelos/")
def obtener_vuelos(db: Session = Depends(get_db)):
    vuelos = lista_vuelos.listar_vuelos()  
    return vuelos

@app.delete("/vuelos/{vuelo_id}")
def eliminar_vuelo(vuelo_id: int, db: Session = Depends(get_db)):
    vuelo = db.query(Vuelo).filter(Vuelo.id == vuelo_id).first()
    if vuelo is None:
        raise HTTPException(status_code=404, detail="Vuelo no encontrado")

    lista_vuelos.extraer_de_posicion(vuelo_id)  
    db.delete(vuelo)
    db.commit()
    return {"detalle": "Vuelo eliminado"}