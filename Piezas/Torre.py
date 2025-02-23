

class Torre:

    def __init__(self,id : int) -> None:
        self.id = id
        self.movido = False

    def movimiento_valido(self, tablero: list[list[int]]) -> list[tuple(int, int)]:
        """
        Comprueba todos los movimientos válidos de la torre
        Parametros:
        -----------
        tabelro : list[list[int]]
            Tablero en sí
        Retorna:
        --------
        list[tuple(int,int)]
            Retorna una lista de movimientos válidos de la torre
        """

        fila, columna = self.posicion
        movimientos = []

        for i in range(fila - 1, 1, -1):
            if tablero[i][columna] != 0:
                break
            movimientos.append(tuple(i, columna))

        for i in range(fila + 1, 8):
            if tablero[i][columna] != 0:
                break
            movimientos.append(tuple(i, columna))

        for j in range(columna - 1, 1, -1):
            if tablero[fila][j] != 0:
                break
            movimientos.append(tuple(fila, i))

        for j in range(columna + 1, 8):
            if tablero[fila][j] != 0:
                break
            movimientos.append(tuple(fila, i))

        return movimientos

    def enroque(self,tablero : list[list[int]]) -> bool:

        fila, columna = self.posicion

        if self.movido == True:
            return False

        if columna == 1 and tablero[fila][columna:5] // 0: #Esa operación se definirá en Tablero
            return True

        elif columna == 8 and tablero[fila][4:columna+1] // 0:
            return True

        return False