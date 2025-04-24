"""
Módulo de excepciones hecha para las piezas.

Este módulo en concreto se encarga de mostrar por pantalla errores personalizados a la hora de intentar crear una pieza,
ya sea porque se crea una pieza en una posición ocupada, se intenta crear una pieza idéntica a otra, etc.

Clases:
    ErrorCrearPieza
"""
from Piezas import Pieza


class ErrorCrearPieza(Exception):
    """
    Excepcion personalizada para que salte un mensaje de error al crear una pieza.

    Métodos:
    --------
    __init__(self, pieza : "Pieza", error : str, *args) -> None:
        Inicializa la excepción con la pieza que se ha intentado crear junto con el error concreto que lo ha provocado.

    __str__(self) -> str:
        Imprime por pantalla el error.
    """

    def __init__(self, pieza : "Pieza", error : str, bandera : bool = False, *args) -> None:
        """
        Inicializa la excepción con la pieza que se ha intentado crear junto con el error concreto que lo ha provocado.

        Parametros:
        -----------
        pieza : "Pieza"
            Pieza que se ha intentado crear.

        error : str
            Mensaje del error o problema exacto.

        args
            Resto de argumentos innecesarios para nuestra clase.
        """
        super().__init__(*args)
        self.pieza_existente : "Pieza" = pieza
        self.error : str = error
        self.bandera : bool = bandera

    def __str__(self) -> str:
        """
        Imprime por pantalla el error.

        Retorna:
        --------
        str
            Devuelve el mensaje del error que ha provocado la pieza al ser creada.
        """
        return f"Problemas con la pieza {type(self.pieza_existente).__name__}: {self.error}" if self.bandera else \
        f'{self.error}'