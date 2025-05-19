from Piezas.Pieza import Pieza
from itertools import count

"""
Modulo para la gestión y uso de un alfil

Este módulo define la clase 'Alfil' que representa un alifl concreto de la partida.
Posee solamente los módulos básicos definidos de la superclase 'Pieza' a la que pertenece.

Clases:
    - Alfil
"""

class Alfil(Pieza):
    """
    Clase que representa un alfil concreto

    Atributos:
    -----------
    posicion : list[int,int]
        Posicíon concreta del alfil

    color : bool
        Color del alfil (1 es blanco y 0 es negro)

    capturado : bool
        Marca si está capturado el alfil

    valor : int
        Valor del alfil

    movimientos : list[(int,int)]
        Lista de movimientos válidos del alfil

    Métodos:
    -----------
    __init__(self, posicion : tuple[int,int], color : int) -> None
        Inicializa un nuevo alfil

    movimiento_valido() -> list[(int,int)]
        Devuelve el conjunto de posiciones validas que puede tener.

    __str__(self) -> str
        Devuelve la representación del Alfil (teniendo en cuenta su color)

    __repr__(self) -> str
        Muesta información técnica del Alfil
    """

    def __init__(self, posicion : tuple[int,int], color : int) -> None:
        """
        Inicializa una instacia de la clase Alfil

        Parámetros:
        -----------
        posicion : list[int,int]
            Posicíon concreta del alfil

        color : bool
            Color del alfil (1 es blanco y 0 es negro)
        """
        super().__init__(posicion,color)

    def movimiento_valido(self, tablero: "Tablero") -> list[(int,int)]:
        """
        Comprueba todos los movimientos válidos del alfil

        Parametros:
        -----------
        tabelro : list[list[int]]
            Tablero en sí

        Retorna:
        --------
        list[(int,int)]
            Retorna una lista de movimientos válidos del alfil
        """

        fila, columna = self.posicion
        movimientos = []

        # Estos bucles for acceden solamente a la diagonal que me interesa

        for k in count(1): #Abajo-izquierda
            i = fila + k
            j = columna - k
            if not tablero.limite(i,j):
                break

            if tablero[i][j].pieza is not None:

                if tablero[i][j].pieza.color != self.color:
                    movimientos.append((i, j))

                break
            movimientos.append((i, j))

        for k in count(1): #Arriba-derecha
            i = fila - k
            j = columna + k
            if not tablero.limite(i, j):
                break

            if tablero[i][j].pieza is not None:

                if tablero[i][j].pieza.color != self.color:
                    movimientos.append((i, j))

                break
            movimientos.append((i, j))

        for k in count(1): #Arriba-izquierda
            i = fila - k
            j = columna - k
            if not tablero.limite(i, j):
                break

            if tablero[i][j].pieza is not None:

                if tablero[i][j].pieza.color != self.color:
                    movimientos.append((i, j))

                break
            movimientos.append((i, j))

        for k in count(1): #Abajo-derecha
            i = fila + k
            j = columna + k
            if not tablero.limite(i, j):
                break

            if tablero[i][j].pieza is not None:

                if tablero[i][j].pieza.color != self.color:
                    movimientos.append((i, j))

                break
            movimientos.append((i, j))

        return movimientos

    def __str__(self) -> str:
        """
        Método dunder que devuelve la representación de la pieza, teniendo en cuenta su color

        Retorna:
        --------
        str
            Devuelve su representación
        """
        return 'B' if self.color else 'b'

    def __repr__(self) -> str:
        """
        Metodo especial para mostrar toda la información de la clase

        Retorna:
        --------
        str
            Retorna un str con toda la información
        """
        return super().__repr__()