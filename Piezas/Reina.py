from Piezas.Pieza import Pieza

"""
Modulo para la gestión y uso de un reina

Este módulo define la clase 'Reina' que representa un reina concreto de la partida.
Posee solamente los módulos básicos definidos de la superclase 'Pieza' a la que pertenece.

Clases:
    - Reina
"""

class Reina(Pieza):
    """
    Clase que representa la reina

    Atributos:
    -----------
    posicion : list[int,int]
        Posicíon concreta de la reina
    color : bool
        Color de la reina (1 es blanco y 0 es negro)
    capturado : bool
        Marca si está capturado la reina
    valor : int
        Valor de la reina
    movimientos : list[(int,int)]
        Lista de movimientos válidos de la reina

    Métodos:
    -----------
    movimiento_valido() -> list[(int,int)]
        Devuelve el conjunto de posiciones validas que puede tener.
    """

    def __init__(self, posicion: list[int, int], color: bool) -> None:
        """
        Inicializa una instacia de la clase Reina
        Parámetros:
        -----------
        posicion : list[int,int]
            Posicíon concreta de la reina
        color : bool
            Color de la reina (1 es blanco y 0 es negro)
        """
        super().__init__(posicion, color)

    def movimiento_valido(self, tablero: "Tablero") -> list[(int,int)]:
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

        # Estos bucles for acceden solamente a la diagonal que me interesa
        for d in range(1, min(8 - fila, columna + 1)):
            i = fila + d
            j = columna - d
            if tablero[i][j].ocupado:
                break
            movimientos.append(tuple[i, j])

        for k in range(1, min(fila + 1, 8 - columna)):
            i = fila - d
            j = columna + d
            if tablero[i][j].ocupado:
                break
            movimientos.append(tuple[i, j])

        for k in range(1, min(fila + 1, columna + 1)):
            i = fila - k
            j = columna - k
            if tablero[i][j].ocupado:
                break
            movimientos.append(tuple[i, j])

        for k in range(1, min(8 - fila, 8 - columna)):
            i = fila + k
            j = columna + k
            if tablero[i][j].ocupado:
                break
            movimientos.append((i, j))

        for i in range(fila-1,1,-1):
            if tablero[i][columna] != 0:
                break
            movimientos.append((i,columna))

        for i in range(fila+1,8):
            if tablero[i][columna] != 0:
                break
            movimientos.append((i,columna))

        for j in range(columna-1,1,-1):
            if tablero[fila][j] != 0:
                break
            movimientos.append((fila,j))

        for j in range(columna+1,8):
            if tablero[fila][j] != 0:
                break
            movimientos.append((fila,j))

        return movimientos

    def __repr__(self):
        """
        Metodo especial para mostrar toda la información de la clase

        Retorna:
        --------
        str
            Retorna un str con toda la información
        """
        return super().__repr__()