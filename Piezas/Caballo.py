

class Caballo:

    def __init__(self,id : int):
        self.id = id

    def movimiento_valido(self, tablero: list[list[int]]) -> list[tuple(int,int)]:
        """
        Comprueba todos los movimientos válidos del caballo
        Parametros:
        -----------
        tabelro : list[list[int]]
            Tablero en sí
        Retorna:
        --------
        list[tuple(int,int)]
            Retorna una lista de movimientos válidos del caballo
        """
        movimientos = [(1,2),(1,-2),(2,1),(2,-1),(-1,2),(-1,-2),(-2,1),(-2,-1)]

        for fila, columna in movimientos:
            if tablero[fila][columna] != 0:
                movimientos.remove((fila,columna))

        return movimientos

