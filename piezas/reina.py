"""
Define la clase Reina, una pieza que combina movimientos de alfil y torre.
"""

from typing import List, Tuple
from piezas.pieza_base import Pieza


class Reina(Pieza):
    """
    Clase que representa a la reina en el ajedrez.

    La reina puede moverse cualquier número de casillas en línea recta
    (horizontal, vertical o diagonal) mientras no encuentre obstáculos.
    """

    def __init__(self, color: str) -> None:
        """
        Inicializa una reina con su color.

        Parámetros:
        -----------
        color : str
            'blanco' o 'negro'
        """
        super().__init__(color)
        self.valor = 950 # Valor asignado por AlphaZero

    def simbolo(self) -> str:
        """
        Devuelve el símbolo Unicode correspondiente a la reina.

        Retorna:
        --------
        str
            '♕' para blancas, '♛' para negras.
        """
        return '♕' if self.color == 'blanco' else '♛'

    def obtener_movimientos_validos(
        self,
        posicion: Tuple[int, int],
        tablero,
        noatacando: bool = False
    ) -> List[Tuple[int, int]]:
        """
        Genera todos los movimientos válidos de la reina desde su posición actual.

        Parámetros:
        -----------
        posicion : Tuple[int, int]
            La posición actual de la reina.
        tablero : Tablero
            Referencia al estado del tablero.
        noatacando : bool
            Si True, se omiten los movimientos de ataque (usado internamente para ver amenazas).

        Retorna:
        --------
        List[Tuple[int, int]]
            Lista de coordenadas a las que la reina puede moverse legalmente.
        """
        fila, columna = posicion
        movimientos_potenciales: List[Tuple[int, int]] = []

        # Todas las direcciones posibles: diagonales, verticales y horizontales
        direcciones = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),          (0, 1),
            (1, -1),  (1, 0), (1, 1)
        ]

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
                    break  # Aliado bloqueando
                nueva_fila += df
                nueva_columna += dc

        return movimientos_potenciales
