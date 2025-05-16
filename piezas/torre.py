"""
Módulo que define el comportamiento de la torre en el ajedrez.

Clases:
-------
- Torre
"""

from piezas.pieza_base import Pieza
from juego.validador_movimiento import ValidadorMovimiento

class Torre(Pieza):
    """
    Clase que representa una torre en el ajedrez.

    Hereda de la clase base `Pieza` e implementa el movimiento lineal
    vertical y horizontal característico de la torre.

    Atributos:
    ----------
    se_ha_movido : bool
        Indica si la torre ya se ha movido (útil para enroque).

    Métodos:
    --------
    simbolo() -> str:
        Retorna el símbolo unicode de la torre según su color.
    obtener_movimientos_validos(posicion, tablero, evitar_jaque=True, noatacando=False) -> list:
        Calcula los movimientos válidos para la torre desde la posición dada,
        filtrando movimientos que dejarían en jaque si `evitar_jaque` es True.
    """

    def __init__(self, color):
        """
        Inicializa la torre con el color especificado.

        Parámetros:
        -----------
        color : str
            'blanco' o 'negro'
        """
        super().__init__(color)
        self.se_ha_movido = False
        self.valor = 5.63 # Valor asignado por AlphaZero

    def simbolo(self):
        """
        Devuelve el símbolo unicode que representa la torre.

        Retorna:
        --------
        str
            '♖' si es blanca, '♜' si es negra.
        """
        return '♖' if self.color == 'blanco' else '♜'

    def obtener_movimientos_validos(self, posicion, tablero, evitar_jaque=True, noatacando=False):
        """
        Calcula los movimientos válidos de la torre desde su posición actual.

        La torre se mueve en líneas verticales y horizontales hasta toparse
        con una pieza amiga o al capturar una pieza enemiga.

        Parámetros:
        -----------
        posicion : tuple (fila, columna)
            Coordenadas actuales de la torre.
        tablero : objeto Tablero
            Referencia al estado actual del tablero.
        evitar_jaque : bool
            Indica si se deben filtrar movimientos que dejan al rey en jaque.
        noatacando : bool
            Ignorado en esta pieza, para compatibilidad con otras.

        Retorna:
        --------
        list de tuplas (fila, columna)
            Lista de movimientos legales donde la torre puede desplazarse.
        """
        fila, columna = posicion
        movimientos_potenciales = []
        direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Movimientos verticales y horizontales

        for df, dc in direcciones:
            nueva_fila, nueva_columna = fila + df, columna + dc
            while 0 <= nueva_fila < 8 and 0 <= nueva_columna < 8:
                casilla = tablero.casillas[nueva_fila][nueva_columna]
                if casilla is None:
                    movimientos_potenciales.append((nueva_fila, nueva_columna))
                elif self.es_oponente(casilla):
                    movimientos_potenciales.append((nueva_fila, nueva_columna))
                    break
                else:  # Pieza amiga bloquea el camino
                    break
                nueva_fila += df
                nueva_columna += dc

        if evitar_jaque:
            resguardo = tablero.guardar_estado()
            validador = ValidadorMovimiento(tablero)
            movimientos_legales = validador.filtrar_movimientos_legales(posicion, movimientos_potenciales, evitar_jaque)
            tablero.restaurar_estado(resguardo)
            return movimientos_legales
        
        return movimientos_potenciales
