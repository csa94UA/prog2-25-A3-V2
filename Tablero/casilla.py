"""
Modulo para la gestión y uso de una casilla del tablero

Este módulo define la clase 'Casilla' que representa una casilla concreta del tablero
y contiene la información más esencial. Posee modulos que permite realizar las funciones básicas.

Clases:
    - Casilla
"""

from typing import Union

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
    __init__(self, fila : int, columna : int) -> None
        Inicializa una nueva casilla

    conquistado(Pieza) -> None
        Actualiza los atributos de la casilla al ser tomada por una pieza.

    tranformacion_a_pieza(self, fila : int, columna : int, simbolo : str) -> None
        Inicializa la casilla con la clase correspondiente. Usado en el formato FEN

    __str__(self) -> str
        Representa la pieza que ocupa la casilla según la clase de pieza que sea y su color.

    __repr__(self) -> str
        Otorga información tecnica de la casilla para trazas y análisis.
    """

    def __init__(self, fila : int, columna : int) -> None:
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

    def tranformacion_a_pieza(self, fila : int, columna : int, simbolo : str) -> None:
        """
        Inicializa la casilla con la pieza correspondiente. Es usado para transformar el formato FEN a un tablero

        Parametros:
        -----------
        fila : int
            Fila en la que se encuentra la casilla.

        columna : int
            Columna en la que se encuentra la casilla.

        simbolo : str
            Simbolo de la pieza.
        """
        from Piezas import Caballo, Alfil, Rey, Torre, Reina, Peon

        match(simbolo.upper()):
            case 'K':
                self.pieza = Rey((fila, columna), 1 if simbolo.lower() != simbolo else 0)
            case 'Q':
                self.pieza = Reina((fila,columna), 1 if simbolo.lower() != simbolo else 0)
            case 'N':
                self.pieza = Caballo((fila,columna), 1 if simbolo.lower() != simbolo else 0)
            case 'B':
                self.pieza = Alfil((fila,columna), 1 if simbolo.lower() != simbolo else 0)
            case 'R':
                self.pieza = Torre((fila,columna), 1 if simbolo.lower() != simbolo else 0)
            case 'P':
                self.pieza = Peon((fila,columna), 1 if simbolo.lower() != simbolo else 0)
            case '_':
                print(f"Error. No se ha encontrado una pieza válida para el símbolo {simbolo}")

        return None

    def __str__(self) -> str:
        """
        Metodo dunder que retorna el simbolo que representa la pieza que contiene la casilla

        Retorna:
        ---------
        str
            Devuelve el simbolo correspondiente a la pieza y su color
        """

        return '.' if self.pieza is None else str(self.pieza)

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
    print(casilla)