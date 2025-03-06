from Piezas.Pieza import Pieza

"""
Modulo para la gestión y uso de un peon

Este módulo define la clase 'Peon' que representa un peon concreto de la partida
y contiene la información única de cualquier peón y sus particularidades.
Posee modulos que permite realizar las funciones especiales de un peon, junto
con modulos más genéricos.

Clases:
    - Peon
"""

class Peon(Pieza):
    """
    Clase que representa un peon concreto

    Atributos:
    -----------
    posicion : list[int,int]
        Posicíon concreta del peon
    color : bool
        Color del peon (1 es blanco y 0 es negro)
    capturado : bool
        Marca si está capturada el peon
    valor : int
        Valor del peon
    movimientos : list[(int,int)]
        Lista de movimientos válidos del peon
    movido : bool
        Si ya se ha movido (para los movimientos especiales)

    Métodos:
    -----------
    transformar() -> bool:
        Comprueba si el peon ha llegado al otro extremo del tablero para transformarse
    en_passant() -> (int,int)
        Devuelve la posición que debe hacer para capturar en passant
    mover_doble() -> (int,int):
        Devuelve la posición si no se ha movido aún y le permite avanzar
        dos veces hacia delante.
    movimiento_valido() -> list[(int,int)]
        Devuelve el conjunto de posiciones validas que puede tener.
    """

    def __init__(self, posicion : list[int,int], color : bool) -> None:
        """
        Inicializa una instacia de la clase Peon
        Parámetros:
        -----------
        posicion : list[int,int]
            Posicíon concreta del peon
        color : bool
            Color del peon (1 es blanco y 0 es negro)
        """
        super().__init__(posicion,color)
        self.movido = False

    def movimiento_valido(self,tablero : "Tablero") -> list[tuple[int,int]]:
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
            movimientos.append((fila + 1,columna))
            if mover_doble(tablero):
                movimientos.append((fila + 2, columna))

        if tablero[fila + 1,columna + 1] != 0 or en_passant(tablero):
            movimientos.append((fila, columna + 1))

        if tablero[fila + 1,columna - 1] != 0 or en_passant(tablero):
            movimientos.append((fila, columna - 1))

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


    def mover_doble(self, tablero : "Tablero") -> bool:
        """
        Comprueba si puede dar un segundo paso

        Parametros:
        -----------
        tabelro : Tablero
            Tablero en sí
        Retorna:
        --------
        bool
            Devuelve un valor booleano marcando su posibilidad de dar un segundo paso
        """

        fila, columna = self.posicion

        if not self.movido and not tablero[fila + 2][columna].pieza is not None:
            return True

        return False

    def en_passant(self, tablero : "Tablero") -> bool:
        """
        Comprueba si puede hacer en passant

        Parametros:
        -----------
        tabelro : Tablero
            Tablero en sí
        Retorna:
        --------
        bool
            Devuelve un valor booleano marcando su posibilidad de hacer en passant
        """

        fila, columna = self.posicion

        if tablero.limite(fila+1,columna+1) and tablero[fila+1][columna+1].en_passant:
            return True

        if tablero.limite(fila+1,columna-1) and tablero[fila+1][columna-1]:
            return True

        return False
