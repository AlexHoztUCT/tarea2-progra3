from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session

from database import SessionLocal, engine, init_db
from models import CrearVuelo, Vuelo
from listadoble import ListaDobleEnlazada

app = FastAPI()

# Inicializar la base de datos (esto creará vuelos.db y las tablas necesarias)
init_db()

lista_vuelos = ListaDobleEnlazada()

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/vuelos/", response_model=Vuelo)
def crear_vuelo(vuelo: CrearVuelo, db: Session = Depends(get_db)):
    # Añadir vuelo a la base de datos
    vuelo_db = Vuelo(**vuelo.dict())
    lista_vuelos.insertar_al_final(vuelo_db)  # O usar insertar_al_frente para emergencias
    db.add(vuelo_db)
    db.commit()
    db.refresh(vuelo_db)
    return vuelo_db

@app.get("/vuelos/total")
def obtener_total_vuelos():
    return {"total_vuelos": lista_vuelos.longitud()}

@app.get("/vuelos/proximo")
def obtener_vuelo_proximo():
    vuelo = lista_vuelos.obtener_primero()
    if vuelo is None:
        raise HTTPException(status_code=404, detail="No hay vuelos en la lista")
    return vuelo

@app.get("/vuelos/ultimo")
def obtener_vuelo_ultimo():
    vuelo = lista_vuelos.obtener_ultimo()
    if vuelo is None:
        raise HTTPException(status_code=404, detail="No hay vuelos en la lista")
    return vuelo

@app.post("/vuelos/insertar")
def insertar_vuelo_en_posicion(vuelo: CrearVuelo, posicion: int):
    lista_vuelos.insertar_en_posicion(vuelo, posicion)
    return {"detalle": "Vuelo insertado en la posición específica"}

@app.delete("/vuelos/extraer")
def eliminar_vuelo(posicion: int):
    vuelo = lista_vuelos.extraer_de_posicion(posicion)
    return {"detalle": f"Vuelo {vuelo} eliminado"}

@app.get("/vuelos/lista")
def listar_vuelos():
    return lista_vuelos.listar_vuelos()

@app.patch("/vuelos/reordenar")
def reordenar_vuelo(posicion_antigua: int, posicion_nueva: int):
    vuelo = lista_vuelos.extraer_de_posicion(posicion_antigua)
    lista_vuelos.insertar_en_posicion(vuelo, posicion_nueva)
    return {"detalle": f"Vuelo movido de {posicion_antigua} a {posicion_nueva}"}