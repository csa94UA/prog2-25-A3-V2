"""
Modulo para la gestión y uso de una casilla del tablero

Este módulo define la clase 'Casilla' que representa una casilla concreta del tablero
y contiene la información más esencial. Posee modulos que permite realizar las funciones básicas.

Clases:
    - Casilla
"""

from typing import Union, TYPE_CHECKING
#if TYPE_CHECKING:
#    from Piezas import Caballo, Alfil, Rey, Torre, Reina, Pieza, Peon

class Casilla:
    """
    Clase que representa una casilla

    Atributos:
    -----------
    fila : int
        Fila en la que se encuentra la casilla
    columna : int
        Columna en la que se encuentra la casilla
    ocupado : bool
        Marca si está ocupado
    pieza : Union[Pieza,None]
        Contiene la pieza que ocupa la casilla
    amenazado : bool
        Valor booleano que representa si alguna pieza puede ir a la casilla

    Métodos:
    -----------
    conquistado(Pieza) -> None:
        Actualiza los atributos de la casilla al ser tomada por una pieza.
    representacion() -> str:
        Representa la pieza que ocupa la casilla según la clase de pieza que sea y su color.
    """

    def __init__(self, fila : int, columna : int):
        """
        Inicializa una instacia de la clase Casilla

        Parámetros:
        -----------
        fila : int
            Fila que ocupa la casilla
        columna : int
            Columna que ocupa la casilla
        """
        self.fila : int = fila
        self.columna : int = columna
        self.ocupado : bool = False
        self.pieza : Union["Pieza",None] = None
        self.amenazado : bool = False

    def conquistado(self, pieza : "Pieza") -> None:
        """
        Establece la ocupación de la pieza en la casilla

        Parametros:
        -----------
        pieza : Pieza
            Pieza que va a ocupar el espacio
        """
        self.pieza : Pieza = pieza
        self.ocupado : bool = True

        return None

    def representacion(self) -> str:
        """
        Metodo que retorna el simbolo que representa la pieza que contiene la casilla

        Retorna:
        ---------
        str
            Devuelve el simbolo correspondiente a la pieza y su color
        """
        #from Piezas import Caballo, Alfil, Rey, Torre, Reina, Peon
        pieza : Union[Pieza,None] = self.pieza

        if type(pieza).__name__ == "Peon":
            return 'P' if pieza.color else 'p'

        if type(pieza).__name__ == "Torre":
            return 'R' if pieza.color else 'r'

        if type(pieza).__name__ == "Caballo":
            return 'N' if pieza.color else 'n'

        if type(pieza).__name__ == "Alfil":
            return 'B' if pieza.color else 'b'

        if type(pieza).__name__ == "Reina":
            return 'Q' if pieza.color else 'q'

        if type(pieza).__name__ == "Rey":
            return 'K' if pieza.color else 'k'

        return '·'

    def __repr__(self):
        """
        Metodo especial para mostrar toda la información de la clase

        Retorna:
        --------
        str
            Retorna un str con toda la información
        """
        pieza : str = repr(self.pieza) if self.pieza is not None else "None"
        return (f"{type(self).__name__}(Posición -> ({self.fila},{self.columna}), "
            f"Ocupado -> {self.ocupado}, Pieza -> {pieza}, "
            f"Amenazado -> {self.amenazado})")

if __name__ == "__main__":
    from Piezas import Caballo, Alfil, Rey, Torre, Reina, Pieza, Peon
    casilla = Casilla(1,2)
    pieza = Rey((1,2),0)
    casilla.conquistado(pieza)
    print(repr(casilla))
    print(casilla.representacion())