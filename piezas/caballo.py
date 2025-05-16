"""
Módulo que define el comportamiento del caballo en el ajedrez.

Clases:
-------
- Caballo
"""

from typing import List, Tuple
from piezas.pieza_base import Pieza
from juego.validador_movimiento import ValidadorMovimiento


class Caballo(Pieza):
    """
    Clase que representa un caballo en el ajedrez.

    Hereda de la clase base `Pieza` e implementa el comportamiento específico
    del caballo, que se mueve en forma de L y puede saltar sobre otras piezas.

    Métodos:
    --------
    simbolo() -> str:
        Retorna el símbolo unicode que representa al caballo según su color.
    obtener_movimientos_validos(posicion, tablero, evitar_jaque=True, noatacando=False) -> List[Tuple[int, int]]:
        Devuelve una lista de movimientos válidos considerando las reglas del juego y jaque.
    """

    def __init__(self, color: str) -> None:
        """
        Inicializa un caballo con el color dado.

        Parámetros:
        -----------
        color : str
            'blanco' o 'negro'.
        """
        super().__init__(color)

    def simbolo(self) -> str:
        """
        Retorna el símbolo unicode correspondiente al caballo.

        Retorna:
        --------
        str
            '♘' para blanco, '♞' para negro.
        """
        return '♘' if self.color == 'blanco' else '♞'

    def obtener_movimientos_validos(
        self,
        posicion: Tuple[int, int],
        tablero,
        evitar_jaque: bool = True,
        noatacando: bool = False
    ) -> List[Tuple[int, int]]:
        """
        Calcula los movimientos válidos del caballo desde la posición actual.

        El caballo se mueve en forma de L: dos casillas en una dirección y una en la otra.
        Puede saltar sobre otras piezas.

        Parámetros:
        -----------
        posicion : Tuple[int, int]
            Posición actual del caballo en el tablero.
        tablero : Tablero
            Referencia al tablero actual del juego.
        evitar_jaque : bool
            Si True, filtra movimientos que dejen al rey en jaque.
        noatacando : bool
            Ignorado por el caballo, aceptado para mantener compatibilidad con otras piezas.

        Retorna:
        --------
        List[Tuple[int, int]]
            Lista de coordenadas válidas donde el caballo puede moverse.
        """
        fila, columna = posicion
        movimientos_posibles = [ # Saltos en L
            (fila + 2, columna + 1), (fila + 2, columna - 1),
            (fila - 2, columna + 1), (fila - 2, columna - 1),
            (fila + 1, columna + 2), (fila + 1, columna - 2),
            (fila - 1, columna + 2), (fila - 1, columna - 2),
        ]

        movimientos_potenciales: List[Tuple[int, int]] = []

        for nueva_fila, nueva_columna in movimientos_posibles:
            if 0 <= nueva_fila < 8 and 0 <= nueva_columna < 8:
                casilla = tablero.casillas[nueva_fila][nueva_columna]
                if casilla is None or self.es_oponente(casilla):
                    movimientos_potenciales.append((nueva_fila, nueva_columna))

        if evitar_jaque:
            resguardo = tablero.guardar_estado()
            validador = ValidadorMovimiento(tablero)
            movimientos_legales = validador.filtrar_movimientos_legales(
                posicion, movimientos_potenciales, evitar_jaque=True
            )
            tablero.restaurar_estado(resguardo)
            return movimientos_legales

        return movimientos_potenciales
