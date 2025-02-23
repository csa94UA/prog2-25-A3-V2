from abc import ABC, abstractmethod

"""
Modulo para la gestión y uso de una pieza genérica

Este módulo define la clase 'Pieza' que representa una pieza de ajedrez genérica
y contiene la información más esencial de cualquier pieza. Posee modulos que permite
realizar funciones básicas de cualquier pieza.

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

    def __init__(self, posicion : list[int,int], color : bool) -> None:
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
    def movimiento_valido(self,tablero : list[list[int]]):
        """
        Metodo que espera ser ejecutado en las subclases (torre, alfil, etc)
        debe retornar una lista de movimientos permitidos
        """
        pass

    def mover(self, destino : list[int,int], tablero : list[list[int]]):
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

            if destino == tuple(x,y) and CaminoLibre(tuple(x,y)) \
                and not Ocupado(tuple(x,y)) and not Jaque(tuple(x,y)):
                self.posicion[0] = x
                self.posicion[1] = y
                return True

        return False

    def capturar(self, destino : tuple(int,int)):
        """
        Desplaza la pieza desde su posición hasta el destino capturando la pieza
        Parámetros:
        -----------
        destino : tuple(int,int)
            Posición dsetino de la pieza
        Retorna:
        --------
        bool
            Si la pieza ha logrado llegar a su destino y ha cazado una pieza
        """

        # Recorremos todos los movimientos válidos de la pieza

        for movimiento in self.movimientos:
            x = self.posicion[0] + movimiento[0]
            y = self.posicion[1] + movimiento[1]

            if destino == tuple(x, y) and CaminoLibre(tuple(x, y)) \
                    and Enemigo(tuple(x, y)) and not Jaque(tuple(x, y)):
                self.posicion[0] = x
                self.posicion[1] = y
                return True

        return False