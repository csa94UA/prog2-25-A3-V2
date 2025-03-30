from Piezas.Pieza import Pieza

"""
Modulo para la gestión y uso de un caballo

Este módulo define la clase 'Caballo' que representa un caballo concreto de la partida.
Posee solamente los módulos básicos definidos de la superclase 'Pieza' a la que pertenece.

Clases:
    - Caballo
"""

class Caballo(Pieza):
    """
    Clase que representa un caballo concreto

    Atributos:
    -----------
    posicion : list[int,int]
        Posicíon concreta del caballo
    color : bool
        Color del caballo (1 es blanco y 0 es negro)
    capturado : bool
        Marca si está capturado el caballo
    valor : int
        Valor del caballo
    movimientos : list[(int,int)]
        Lista de movimientos válidos del caballo

    Métodos:
    -----------
    movimiento_valido() -> list[(int,int)]
        Devuelve el conjunto de posiciones validas que puede tener.
    """

    def __init__(self, posicion : tuple[int,int], color : int) -> None:
        """
        Inicializa una instacia de la clase Caballo
        Parámetros:
        -----------
        posicion : list[int,int]
            Posicíon concreta del caballo
        color : bool
            Color del caballo (1 es blanco y 0 es negro)
        """
        super().__init__(posicion,color)

    def movimiento_valido(self, tablero: "Tablero") -> list[(int,int)]:
        """
        Comprueba todos los movimientos válidos del caballo
        Parametros:
        -----------
        tabelro : Tablero
            Tablero en sí
        Retorna:
        --------
        list[tuple(int,int)]
            Retorna una lista de movimientos válidos del caballo
        """
        movimientos_posibles = [(1,2),(1,-2),(2,1),(2,-1),(-1,2),(-1,-2),(-2,1),(-2,-1)]
        movimientos = []

        for fila, columna in movimientos_posibles:
            if not tablero[fila][columna].ocupado:
                movimientos.append((fila,columna))

        return movimientos

    def __repr__(self):
        """
        Metodo especial para mostrar toda la información de la clase

        Retorna:
        --------
        str
            Retorna un str con toda la información
        """
        return super().__repr__()