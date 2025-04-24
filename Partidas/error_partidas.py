"""
Módulo de excepciones hecha para las partidas

Este módulo en concreto se encarga de manejar toda clase de errores que puedan ocurrir dentro de una partida: desde
movimientos ilegales hasta errores en movimientos especiales.

Clases:
    ErrorPartida
"""
from typing import Union
from Piezas import Pieza


class ErrorPartida(Exception):
    """
    Excepcion personalizada para que salte un mensaje de error durante el manejo de una partida

    Métodos:
    --------
    __init__(self, pieza : "Pieza", error : str, *args) -> None:
        Inicializa la excepción con el mensaje de error y, a veces, con el causante del problema

    __str__(self) -> str:
        Imprime por pantalla el error causado durante la partida.
    """
    def __init__(self, error : str, problema : Union["Pieza",str,None] = None, *args) -> None:
        """
        Inicializa la excepción con el mensaje de error y, a veces, con el causante del problema

        Parametros:
        -----------
        error : str
            Mensaje del error o problema exacto.

        problema : Optional["Pieza",str]
            Causante del error. Puede ser una pieza o algo más concreto (jugador, error al comprobar tablas, etc).

        args
            Resto de argumentos innecesarios para nuestra clase.
        """
        super().__init__(*args)
        self.problema : Union["Pieza",str,None] = problema
        self.error : str = error

    def __str__(self) -> str:
        """
        Imprime por pantalla el error causado durante la partida

        Retorna:
        --------
        str
            Devuelve el mensaje del error que se ha producido durante la partida.
        """
        return f'Problemas con {self.problema}: {self.error}' if not isinstance(self.problema, Pieza) and self.problema is not None else (
            f'Problemas con la pieza {type(self.problema).__name__}: {self.error}' if isinstance(self.problema, Pieza) else
            f'Problemas en la partida: {self.error}'
        )