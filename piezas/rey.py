"""
Módulo que define el comportamiento del rey en el ajedrez.

Clases:
-------
- Rey
"""

from piezas.pieza_base import Pieza
from piezas.torre import Torre

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
    obtener_movimientos_validos(posicion, tablero, noatacando=False) -> list:
        Calcula movimientos legales del rey.
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

    def obtener_movimientos_validos(self, posicion, tablero, noatacando=False):
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
        
        
        # Movimientos normales del rey (una casilla en cualquier dirección)
        direcciones = [
            (-1, -1), (-1, 0), (-1, 1),
            ( 0, -1),          ( 0, 1),
            ( 1, -1), ( 1, 0), ( 1, 1)
        ]

        for df, dc in direcciones:
            nueva_fila, nueva_columna = fila + df, columna + dc
            if 0 <= nueva_fila < 8 and 0 <= nueva_columna < 8:
                casilla = tablero.casillas[nueva_fila][nueva_columna]
                if casilla is None or self.es_oponente(casilla):
                    movimientos_potenciales.append((nueva_fila, nueva_columna))

        if not noatacando and not self.se_ha_movido:
            fila_rey = 7 if self.color == 'blanco' else 0

            # Enroque corto (torre en columna 7)
            torre_corta = tablero.casillas[fila_rey][7]
            if isinstance(torre_corta, Torre) and not torre_corta.se_ha_movido:
                if all(tablero.casillas[fila_rey][c] is None for c in [5, 6]):
                    movimientos_potenciales.append((fila_rey, 6))

            # Enroque largo (torre en columna 0)
            torre_larga = tablero.casillas[fila_rey][0]
            if isinstance(torre_larga, Torre) and not torre_larga.se_ha_movido:
                if all(tablero.casillas[fila_rey][c] is None for c in [1, 2, 3]):
                    movimientos_potenciales.append((fila_rey, 2))

        return movimientos_potenciales
