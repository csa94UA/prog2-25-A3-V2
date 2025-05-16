"""
Módulo base para definir piezas de ajedrez.

Este módulo contiene una clase abstracta `Pieza` que representa el comportamiento común de todas las piezas del ajedrez.
Proporciona una interfaz para obtener movimientos válidos, representar la pieza con un símbolo y verificar si una pieza es oponente.

Clases:
    - Pieza

"""

from abc import ABC, abstractmethod
from typing import List, Optional, Tuple, Any


class Pieza(ABC):
    """
    Clase abstracta base para todas las piezas de ajedrez.

    Atributos:
    ----------
    color : str
        Color de la pieza ('blanco' o 'negro').
    valor : int
        Valor numérico de la pieza para evaluar su importancia (por defecto 0).

    Métodos abstractos:
    -------------------
    obtener_movimientos_validos(posicion, tablero, evitar_jaque=True, noatacando=False) -> List[Tuple[int, int]]:
        Devuelve una lista de posiciones válidas a las que esta pieza puede moverse.
    simbolo() -> str:
        Devuelve un símbolo textual para representar la pieza en consola/tablero.

    Métodos concretos:
    ------------------
    es_oponente(otra_pieza: Optional['Pieza']) -> bool:
        Indica si la otra pieza es del color contrario.
    clonar() -> 'Pieza':
        Retorna una copia de la pieza actual, incluyendo ciertos atributos adicionales si existen.
    """

    def __init__(self, color: str) -> None:
        self.color: str = color
        self.valor: int = 0

    @abstractmethod
    def obtener_movimientos_validos(
        self,
        posicion: Tuple[int, int],
        tablero: List[List[Optional['Pieza']]],
        evitar_jaque: bool = True,
        noatacando: bool = False
    ) -> List[Tuple[int, int]]:
        """
        Devuelve una lista de posiciones válidas a las que esta pieza puede moverse desde una posición dada.

        Parámetros:
        -----------
        posicion : Tuple[int, int]
            Coordenadas actuales de la pieza en el tablero (fila, columna).
        tablero : List[List[Optional[Pieza]]]
            Matriz 8x8 que representa el tablero actual.
        evitar_jaque : bool, opcional
            Si es True, filtra los movimientos que dejarían al rey en jaque.
        noatacando : bool, opcional
            Si es True, devuelve movimientos que no impliquen ataques (por ejemplo, para validar protecciones).

        Retorna:
        --------
        List[Tuple[int, int]]
            Lista de posiciones válidas a las que esta pieza puede moverse.
        """
        pass

    @abstractmethod
    def simbolo(self) -> str:
        """
        Devuelve un símbolo textual que representa esta pieza.

        Retorna:
        --------
        str
            Símbolo que representa gráficamente la pieza.
        """
        pass

    def es_oponente(self, otra_pieza: Optional['Pieza']) -> bool:
        """
        Indica si la otra pieza es del color contrario.

        Parámetros:
        -----------
        otra_pieza : Optional[Pieza]
            Pieza con la que se compara.

        Retorna:
        --------
        bool
            True si la otra pieza no es None y tiene color diferente.
        """
        return otra_pieza is not None and self.color != otra_pieza.color

    def clonar(self) -> 'Pieza':
        """
        Retorna una copia de la pieza actual.

        Si la pieza tiene atributos adicionales como 'se_ha_movido', también se copian.

        Retorna:
        --------
        Pieza
            Nueva instancia de la misma clase con los mismos atributos.
        """
        clase = self.__class__
        clon = clase(self.color)
        clon.valor = self.valor
        if hasattr(self, 'se_ha_movido'):
            clon.se_ha_movido = self.se_ha_movido
        return clon
