"""
Módulo que define el comportamiento del alfil en el ajedrez.

Clases:
-------
- Alfil
"""

from typing import List, Tuple
from piezas.pieza_base import Pieza


class Alfil(Pieza):
    """
    Clase que representa un alfil en el ajedrez.

    Hereda de la clase base `Pieza` e implementa el comportamiento específico
    del alfil, que se mueve en diagonales.

    Métodos:
    --------
    simbolo() -> str:
        Retorna el símbolo unicode que representa al alfil según su color.
    obtener_movimientos_validos(posicion, tablero, noatacando=False) -> List[Tuple[int, int]]:
        Devuelve una lista de movimientos válidos considerando reglas del juego 
    """

    def __init__(self, color: str) -> None:
        """
        Inicializa un alfil con el color dado.

        Parámetros:
        -----------
        color : str
            'blanco' o 'negro'.
        """
        super().__init__(color)
        self.valor = 333 # Valor asignado por AlphaZero

    def simbolo(self) -> str:
        """
        Retorna el símbolo unicode correspondiente al alfil.

        Retorna:
        --------
        str
            '♗' para blanco, '♝' para negro.
        """
        return '♗' if self.color == 'blanco' else '♝'

    def obtener_movimientos_validos(
        self,
        posicion: Tuple[int, int],
        tablero,
        noatacando: bool = False
    ) -> List[Tuple[int, int]]:
        """
        Calcula los movimientos válidos del alfil desde la posición actual.

        El alfil se mueve en las cuatro diagonales hasta encontrarse con una pieza.

        Parámetros:
        -----------
        posicion : Tuple[int, int]
            Posición actual del alfil en el tablero.
        tablero : Tablero
            Referencia al tablero actual del juego.
        noatacando : bool
            Ignorado por el alfil, pero aceptado para compatibilidad con otras piezas.

        Retorna:
        --------
        List[Tuple[int, int]]
            Lista de coordenadas válidas donde el alfil puede moverse.
        """
        fila, columna = posicion
        movimientos_potenciales = []
        direcciones = [(-1, -1), (-1, 1), (1, -1), (1, 1)]  # diagonales

        for df, dc in direcciones:
            nueva_fila, nueva_columna = fila + df, columna + dc
            while 0 <= nueva_fila < 8 and 0 <= nueva_columna < 8:
                casilla = tablero.casillas[nueva_fila][nueva_columna]
                if casilla is None:
                    movimientos_potenciales.append((nueva_fila, nueva_columna))
                elif self.es_oponente(casilla):
                    movimientos_potenciales.append((nueva_fila, nueva_columna))
                    break
                else:
                    break
                nueva_fila += df
                nueva_columna += dc

        return movimientos_potenciales
