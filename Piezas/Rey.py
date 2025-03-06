from Piezas.Pieza import Pieza

"""
Modulo para la gestión y uso del rey

Este módulo define la clase 'Rey' que representa el rey de la partida
y contiene la información única del rey y sus particularidades.
Posee modulos que permite realizar sus funciones especiales , junto
con modulos más genéricos.

Clases:
    - Rey
"""

class Rey(Pieza):
    """
    Clase que representa el rey

    Atributos:
    -----------
    posicion : list[int,int]
        Posicíon concreta del rey
    color : bool
        Color del rey (1 es blanco y 0 es negro)
    capturado : bool
        Marca si está capturada el rey
    valor : int
        Valor del rey
    movimientos : list[(int,int)]
        Lista de movimientos válidos del rey
    movido : bool
        Si ya se ha movido (para los movimientos especiales)
    turnos : int
        Marca la cantidad de movimientos restantes que tiene el rey.
        Solo se activa cuando no quedan piezas activas de su color

    Métodos:
    -----------
    movimiento_valido() -> list[(int,int)]
        Devuelve el conjunto de posiciones validas que puede tener.
    enroque() -> bool
        Devuelve True si es posible hacer el enroque.
    jaque_mate() -> bool
        Comprueba si es jaque mate
    """

    def __init__(self, posicion: list[int, int], color: bool) -> None:
        """
        Inicializa una instacia de la clase Rey

        Parámetros:
        -----------
        posicion : list[int,int]
            Posicíon concreta del rey
        color : bool
            Color del rey (1 es blanco y 0 es negro)
        """
        super().__init__(posicion, color)
        self. movido = False
        self.turnos = 50 #Se descuenta cuando solo quede el rey en pie

    def movimiento_valido(self, tablero : "Tablero") -> list[(int,int)]:
        """
        Comprueba todos los movimientos válidos del rey

        Parametros:
        -----------
        tabelro : list[list[int]]
            Tablero en sí
        Retorna:
        --------
        list[tuple(int,int)]
            Retorna una lista de movimientos válidos del rey
        """

        fila, columna = self.posicion
        movimientos = []

        for i in range(fila - 1, fila + 2):
            for j in range(columna - 1, columna + 2):
                if tablero.limite(i,j) and tablero[i][j] == 0:
                    movimientos.append(tuple[i,j])

        return movimientos

    def enroque(self) -> bool:
        """
        Comprueba si puede hacer enroque

        Retorna:
        --------
        bool
            Devuelve True si puede hacer enroque
        """

        if self.movido is True:
            return False

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
                f"Turnos -> {self.turnos}, Movimientos -> {self.movimientos})")