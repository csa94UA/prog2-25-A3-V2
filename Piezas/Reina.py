from Piezas.Pieza import Pieza
from itertools import count

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

    def __init__(self, posicion: tuple[int,int], color: int) -> None:
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

        for k in count(1):  # Abajo-izquierda
            i = fila + k
            j = columna - k
            if not tablero.limite(i, j):
                break

            if tablero[i][j].pieza is not None:

                if tablero[i][j].pieza.color != self.color:
                    movimientos.append((i, j))

                break
            movimientos.append((i, j))

        for k in count(1):  # Arriba-derecha
            i = fila - k
            j = columna + k
            if not tablero.limite(i, j):
                break

            if tablero[i][j].pieza is not None:

                if tablero[i][j].pieza.color != self.color:
                    movimientos.append((i, j))

                break
            movimientos.append((i, j))

        for k in count(1):  # Arriba-izquierda
            i = fila - k
            j = columna - k
            if not tablero.limite(i, j):
                break

            if tablero[i][j].pieza is not None:

                if tablero[i][j].pieza.color != self.color:
                    movimientos.append((i, j))

                break
            movimientos.append((i, j))

        for k in count(1):  # Abajo-derecha
            i = fila + k
            j = columna + k
            if not tablero.limite(i, j):
                break

            if tablero[i][j].pieza is not None:

                if tablero[i][j].pieza.color != self.color:
                    movimientos.append((i, j))

                break
            movimientos.append((i, j))

        for i in count(fila-1,-1):

            if not tablero.limite(i,columna):
                break

            if tablero[i][columna].pieza is not None:

                if tablero[i][columna].pieza.color != self.color:
                    movimientos.append((i,columna))

                break
            movimientos.append((i,columna))

        for i in count(fila + 1):

            if not tablero.limite(i, columna):
                break

            if tablero[i][columna].pieza is not None:

                if tablero[i][columna].pieza.color != self.color:
                    movimientos.append((i, columna))

                break
            movimientos.append((i, columna))

        for j in count(columna - 1, -1):

            if not tablero.limite(fila, j):
                break

            if tablero[fila][j].pieza is not None:

                if tablero[fila][j].pieza.color != self.color:
                    movimientos.append((fila, j))

                break
            movimientos.append((fila, j))

        for j in count(columna + 1):

            if not tablero.limite(fila, j):
                break

            if tablero[fila][j].pieza is not None:

                if tablero[fila][j].pieza.color != self.color:
                    movimientos.append((fila, j))

                break
            movimientos.append((fila, j))

        return movimientos

    def __str__(self) -> str:
        """
        Método dunder que devuelve la representación de la pieza, teniendo en cuenta su color

        Retorna:
        --------
        str
            Devuelve su representación
        """
        return 'Q' if self.color else 'q'

    def __repr__(self):
        """
        Metodo especial para mostrar toda la información de la clase

        Retorna:
        --------
        str
            Retorna un str con toda la información
        """
        return super().__repr__()