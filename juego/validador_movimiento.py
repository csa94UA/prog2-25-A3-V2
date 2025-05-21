"""
Módulo que contiene la lógica de validación de movimientos en el ajedrez.

La clase `ValidadorMovimiento` se encarga de determinar si los movimientos son legales,
si un jugador está en jaque y de filtrar movimientos inválidos para proteger al rey.

Clases:
-------
- ValidadorMovimiento
"""

from typing import List, Optional, Tuple


class ValidadorMovimiento:
    """
    Clase responsable de validar movimientos en el ajedrez.

    Esta clase permite verificar condiciones como el jaque, movimientos legales y filtrar
    aquellos que dejan al rey expuesto.

    Atributos:
    ----------
    tablero : Tablero
        Referencia al tablero actual del juego.

    Métodos:
    --------
    esta_en_jaque(color: str) -> bool:
        Determina si el rey del color dado está en jaque.
    movimiento_es_legal(origen: Tuple[int, int], destino: Tuple[int, int], color: str) -> bool:
        Verifica si el movimiento es legal.

    """

    def __init__(self, tablero) -> None:
        """
        Inicializa el validador con una referencia al tablero.

        Parámetros:
        -----------
        tablero : Tablero
            El tablero actual del juego.
        """
        self.tablero = tablero

    def esta_en_jaque(self, color: str) -> bool:
        """
        Determina si el rey del color dado está en jaque.

        Parámetros:
        -----------
        color : str
            Color del rey ('blanco' o 'negro').

        Retorna:
        --------
        bool
            True si el rey está en jaque, False en caso contrario.
        """
        rey_pos = self._encontrar_rey(color)
        if not rey_pos:
            return False

        for fila in range(8):
            for col in range(8):
                pieza = self.tablero.casillas[fila][col]
                if pieza and pieza.color != color:
                    movimientos = pieza.obtener_movimientos_validos(
                        (fila, col), self.tablero, noatacando=True
                    )
                    if rey_pos in movimientos and self.movimiento_es_legal((fila,col),rey_pos,pieza.color):
                        return True

        return False

    def movimiento_es_legal(
        self, origen: Tuple[int, int], destino: Tuple[int, int], color: str
    ) -> bool:
        """
        Verifica si el movimiento es legal: la pieza puede moverse y no deja en jaque al propio rey.

        Parámetros:
        -----------
        origen : Tuple[int, int]
            Coordenadas de la casilla de origen.
        destino : Tuple[int, int]
            Coordenadas de la casilla de destino.
        color : str
            Color del jugador actual.

        Retorna:
        --------
        bool
            True si el movimiento es legal, False en caso contrario.
        """
        pieza = self.tablero.casillas[origen[0]][origen[1]]
        if (
            pieza is None or
            pieza.color != color or
            destino not in pieza.obtener_movimientos_validos(origen, self.tablero)
        ):
            return False

        self.tablero.hacer_movimiento(origen,destino)
        es_legal = not self.esta_en_jaque(color)
        self.tablero.deshacer_ultimo_movimiento()
        return es_legal

    def _encontrar_rey(self, color: str) -> Optional[Tuple[int, int]]:
        """
        Encuentra la posición del rey del color dado.

        Parámetros:
        -----------
        color : str
            Color del rey que se busca.

        Retorna:
        --------
        Optional[Tuple[int, int]]
            Coordenadas del rey, o None si no se encuentra.
        """
        for fila in range(8):
            for col in range(8):
                pieza = self.tablero.casillas[fila][col]
                if pieza and pieza.color == color and pieza.__class__.__name__ == "Rey":
                    return (fila, col)
        return None
