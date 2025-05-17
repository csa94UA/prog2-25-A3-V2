"""
Módulo que define el comportamiento del rey en el ajedrez.

Clases:
-------
- Rey
"""

from piezas.pieza_base import Pieza
from piezas.torre import Torre
from juego.validador_movimiento import ValidadorMovimiento

class Rey(Pieza):
    """
    Clase que representa al rey en el ajedrez.

    Hereda de la clase base `Pieza` e implementa los movimientos básicos
    del rey, incluyendo el enroque.

    Atributos:
    ----------
    se_ha_movido : bool
        Indica si el rey ya se ha movido (importante para enroque).

    Métodos:
    --------
    simbolo() -> str:
        Retorna el símbolo unicode del rey según su color.
    obtener_movimientos_validos(posicion, tablero, evitar_jaque=True, noatacando=False) -> list:
        Calcula movimientos legales del rey, filtrando movimientos que dejan en jaque.
    _movimientos_enroque(posicion, tablero) -> list:
        Calcula movimientos legales de enroque.
    _pasa_por_jaque(tablero, origen, casillas_enroque) -> bool:
        Verifica si alguna casilla por donde pasa el rey en el enroque está en jaque.
    """

    def __init__(self, color):
        """
        Inicializa el rey con el color dado.

        Parámetros:
        -----------
        color : str
            'blanco' o 'negro'
        """
        super().__init__(color)
        self.se_ha_movido = False
        self.valor = 1000000 # Valor amuy elevado para similar el infinito

    def simbolo(self):
        """
        Retorna el símbolo unicode que representa al rey.

        Retorna:
        --------
        str
            '♔' si es blanco, '♚' si es negro.
        """
        return '♔' if self.color == 'blanco' else '♚'

    def obtener_movimientos_validos(self, posicion, tablero, evitar_jaque=True, noatacando=False):
        """
        Calcula los movimientos legales del rey desde la posición actual.

        Incluye movimientos normales de una casilla en cualquier dirección
        y el enroque si es posible.

        Parámetros:
        -----------
        posicion : tuple (fila, columna)
            Posición actual del rey.
        tablero : objeto Tablero
            Estado actual del tablero.
        evitar_jaque : bool
            Si True, filtra movimientos que dejarían al rey en jaque.
        noatacando : bool
            Parámetro para compatibilidad, evita que el rey considere enroque
            en ciertos contextos.

        Retorna:
        --------
        list de tuplas (fila, columna)
            Movimientos legales disponibles para el rey.
        """
        fila, columna = posicion
        movimientos_potenciales = []
        validador = ValidadorMovimiento(tablero)
        
        # Movimientos normales del rey (una casilla en cualquier dirección)
        direcciones = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),           (0, 1),
            (1, -1),  (1, 0),  (1, 1)
        ]

        for df, dc in direcciones:
            nueva_fila, nueva_columna = fila + df, columna + dc
            if 0 <= nueva_fila < 8 and 0 <= nueva_columna < 8:
                casilla = tablero.casillas[nueva_fila][nueva_columna]
                if casilla is None or self.es_oponente(casilla):
                    movimientos_potenciales.append((nueva_fila, nueva_columna))

        # Enroque (solo si el rey no se ha movido, no está en jaque y no se ignora)
        if evitar_jaque:
            if not self.se_ha_movido and not validador.esta_en_jaque(self.color) and not noatacando:
                movimientos_potenciales += self._movimientos_enroque(posicion, tablero)

        # Filtrar movimientos que dejarían al rey en jaque
        resguardo = tablero.guardar_estado()
        
        movimientos_legales = validador.filtrar_movimientos_legales(posicion, movimientos_potenciales, evitar_jaque)
        tablero.restaurar_estado(resguardo)

        return movimientos_legales

    def _movimientos_enroque(self, posicion, tablero):
        """
        Calcula los movimientos legales de enroque para el rey.

        Parámetros:
        -----------
        posicion : tuple (fila, columna)
            Posición actual del rey.
        tablero : objeto Tablero
            Estado actual del tablero.

        Retorna:
        --------
        list de tuplas (fila, columna)
            Posibles posiciones finales del rey tras enroque.
        """
        fila_rey = 0 if self.color == 'blanco' else 7
        movimientos_enroque = []

        # Enroque corto (torre en la columna 7)
        torre_derecha = tablero.casillas[fila_rey][7]
        if (
            isinstance(torre_derecha, Torre) and
            not torre_derecha.se_ha_movido and
            all(tablero.casillas[fila_rey][c] is None for c in [5, 6])
        ):
            if not self._pasa_por_jaque(tablero, posicion, [(fila_rey, 5), (fila_rey, 6)]):
                movimientos_enroque.append((fila_rey, 6))

        # Enroque largo (torre en la columna 0)
        torre_izquierda = tablero.casillas[fila_rey][0]
        if (
            isinstance(torre_izquierda, Torre) and
            not torre_izquierda.se_ha_movido and
            all(tablero.casillas[fila_rey][c] is None for c in [1, 2, 3])
        ):
            if not self._pasa_por_jaque(tablero, posicion, [(fila_rey, 3), (fila_rey, 2)]):
                movimientos_enroque.append((fila_rey, 2))

        return movimientos_enroque

    def _pasa_por_jaque(self, tablero, origen, casillas_enroque):
        """
        Verifica si alguna casilla por la que pasa o termina el rey durante
        el enroque está bajo amenaza (en jaque).

        Parámetros:
        -----------
        tablero : objeto Tablero
            Estado actual del tablero.
        origen : tuple (fila, columna)
            Posición actual del rey.
        casillas_enroque : list de tuplas
            Casillas por las que el rey pasaría al enrocar.

        Retorna:
        --------
        bool
            True si alguna casilla está en jaque, False en caso contrario.
        """
        color = self.color
        resguardo = tablero.guardar_estado()
        for casilla in casillas_enroque:
            tablero.mover_pieza_tests((origen, casilla))
            if tablero.validador.esta_en_jaque(color):
                tablero.restaurar_estado(resguardo)
                return True
            tablero.restaurar_estado(resguardo)
        return False
