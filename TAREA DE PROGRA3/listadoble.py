# listadoble.py
class Nodo:
    """Clase que representa un nodo en la lista doblemente enlazada."""
    def __init__(self, vuelo):
        self.vuelo = vuelo
        self.siguiente = None
        self.anterior = None

class ListaDobleEnlazada:
    """Clase que representa la lista doblemente enlazada de vuelos."""
    def __init__(self):
        self.primero = None
        self.ultimo = None
        self.contador = 0

    def insertar_al_frente(self, vuelo):
        nuevo_nodo = Nodo(vuelo)
        if not self.primero:
            self.primero = nuevo_nodo
            self.ultimo = nuevo_nodo
        else:
            nuevo_nodo.siguiente = self.primero
            self.primero.anterior = nuevo_nodo
            self.primero = nuevo_nodo
        self.contador += 1
        
    def insertar_al_final(self, vuelo):
        nuevo_nodo = Nodo(vuelo)
        if not self.primero:
            self.primero = nuevo_nodo
            self.ultimo = nuevo_nodo
        else:
            self.ultimo.siguiente = nuevo_nodo
            nuevo_nodo.anterior = self.ultimo
            self.ultimo = nuevo_nodo
        self.contador += 1
        
    def obtener_primero(self):
        if self.primero:
            return self.primero.vuelo
        return None

    def obtener_ultimo(self):
        if self.ultimo:
            return self.ultimo.vuelo
        return None

    def longitud(self):
        return self.contador

    def insertar_en_posicion(self, vuelo, posicion):
        if posicion < 0 or posicion > self.contador:
            raise IndexError("Posición fuera de rango")

        nuevo_nodo = Nodo(vuelo)

        if posicion == 0:
            self.insertar_al_frente(vuelo)
        elif posicion == self.contador:
            self.insertar_al_final(vuelo)
        else:
            nodo_actual = self.primero
            for _ in range(posicion):
                nodo_actual = nodo_actual.siguiente
            nuevo_nodo.anterior = nodo_actual.anterior
            nuevo_nodo.siguiente = nodo_actual
            nodo_actual.anterior.siguiente = nuevo_nodo
            nodo_actual.anterior = nuevo_nodo
            self.contador += 1

    def extraer_de_posicion(self, posicion):
        if posicion < 0 or posicion >= self.contador:
            raise IndexError("Posición fuera de rango")

        if posicion == 0:
            vuelo = self.primero.vuelo
            self.primero = self.primero.siguiente
            if self.primero:
                self.primero.anterior = None
            else:
                self.ultimo = None  # Si la lista queda vacía
            self.contador -= 1
            return vuelo

        if posicion == self.contador - 1:
            vuelo = self.ultimo.vuelo
            self.ultimo = self.ultimo.anterior
            if self.ultimo:
                self.ultimo.siguiente = None
            else:
                self.primero = None  # Si la lista queda vacía
            self.contador -= 1
            return vuelo

        nodo_actual = self.primero
        for _ in range(posicion):
            nodo_actual = nodo_actual.siguiente

        vuelo = nodo_actual.vuelo
        nodo_actual.anterior.siguiente = nodo_actual.siguiente
        nodo_actual.siguiente.anterior = nodo_actual.anterior
        self.contador -= 1
        return vuelo

    def listar_vuelos(self):
        vuelos = []
        nodo_actual = self.primero
        while nodo_actual:
            vuelos.append(nodo_actual.vuelo)
            nodo_actual = nodo_actual.siguiente
        return vuelos