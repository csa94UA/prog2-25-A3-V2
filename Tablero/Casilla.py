

class Casilla:

    def __init__(self, fila : int, columna : int):
        self.fila = fila
        self.columna = columna
        self.ocupado = False
        self.pieza = None
        self.amenazado = False

    def conquistado(self, pieza : Pieza):
        self.pieza = pieza.id

    def amenazas(self):


    def __repr__(self):
        return (f"Posicion -> ("'{self.fila}'",""{self.columna})'",
                "Ocupado -> '{self.ocupado}'", "Pieza -> '{self.pieza}'",
                "Amenazado -> '{self.amenazado}'")
