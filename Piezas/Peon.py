"""
Modulo para la gestión y uso de un peon

Este módulo define la clase 'Peon' que representa un peon concreto de la partida
y contiene la información única de cualquier peón y sus particularidades.
Posee modulos que permite realizar las funciones especiales de un peon, junto
con modulos más genéricos.

Clases:
    - Peon
"""

from Piezas.Pieza import Pieza

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
    __init__(self, posicion : tuple[int,int], color : int) -> None
        Inicializa un nuevo peon

    transformar() -> bool:
        Comprueba si el peon ha llegado al otro extremo del tablero para transformarse

    en_passant() -> (int,int)
        Devuelve la posición que debe hacer para capturar en passant

    mover_doble() -> (int,int):
        Devuelve la posición si no se ha movido aún y le permite avanzar dos veces hacia delante.

    movimiento_valido() -> list[(int,int)]
        Devuelve el conjunto de posiciones validas que puede tener.

    __str__(self) -> str
        Devuelve la representación del Peon (teniendo en cuenta su color)

    __repr__(self) -> str
        Muesta información técnica del Peon
    """

    def __init__(self, posicion : tuple[int,int], color : int) -> None:
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

    def movimiento_valido(self,tablero : "Tablero",detectando_ataque:bool=False) -> list[tuple[int,int]]:
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

        color : int = -1 if self.color else 1

        if not detectando_ataque:
            if tablero.limite(fila + color, columna) and tablero[fila + color][columna].pieza is None:
                movimientos.append((fila + color,columna))
                if self.mover_doble(tablero,color):
                    movimientos.append((fila + color * 2, columna))

        if (tablero.limite(fila + color, columna + 1) and tablero[fila + color][columna + 1].pieza is not None
                and tablero[fila + color][columna + 1].pieza.color != self.color or self.en_passant(tablero, color)):
            movimientos.append((fila + color, columna + 1))

        if (tablero.limite(fila + color, columna - 1) and tablero[fila + color][columna - 1].pieza is not None
                and tablero[fila + color][columna - 1].pieza.color != self.color or self.en_passant(tablero, color)):
            movimientos.append((fila + color, columna - 1))

        return movimientos

    def transformacion(self) -> bool:
        """
        Comprueba si tiene la posibilidad de transformarse

        Retorna:
        --------
        bool
            Retorna un valor booleano marcando su posibilidad de transformarse
        """

        if self.posicion[0] in [1,6]:
            return True

        return False

    def mover_doble(self, tablero : "Tablero", color : int) -> bool:
        """
        Comprueba si puede dar un segundo paso

        Parametros:
        -----------
        tabelro : Tablero
            Tablero en sí

        color : int
            Color del peon que marca el sentido de su movimiento
        Retorna:
        --------
        bool
            Devuelve un valor booleano marcando su posibilidad de dar un segundo paso
        """

        fila, columna = self.posicion

        if (not self.movido and tablero.limite(fila + color * 2, columna) and
                not tablero[fila + color * 2][columna].pieza is not None):
            return True

        return False

    def en_passant(self, tablero : "Tablero", color : int) -> bool:
        """
        Comprueba si puede hacer en passant

        Parametros:
        -----------
        tabelro : Tablero
            Tablero en sí

        color : int
            Color del peon que marca el sentido de su movimiento
        Retorna:
        --------
        bool
            Devuelve un valor booleano marcando su posibilidad de hacer en passant
        """

        fila, columna = self.posicion

        if tablero.limite(fila + color,columna + 1) and tablero.en_passant is not None and tablero.en_passant[1] == \
                (fila + color, columna + 1):
            return True

        if tablero.limite(fila + color, columna - 1) and tablero.en_passant is not None and tablero.en_passant[1] == \
                (fila + color, columna - 1):
            return True

        return False

    def __str__(self) -> str:
        """
        Método dunder que devuelve la representación de la pieza, teniendo en cuenta su color

        Retorna:
        --------
        str
            Devuelve su representación
        """
        return 'P' if self.color else 'p'

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
