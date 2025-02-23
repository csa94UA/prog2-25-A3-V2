

class Reina:

    def __init__(self,id : int):
        self.id = id

    def movimiento_valido(self, tablero: list[list[int]]) -> list[tuple(int, int)]:
        """
        Comprueba todos los movimientos válidos del alfil
        Parametros:
        -----------
        tabelro : list[list[int]]
            Tablero en sí
        Retorna:
        --------
        list[tuple(int,int)]
            Retorna una lista de movimientos válidos del alfil
        """

        fila, columna = self.posicion
        movimientos = []

        # Esto es un conjunto de bucles for sucediendo SIMULTANEAMENTE (para facilitame las diagonales)
        for i, j in product(range(fila - 1.1,-1), range(columna - 1, 1,-1)):
            if tablero[i][j] != 0:
                break
            movimientos.append(tuple(i, j))

        for i, j in product(range(fila - 1.1,-1), range(columna + 1, 8)):
            if tablero[i][j] != 0:
                break
            movimientos.append(tuple(i, j))

        for i, j in product(range(fila + 1,8), range(columna - 1, 1,-1)):
            if tablero[i][j] != 0:
                break
            movimientos.append(tuple(i, j))

        for i, j in product(range(fila + 1,8), range(columna + 1, 8)):
            if tablero[i][j] != 0:
                break
            movimientos.append(tuple(i, j))

        for i in range(fila-1,1,-1):
            if tablero[i][columna] != 0:
                break
            movimientos.append(tuple(i,columna))

        for i in range(fila+1,8):
            if tablero[i][columna] != 0:
                break
            movimientos.append(tuple(i,columna))

        for j in range(columna-1,1,-1):
            if tablero[fila][j] != 0:
                break
            movimientos.append(tuple(fila,i))

        for j in range(columna+1,8):
            if tablero[fila][j] != 0:
                break
            movimientos.append(tuple(fila,i))

        return movimientos