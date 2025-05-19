"""
Modulo para la gestión de un jugador

Este modulo define la clase Jugador que contendra la información del usuario junto con sus piezas
que estarán dispoonibles cuando esté en partida

Clases:
    - Jugador
"""
from Piezas import Caballo, Alfil, Rey, Torre, Reina, Pieza, Peon
from typing import Union, Self

class Jugador:
    """
    Clase que repersenta al jugador

    Atributos:
    ----------
    nombre : str
        Nombre del jugador

    puntuacion : int
        Puntuacion del jugador (similar a su nivel)

    color : Union[int,None]
        Color del jugador. Al inicializarse no se define su color

    piezas : list
        Representa las piezas del jugador

    cantidad : dict
        Diccionario que marca la cantidad de cada tipo de pieza que tiene

    Métodos:
    --------
    __init__(self, nombre : str, puntuacion : int) -> None
        Inicializa un nuevo jugador

    añadir_pieza(self, pieza : Pieza) -> None
        Actualiza la cantidad de piezas de su inventario

    eliminar_pieza(self, pieza : Pieza) -> None
        Elimina la pieza de su inventario

    encontrar_rey(self) -> tuple[int,int]
        Busca la posición del rey

    __len__(self) -> int
        Mide cuantas piezas le quedan en su inventario

    __bool__(self) -> bool
        Comprueba si solo tiene el rey

    __sub__(self, other : "Pieza") -> "Jugador"
        Elimina una pieza de su invetario con la resta. También se aplica con __isub()__ y __rsub__()

    __add__(self, other : "Pieza") -> "Jugador"
        Añade una nueva pieza a su inventario con la suma. También se aplica con __iadd__() y __radd__()

    __repr__(self) -> str
        Devuelve la información del jugador de manera técnica (para trazas y análisis)
    """

    def __init__(self, nombre : str, puntuacion : int) -> None:
        """
        Inicializa una instacia de la clase Jugador

        Parámetros:
        -----------
        nombre : str
            Nombre del jugador

        puntuacion : bool
            Puntuacion que tiene el jugador. Refleja el nivel del jugador
        """
        self.nombre : str = nombre
        self.puntuacion : int = puntuacion
        self.color : Union[int,None] = None
        self.piezas : list = []
        self.cantidad : dict = {"P" : 0, "B" : 0, "N" : 0,
                               "R" : 0, "Q" : 0, "K" : 0}

    def añadir_pieza(self, pieza : Pieza) -> None:
        """
        Añade una pieza a su colección y lo cuenta

        Parámetros:
        -----------
        pieza : Pieza
            Pieza que va a ser añadida al equipo
        """

        if isinstance(pieza, Peon):
            self.cantidad["P"] += 1

        elif isinstance(pieza, Alfil):
            self.cantidad["B"] += 1

        elif isinstance(pieza, Caballo):
            self.cantidad["N"] += 1

        elif isinstance(pieza, Torre):
            self.cantidad["R"] += 1

        elif isinstance(pieza, Reina):
            self.cantidad["Q"] += 1

        elif isinstance(pieza, Rey):
            self.cantidad["K"] += 1

        self.piezas.append(pieza)

        return None

    def eliminar_pieza(self, pieza : Pieza) -> None:
        """
        Elimina la pieza en caso de ser capturada

        Parámetros:
        -----------
        pieza : Pieza
            Se trata de la pieza que va a ser eliminada

        """

        self.piezas.remove(pieza)

        return None
    
    def encontrar_rey(self) -> tuple[int,int]:
        """
        Elimina la pieza en caso de ser capturada

        Retorna:
        --------
        tuple
            Retorna una tupla con la posicion del rey

        """
        rey = None
        for pieza in self.piezas:
            if type(pieza).__name__ == "Rey":
                rey = pieza
                break

        posicion_rey = rey.posicion
        return posicion_rey

    def __len__(self) -> int:
        """
        Método dunder para devolver el número de piezas que tiene el jugador

        Retorna:
        --------
        int
            Número de piezas que tiene el jugador

        """
        return len(self.piezas)

    def __bool__(self) -> bool:
        """
        Método dunder que comprueba si solo le queda el rey

        Retorna:
        --------
        bool
            Devuelve True si tiene más piezas a parte del rey
        """

        return False if self.encontrar_rey() or len(self) == 1 else True

    def __sub__(self, other : "Pieza") -> "Jugador":
        """
        Método dunder que elimina una pieza de la lista de piezas del jugador

        Retorna:
        --------
        Jugador
            Devuelve un nuevo objeto de la clase jugador con los atributos actualizados
        """
        if not isinstance(other, Pieza):
            print("Error. Se ha intentado eliminar de la lista de piezas algo que no es una pieza")
            return self

        jugador = Jugador(self.nombre, self.puntuacion)

        for pieza in self.piezas:
            if other == pieza:
                self.piezas.remove(other)
                break

        else:
            print(f"No se ha encontrado la pieza {other} en el jugdaor {self.nombre}")

        jugador.color = self.color
        jugador.piezas = self.piezas
        jugador.cantidad = self.cantidad

        return jugador

    def __rsub__(self, other : "Pieza") -> "Jugador":
        """
        Método dunder que elimina una pieza de la lista de piezas del jugador

        Retorna:
        --------
        Jugador
            Devuelve un nuevo objeto de la clase jugador con los atributos actualizados
        """
        return self - other

    def __isub__(self, other : "Pieza") -> Self:
        """
        Método dunder que elimina una pieza de la lista de piezas del jugador

        Retorna:
        --------
        Self
            Devuelve su propia instancia con los atributos actualizados
        """
        if not isinstance(other, Pieza):
            print("Error. Se ha intentado eliminar de la lista de piezas algo que no es una pieza")
            return self

        for pieza in self.piezas:
            if other == pieza:
                self.piezas.remove(other)
                break

        else:
            print(f"No se ha encontrado la pieza {other} en el jugdaor {self.nombre}")

        return self

    def __add__(self, other : "Pieza") -> "Jugador":
        """
        Método dunder que añade una pieza de la lista de piezas del jugador

        Retorna:
        --------
        Jugador
            Devuelve un nuevo objeto de la clase jugador con los atributos actualizados
        """
        if not isinstance(other, Pieza):
            print("Error. Se ha intentado eliminar de la lista de piezas algo que no es una pieza")
            return self

        jugador = Jugador(self.nombre, self.puntuacion)

        self.piezas.insert(0,other)

        jugador.color = self.color
        jugador.piezas = self.piezas
        jugador.cantidad = self.cantidad

        return jugador

    def __radd__(self, other : "Pieza") -> "Jugador":
        """
        Método dunder que añade una pieza de la lista de piezas del jugador

        Retorna:
        --------
        Jugador
            Devuelve un nuevo objeto de la clase jugador con los atributos actualizados
        """
        return self + other

    def __iadd__(self, other : "Pieza") -> Self:
        """
        Método dunder que añade una pieza de la lista de piezas del jugador

        Retorna:
        --------
        Self
            Devuelve su propia instancia con los atributos actualizados
        """
        if not isinstance(other, Pieza):
            print("Error. Se ha intentado eliminar de la lista de piezas algo que no es una pieza")
            return self

        self.piezas.insert(0, other)

        return self

    def __repr__(self):
        """
        Metodo especial para mostrar toda la información de la clase

        Retorna:
        --------
        str
            Retorna un str con toda la información
        """

        return f"{type(self).__name__}(nombre = {self.nombre}, puntuacion = {self.puntuacion}, \
        color =  {str(1) if self.color else str(0)}, piezas = {self.piezas}, cantidad = {self.cantidad})"