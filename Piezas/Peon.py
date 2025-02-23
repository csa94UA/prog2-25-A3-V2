"""
Modulo para la gestión y uso de un peon

Este módulo define la clase 'Peon' que representa una peon concreto de la partida
y contiene la información única para cualquier peón y sus particularidades.
Posee modulos que permite realizar las funciones especiales de un peon, junto
con modulos más genéricos.

Clases:
    - Peon
"""

class Peon:
    """
    Clase que representa un peon concreto

    Atributos:
    -----------
    movido : bool
        Si ya se ha movido (para los movimientos especiales)
    id : int
        Id de la pieza (para diferenciar)

    Métodos:
    -----------
    transformar() -> bool:
        Comprueba si el peon ha llegado al otro extremo del tablero para transformarse
    en_passant() -> tuple(int,int)
        Devuelve la posición que debe hacer para capturar en passant
    mover_doble() -> tuple(int,int):
        Devuelve la posición si no se ha movido aún y le permite avanzar
        dos veces hacia delante.
    movimiento_valido() -> tuple(int,int)
    """

    def __init__(self,id : int) -> None:
        """
        Inicializa una instacia de la clase Peon
        Parámetros:
        -----------
        id : int
            Id de la pieza (para diferenciar)
        """
        self.id = id
        self.movido = False

    def movimiento_valido(self,tablero : list[list[int]]) -> list[tuple(int,int)]:
        """
        Comprueba todos los movimientos válidos del peon
        Parametros:
        -----------
        tabelro : list[list[int]]
            Tablero en sí
        Retorna:
        --------
        list[tuple(int,int)]
            Retorna una lista de movimientos válidos del peon
        """

        fila, columna = self.posicion
        movimientos = []

        if tablero[fila+1][columna] == 0:
            movimientos.append(tuple(fila + 1,columna))
            if mover_doble(tablero):
                movimientos.append(tuple(fila + 2, columna))

        if tablero[fila + 1,columna + 1] != 0 or en_passant(tablero):
            movimientos.append(tuple(fila, columna + 1))

        if tablero[fila + 1,columna - 1] != 0 or en_passant(tablero):
            movimientos.append(tuple(fila, columna - 1))

        return movimientos

    def transformacion(self) -> bool:

        """
        Comprueba si tiene la posibilidad de transformarse
        Retorna:
        --------
        bool
            Retorna un valor booleano marcando su posibilidad de transformarse
        """

        fila, columna = self.posicion

        if self.posicion == (1,1) or (8,8):
            return True

    def mover_doble(self, tablero : list[list[int]]) -> bool:
        """
        Comprueba si puede dar un segundo paso
        Parametros:
        -----------
        tabelro : list[list[int]]
            Tablero en sí
        Retorna:
        --------
        bool
            Retorna un valor booleano marcando su posibilidad de dar un segundo paso
        """
        fila, columna = self.posicion

        if not self.movido and tablero[fila + 2][columna] == 0:
            return True

        return False

    def en_passant(self, tablero : list[list[int]]) -> bool: