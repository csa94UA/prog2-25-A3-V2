

class Rey:

    def __init__(self,id : int):
        self.id = id
        self. movido = False
        self.turnos = 50 #Se descuenta cuando solo quede el rey en pie

    def movimiento_valido(self, tablero  :list[list[int]]) -> list[tuple[int]]:

        fila, columna = self.posicion
        movimientos = []

        for i in range(fila - 1. fila + 2):
            for j in range(columna - 1, columna + 2):
                if tablero.limite(i,j) and tablero[i][j] == 0:
                    movimientos.append(tuple(i,j))

        return movimientos

    def enroque(self, tablero: list[list[int]]) -> bool:

        if self.movido == True:
            return False

        return False

    def jaque_mate(self, tablero : list[list[int]]) -> bool:

        fila, columna = self.posicion

        if Rey.movimiento_valido(tablero) == [] and not tablero.jaque_in(fila,columna):
            return True

        return False

