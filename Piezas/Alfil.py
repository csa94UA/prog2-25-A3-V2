from Piezas.Pieza import Pieza

"""
Modulo para la gestión y uso de un alfil

Este módulo define la clase 'Alfil' que representa un alifl concreto de la partida.
Posee solamente los módulos básicos definidos de la superclase 'Pieza' a la que pertenece.

Clases:
    - Alfil
"""

class Alfil(Pieza):
    """
    Clase que representa un alfil concreto

    Atributos:
    -----------
    posicion : list[int,int]
        Posicíon concreta del alfil
    color : bool
        Color del alfil (1 es blanco y 0 es negro)
    capturado : bool
        Marca si está capturado el alfil
    valor : int
        Valor del alfil
    movimientos : list[(int,int)]
        Lista de movimientos válidos del alfil

    Métodos:
    -----------
    movimiento_valido() -> list[(int,int)]
        Devuelve el conjunto de posiciones validas que puede tener.
    """

    def __init__(self, posicion : list[int,int], color : bool) -> None:
        """
        Inicializa una instacia de la clase Alfil

        Parámetros:
        -----------
        posicion : list[int,int]
            Posicíon concreta del alfil
        color : bool
            Color del alfil (1 es blanco y 0 es negro)
        """
        super().__init__(posicion,color)

    def movimiento_valido(self, tablero: "Tablero") -> list[(int,int)]:
        """
        Comprueba todos los movimientos válidos del alfil

        Parametros:
        -----------
        tabelro : list[list[int]]
            Tablero en sí
        Retorna:
        --------
        list[(int,int)]
            Retorna una lista de movimientos válidos del alfil
        """

        fila, columna = self.posicion
        movimientos = []

        # Estos bucles for acceden solamente a la diagonal que me interesa
        for k in range(1, min(8 - fila, columna + 1)):
            i = fila + k
            j = columna - k
            if tablero[i][j].ocupado:
                break
            movimientos.append(tuple[i,j])

        for k in range(1, min(fila + 1, 8 - columna)):
            i = fila - k
            j = columna + k
            if tablero[i][j].ocupado:
                break
            movimientos.append(tuple[i,j])

        for k in range(1, min(fila + 1, columna + 1)):
            i = fila - k
            j = columna - k
            if tablero[i][j].ocupado:
                break
            movimientos.append(tuple[i,j])

        for k in range(1, min(8 - fila, 8 - columna)):
            i = fila + k
            j = columna + k
            if tablero[i][j].ocupado:
                break
            movimientos.append(tuple[i,j])

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