from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Tablero import Tablero

"""
Modulo para la gestión y uso de una pieza genérica

Este módulo define la clase abstracta 'Pieza' que representa una pieza de ajedrez genérica
y contiene la información más esencial. Posee modulos que permite realizar las funciones básicas.

Clases:
    - Pieza
"""


class Pieza(ABC):
    """
    Clase que representa una pieza genérica

    Atributos:
    -----------
    posicion : list[int,int]
        Posicíon concreta de una pieza
    color : bool
        Color de la pieza (1 es blanco y 0 es negro)
    capturado : bool
        Marca si está capturada la pieza
    valor : int
        Valor de la pieza (según la subclase a la que pertenezca)
    movimientos : list[tuple(int,int)]
        Lista de movimientos válidos de la pieza (según su subclase)

    Métodos:
    -----------
    mover(tuple(int,int)) -> bool:
        Desplaza la pieza desde su posición hasta el destino.
    capturar(tuple(int,int)) -> bool:
        Desplaza la pieza desde su posición hasta el destino para
        capturar una pieza (con la notación algebráica cobra más sentido)
    """

    def __init__(self, posicion: list[int, int], color: bool) -> None:
        """
        Inicializa una instacia de la clase Pieza

        Parámetros:
        -----------
        posicion : list[int,int]
            Posicíon concreta de una pieza
        color : bool
            Color de la pieza (1 es blanco y 0 es negro)
        """
        self.posicion = posicion
        self.color = color
        self.capturado = False
        self.valor = 0
        self.movimientos = []

    @abstractmethod
    def movimiento_valido(self, tablero: "Tablero"):
        from Tablero import Tablero
        """
        Metodo que espera ser ejecutado en las subclases (torre, alfil, etc)
        debe retornar una lista de movimientos permitidos
        """
        pass

    def mover(self, destino: list[int, int], tablero: "Tablero"):
        from Tablero import Tablero
        """
        Desplaza la pieza desde su posición hasta el destino.

        Parámetros:
        -----------
        destino : tuple(int,int)
            Posición dsetino de la pieza
        Retorna:
        --------
        bool
            Si la pieza ha logrado llegar a su destino
        """

        # Recorremos todos los movimientos válidos de la pieza

        self.movimientos = self.movimiento_valido(tablero)

        for movimiento in self.movimientos:
            x = self.posicion[0] + movimiento[0]
            y = self.posicion[1] + movimiento[1]

            if destino == (x, y) and tablero[x][y].pieza is None and not Jaque(tuple[x, y]):
                self.posicion[0] = x
                self.posicion[1] = y
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
                f"Valor -> {self.valor}, Movimientos -> {self.movimientos})")