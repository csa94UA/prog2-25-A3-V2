from uaclient.util import replace_top_level_logger_name

from Piezas import Caballo, Alfil, Rey, Torre, Reina, Pieza, Peon
from typing import Union

"""
Modulo para la gestión de un jugador

Este modulo define la clase Jugador que contendra la información del usuario junto con sus piezas
que estarán dispoonibles cuando esté en partida

Clases:
    - Jugador
"""

class Jugador:

    def __init__(self, nombre : str, puntuacion : int) -> None:
        """
        Inicializa una instacia de la clase Jugador

        Parámetros:
        -----------
        nombre : str
            Nombre del jugador
        puntuacion : bool
            Puntuacion que tiene el jugador. Refleja el nivel del jugador
        """
        self.nombre : str = nombre
        self.puntuacion : int = puntuacion
        self.color : Union[bool,None] = None
        self.piezas : list= []
        self.cantidad : dict = {"P" : 0, "B" : 0, "N" : 0,
                               "R" : 0, "Q" : 0, "K" : 0}

    def añadir_pieza(self, pieza : Pieza) -> None:
        """
        Añade una pieza a su colección y lo cuenta

        Parámetros:
        -----------
        pieza : Pieza
            Pieza que va a ser añadida al equipo
        """

        if isinstance(pieza, Peon):
            self.cantidad["P"] += 1

        elif isinstance(pieza, Alfil):
            self.cantidad["B"] += 1

        elif isinstance(pieza, Caballo):
            self.cantidad["N"] += 1

        elif isinstance(pieza, Torre):
            self.cantidad["R"] += 1

        elif isinstance(pieza, Reina):
            self.cantidad["Q"] += 1

        elif isinstance(pieza, Rey):
            self.cantidad["K"] += 1

        self.piezas.append(pieza)

        return None

    def eliminar_pieza(self, pieza : Pieza) -> None:
        """
        Elimina la pieza en caso de ser capturada

        Parámetros:
        -----------
        pieza : Pieza
            Se trata de la pieza que va a ser eliminada

        """

        self.piezas.remove(pieza)

        return None

    def __repr__(self):
        """
        Metodo especial para mostrar toda la información de la clase

        Retorna:
        --------
        str
            Retorna un str con toda la información
        """

        return f"{type(self).__name__}(Jugador -> {self.nombre}, puntuacion -> {self.puntuacion}, \
        color ->  {"1" if self.color else "0"}, piezas -> {self.piezas}, Cantidad -> {self.cantidad})"