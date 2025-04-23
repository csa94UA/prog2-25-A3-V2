from abc import ABC, abstractmethod
from typing import Union

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
    movimiento_valido():
        Es un metodo abstracto. Obtiene todos los movimientos posibles de una pieza.
    mover(tuple(int,int)) -> bool:
        Desplaza la pieza desde su posición hasta el destino.
    """

    def __init__(self, posicion: tuple[int,int], color: int) -> None:
        """
        Inicializa una instacia de la clase Pieza

        Parámetros:
        -----------
        posicion : tuple[int,int]
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

    def mover(self, destino: tuple[int], tablero: "Tablero", jugador : "Jugador", enemigo : "Jugador", especial : Union[str,int]) -> bool:
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
        pos_rey = jugador.encontrar_rey()

        x = destino[0]
        y = destino[1]

        if especial.isalpha() and not x in [0,7]:
            print("Error. No se encuentra en el otro lado del tablero")
            return False

        if especial == '0' and str(tablero[self.posicion[0]][self.posicion[1]]) in ['P','p'] and \
                x in [0,7]:
            print("Error. No has digitado una promoción siendo peón.")
            return False

        # Recorremos todos los movimientos válidos de la pieza

        if destino is not tuple() and not destino in self.movimiento_valido(tablero):
            print("Error. La posición desitno no está dentro de los movimientos validos de la pieza")
            return False

        tablero_antiguo = tablero.guardar_estado()

        pos_ant_pieza : tuple[int,int] = self.posicion
        self.posicion = (x, y)
        tablero[pos_ant_pieza[0]][pos_ant_pieza[1]].pieza = None
        
        pieza_enemgio = tablero[x][y].pieza
        tablero[x][y].pieza = self
        if tablero.amenazas(enemigo,*pos_rey):
            print("Error. Tu movimiento provoca o no impide un jaque")
            tablero.restaurar_estado(tablero_antiguo)
            return False

        

        if pieza_enemgio is not None and pieza_enemgio.posicion == self.posicion:
            enemigo.piezas.remove(pieza_enemgio)
        return True

    @abstractmethod
    def __str__(self):
        """
        Método abstracto que se espera ser definido por las subclases.
        Debe devolver la representación en string de la pieza en sí (teniendo en cuenta su color)
        """
        pass
    
    def __repr__(self):
        """
        Metodo especial para mostrar toda la información de la clase

        Retorna:
        --------
        str
            Retorna un str con toda la información
        """
        return (f"{type(self).__name__}(Posición = {self.posicion}, "
                f"Color = {self.color}, Capturado = {self.capturado}, "
                f"Valor = {self.valor}, Movimientos = {self.movimientos})")