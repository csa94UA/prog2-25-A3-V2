from abc import ABC, abstractmethod
from typing import Union, TYPE_CHECKING
from Jugador import Jugador
from Piezas import Reina, Torre

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
    posicion : tuple[int,int]
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

    def __init__(self, posicion: tuple[int, int], color: bool) -> None:
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

    def mover(self, destino: tuple[int, int], tablero: "Tablero", jugador : "Jugador", enemigo : "Jugador",
              pos_rey : tuple[int, int], especial : Union[str,int]) -> bool:
        from Tablero import Tablero
        from Jugador import Jugador
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

        if especial.isalpha() and not self.transformacion():
            print("Error. No se encuentra en el otro lado del tablero")
            return False

        # Recorremos todos los movimientos válidos de la pieza

        if destino is not tuple() and not destino in self.movimiento_valido(tablero):
            print("Error. La posición desitno no está dentro de los movimientos validos de la pieza")
            return False

        x = destino[0]
        y = destino[1]

        pos_ant = self.posicion
        self.posicion = (x, y)
        tablero[pos_ant[0]][pos_ant[1]].pieza = None

        if tablero.amenazas(enemigo, pos_rey[0], pos_rey[1]):
            print("Error. Tu movimiento provoca o no impide un jaque")
            self.posicion = pos_ant
            tablero[pos_ant[0]][pos_ant[1]].pieza = self
            return False

        if tablero[x][y].pieza is not None:
            enemigo.piezas.remove(tablero[x][y].pieza)
            tablero[x][y].pieza = None

        tablero[x][y] = self

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