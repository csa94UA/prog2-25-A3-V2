"""
Módulo que define el comportamiento del peón en el ajedrez.

Clases:
-------
- Peon
"""

from typing import List, Tuple
from piezas.pieza_base import Pieza
from juego.validador_movimiento import ValidadorMovimiento


class Peon(Pieza):
    """
    Clase que representa un peón en el ajedrez.

    Implementa la lógica del movimiento normal, doble paso inicial, captura diagonal y captura al paso (en passant).
    """

    def __init__(self, color: str) -> None:
        """
        Inicializa un peón con su color y estado de movimiento.

        Parámetros:
        -----------
        color : str
            'blanco' o 'negro'.
        """
        super().__init__(color)
        self.se_ha_movido = False

    def simbolo(self) -> str:
        """
        Retorna el símbolo unicode correspondiente al peón.

        Retorna:
        --------
        str
            '♙' para blanco, '♟' para negro.
        """
        return '♙' if self.color == 'blanco' else '♟'

    def obtener_movimientos_validos(
        self,
        posicion: Tuple[int, int],
        tablero,
        evitar_jaque: bool = True,
        noatacando: bool = False
    ) -> List[Tuple[int, int]]:
        """
        Calcula los movimientos válidos del peón, incluyendo en passant.

        Parámetros:
        -----------
        posicion : Tuple[int, int]
            Posición actual del peón en el tablero.
        tablero : Tablero
            Objeto que contiene el estado del tablero y el último movimiento realizado.
        evitar_jaque : bool
            Si True, se filtran movimientos que dejen al rey propio en jaque.
        noatacando : bool
            Si True, se omiten los movimientos hacia adelante (usado para validación de jaque).

        Retorna:
        --------
        List[Tuple[int, int]]
            Lista de coordenadas válidas donde el peón puede moverse.
        """
        fila, columna = posicion
        direccion = -1 if self.color == 'blanco' else 1
        movimientos_potenciales: List[Tuple[int, int]] = []

        # Movimiento hacia adelante
        if not noatacando:
            if self._esta_vacio(tablero.casillas, fila + direccion, columna):
                movimientos_potenciales.append((fila + direccion, columna))
                if not self.se_ha_movido and self._esta_vacio(tablero.casillas, fila + 2 * direccion, columna):
                    movimientos_potenciales.append((fila + 2 * direccion, columna))

        # Capturas diagonales y en passant
        for desplazamiento_columna in [-1, 1]:
            nueva_columna = columna + desplazamiento_columna
            nueva_fila = fila + direccion

            if 0 <= nueva_fila < 8 and 0 <= nueva_columna < 8:
                objetivo = tablero.casillas[nueva_fila][nueva_columna]
                if objetivo and self.es_oponente(objetivo):
                    movimientos_potenciales.append((nueva_fila, nueva_columna))

                # Captura al paso
                if not noatacando and tablero.ultimo_movimiento:
                    origen, destino, pieza_movida = tablero.ultimo_movimiento
                    if (
                        isinstance(pieza_movida, Peon)
                        and abs(destino[0] - origen[0]) == 2
                        and destino[0] == fila
                        and destino[1] == nueva_columna
                        and self.es_oponente(pieza_movida)
                    ):
                        movimientos_potenciales.append((fila + direccion, nueva_columna))

        if evitar_jaque:
            resguardo = tablero.guardar_estado()
            validador = ValidadorMovimiento(tablero)
            movimientos_legales = validador.filtrar_movimientos_legales(posicion, movimientos_potenciales, True)
            tablero.restaurar_estado(resguardo)
            return movimientos_legales

        return movimientos_potenciales

    def _esta_vacio(self, casillas, fila: int, columna: int) -> bool:
        """
        Verifica si una casilla está vacía y dentro del tablero.

        Parámetros:
        -----------
        casillas : List[List[Pieza | None]]
            Matriz del tablero.
        fila : int
        columna : int

        Retorna:
        --------
        bool
        """
        return 0 <= fila < 8 and 0 <= columna < 8 and casillas[fila][columna] is None
