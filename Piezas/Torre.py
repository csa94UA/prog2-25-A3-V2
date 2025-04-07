from Piezas.Pieza import Pieza
from itertools import count


"""
Modulo para la gestión y uso de una torre

Este módulo define la clase 'Torre' que representa una torre concreto de la partida
y contiene la información única de cualquier torre y sus particularidades.
Posee modulos que permite realizar las funciones especiales de una torre, junto
con modulos más genéricos.

Clases:
    - Torre
"""

class Torre(Pieza):
    """
    Clase que representa una torre concreto

    Atributos:
    -----------
    posicion : list[int,int]
        Posicíon concreta de la torre
    color : bool
        Color de la torre (1 es blanco y 0 es negro)
    capturado : bool
        Marca si está capturada la torre
    valor : int
        Valor de la torre
    movimientos : list[(int,int)]
        Lista de movimientos válidos de la torre
    movido : bool
        Si ya se ha movido (para los movimientos especiales)

    Métodos:
    -----------
    movimiento_valido() -> list[(int,int)]
        Devuelve el conjunto de posiciones validas que puede tener.
    enroque() -> bool
        Devuelve True si es posible hacer el enroque.
    """

    def __init__(self, posicion: tuple[int,int], color: int) -> None:
        """
        Inicializa una instacia de la clase Torre
        Parámetros:
        -----------
        posicion : list[int,int]
            Posicíon concreta de la torre
        color : bool
            Color de la torre (1 es blanco y 0 es negro)
        """
        super().__init__(posicion, color)
        self.movido = False

    def movimiento_valido(self, tablero: "Tablero") -> list[(int,int)]:
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

        for i in count(fila - 1, -1):

            if not tablero.limite(i, columna):
                break

            if tablero[i][columna].pieza is not None:

                if tablero[i][columna].pieza.color != self.color:
                    movimientos.append((i, columna))

                break
            movimientos.append((i, columna))

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

    def enroque(self) -> bool:
        """
        Comprueba si puede hacer enroque

        Retorna:
        --------
        bool
            Devuelve True si puede hacer enroque
        """

        #fila, columna = self.posicion

        if self.movido is not True:
            return True

        #if columna == 1 and tablero[fila][columna:5] // 0: #Esa operación se definirá en Tablero
        #    return True

        #elif columna == 8 and tablero[fila][4:columna+1] // 0:
        #    return True

        return False

    def __repr__(self):
        """
        Metodo especial para mostrar toda la información de la clase

        Retorna:
        --------
        str
            Retorna un str con toda la información
        """
        return (f"{type(self).__name__}(Posición -> {self.posicion}, "
                f"Color -> {self.color}, Capturado -> {self.capturado}, "
                f"Valor -> {self.valor}, Movido -> {self.movido}, "
                f"Movimientos -> {self.movimientos})")