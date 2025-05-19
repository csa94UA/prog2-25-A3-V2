"""
Modulo para la gestión y uso de una pieza genérica

Este módulo define la clase abstracta 'Pieza' que representa una pieza de ajedrez genérica
y contiene la información más esencial. Posee modulos que permite realizar las funciones básicas.

Clases:
    - Tablero
"""
from .casilla import Casilla
#from Jugador import Jugador
from typing import Union, Self, Optional
import threading
import itertools
import pygame
import os

class Tablero:
    """
    Clase que representa un tablero

    Atributos:
    -----------
    tablero : list[list[Casilla]]
        Matriz donde cada elemento está formado por la clase Casilla

    enroque : Union[list[bool,bool],None]
        Contiene la información sobre la posibilidad de que las blancas y/o las negras hagan enroque

    en_passant : str
        Marca el lugar concreto donde se puede hacer en passant con coordenadas de ajedrez

    contador : int
        Cuenta las veces que se ha hecho semimovimientos

    jugadas : int
        Cuenta las jugadas repetidas

    turno : int
        Marca el número de turno de la partida

    Métodos:
    -----------
    __init__(self) -> None
        Inicializa un nuevo tablero

    creacion_con_FEN(cls, fen : str) -> Self
        Perimte una nueva forma de inicializar un tablero mediante el fen

    __getitem__(self, indice : int) -> Union[list["Casilla"],"Casilla"]
        Devuelve la lista de casillas o la casilla situado en el tablero

    __str__(self) -> str
        Muestra el tablero por pantalla. Tiene en cuenta la perspectiva del jugador que tiene turno

    esta_en_jaque(self, jugador:Jugador,enemigo:Jugador) -> bool:
        Detecta si un jugador se encuentra en jaque o no

    guardar_estado(self) -> dict:
        Guanda el estado del tablero en un diccionario

    restaurar_estado(self, estado: dict) -> None:
        Restaura el estado del tablero a partir de un diccionario obtenido del metodo guardar_estado()

    obtener_casilla(self, fila : int, columna : int) -> Casilla:
        Devuelve la casilla coherente a la perspectiva del jugador actual

    limite(fila : int, columna : int) -> bool:
        Comprueba si se ha digitado una posicion fuera de los limites

    mostrar_tablero(self, color : bool) -> None:
        Representa el tablero en función de la persepctiva del jugador actual

    traduccion_FEN(self, turno : int) -> str:
        Devuelve toda la información del tablero en formato FEN. Util para guardar partidas y comunicarse con otras IA

    casillas_intermedias(fila : int, columna : int, fila_m : int, columna_m : int) -> list[(int, int)]:
        Retorna las casillas intermedias entre dos piezas. Usado para comprobar las casillas problematicas dentro de un jaque

    quitar_permutaciones(self, mov : tuple, casillas_tocapelotas : list, fila : int, columna : int) -> None:
        Elimina las permutaciones que contengan a la posicoin de la pieza. Se usa para eliminar casillas intermedias

    jaque_in(self, fila : int, columna : int, jugador : "Jugador", enemigo : "Jugador") -> bool:
        Comprueba si el jaque es inevitable o no

    amenazas(self, enemigo : "Jugador", fila : int, columna : int) -> list:
        Revisa las piezas que amenazan una casilla

    casillas_amenazadas(self, amenazadores : list, fila : int, columna : int) -> list:
        Obtiene todas las casillas amenazadas entre la posición de cada pieza amenazadora y la posición de la pieza
        víctima. En ella se emplea la funcion casillas_intermedias (por eso su similitud), pero este tiene en cuenta
        el caso especial del caballo (que no tiene casillas intermedias)

    posibilidad_matar_con_rey(self, enemigo : "Jugador", fila : int, columna : int, rey : "Rey") -> bool
        Comprueba si la posicion (fila, columna) que contiene un enemigo (si hay) puede matarlo, es decir, que no haya
        piezas enemigas que lo defiendan
    """

    def __init__(self) -> None:
        """
        Inicializa una instacia de la clase Tablero
        """

        self.tablero : list[list["Casilla"]]= [[Casilla(i,j) for i in range(8)] for j in range(8)]
        self.enroque : Union[list[bool],None] = None
        self.en_passant : Union[tuple[str,tuple[int,int]],None] = None
        self.contador : int = 0
        self.jugadas : int = 0
        self.turno : int = 1 #Representa el color que tiene el turno (por defecto es el blanco)

    @classmethod
    def creacion_con_FEN(cls, fen : str) -> Self:
        """
        Perimte inicializar la clase Tablero de otra manera pasándole la información en formato FEN

        Parametros:
        -----------
        fen : str
            string que contiene toda la información necesario para el tablero

        Retorna:
        -------
        Self
            Devuelve una nueva instancia de la case Tablero
        """
        from Partidas.aflabeto_FEN import traduccion_posicion

        self = cls()

        self.tablero = [[Casilla(i,j) for i in range(8)] for j in range(8)]

        fen = fen.split()
        filas = fen[0].split('/')

        for i,fila in enumerate(filas):
            j = 0

            for letra in fila:
                if letra.isdigit():
                    j += int(letra)
                    continue

                self[i][j].tranformacion_a_pieza(i, j, letra)
                j += 1


        self.turno = 0 if fen[1] == 'w' else 1
        if fen[2] == '':
            self.enroque = None
        else:
            self.enroque = [True if 'KQ' in fen[2] else False, True if 'kq' in fen[2] else False] if fen[2] else None

        if fen[3] == '-':
            self.en_passant = None
        else:
            self.en_passant = (fen[3],traduccion_posicion(fen[3]))

        self.contador = int(fen[5])

        return self


    def __getitem__(self, indice : int) -> Union[list["Casilla"],"Casilla"]:
        """
        Metodo especial para poder acceder a un elemento de la matriz
        solamente con la variable de la clase Tablero.
        En resumen -> tablero.tablero[i][j] es igual a tablero[i][j]

        Parametros:
        -----------
        indice : int
            Es el índice que nos ayuda a seleccionar las casillas.

        Retorna:
        --------
        Union[list["Casilla"],"Casilla"]
            Retorna la casilla (o las casillas) que ha sido seleccionado
        """
        return self.tablero[indice]

    def __str__(self) -> str:
        """
        Método dunder que representa el tablero desde la persepctiva del jugador que tiene el turn
        """

        color: int = self.turno
        filas = ['  '.join(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'])]

        for i in range(8):
            fila = []
            for j in range(8):
                fila.append(str(self.obtener_casilla(i, j, color)))
                fila.append(f'  {8 - i}' if j == 7 else '')
            filas.append(' '.join(fila))

        return '\n'.join(filas)

    def esta_en_jaque(self, jugador:"Jugador",enemigo:"Jugador") -> bool:
        """
        Verifica si el rey del jugador está en jaque después de un movimiento.

        Parámetros:
        -----------
        jugador : "Jugador"
            A que jugador se quiere saber si esta en jaque o no

        Retorna:
        --------
        bool
            Devuelve True si el rey está en jaque, False si no lo está.
        """
    
        posicion_rey = jugador.encontrar_rey()

        for pieza in enemigo.piezas:
            if (posicion_rey in pieza.movimiento_valido(self) and type(pieza).__name__ != "Peon") or (type(pieza).__name__ == "Peon" and posicion_rey in pieza.movimiento_valido(self) ):
                return True

        return False

    def guardar_estado(self) -> dict:
        """
        Guarda el estado actual del tablero y los datos relevantes para
        poder restaurarlos más adelante. Este método es útil, por ejemplo,
        al implementar deshacer movimientos o para evaluaciones de IA.

        Retorna:
        --------
        dict
            Diccionario que contiene el estado del tablero, los derechos de enroque,
            la casilla de en passant, el contador de medio movimiento y el turno actual.
        """

        estado = {
            "tablero": [[casilla.pieza for casilla in fila] for fila in self.tablero], 
            "enroque": self.enroque.copy() if self.enroque else None,
            "en_passant": self.en_passant,
            "contador": self.contador,
            "turno": self.turno,
        }
        return estado


    def restaurar_estado(self, estado: dict) -> None:
        """
        Restaura el estado del tablero y de la partida a partir de un diccionario previamente
        guardado. Ideal para funciones como deshacer movimiento, análisis o carga de partidas.

        Parámetros:
        -----------
        estado : dict
            Diccionario que contiene el estado del juego, tal como fue devuelto por guardar_estado.

        Retorna:
        --------
        None
            No retorna ningún valor. Modifica el estado interno del objeto.
        """

        for i in range(8):
            for j in range(8):
                self.tablero[i][j].pieza = estado["tablero"][i][j]

        self.enroque = estado["enroque"].copy() if estado["enroque"] else None
        self.en_passant = estado["en_passant"]
        self.contador = estado["contador"]
        self.turno = estado["turno"]

    def obtener_casilla(self, fila : int, columna : int, color : int) -> Casilla:
        """
        Permite encontrar la casilla concreta. La diferencia se encuentra en que,
        como las matrices comienzan arriba a la izquierda y el tablero de ajedrez
        comienza abajo a la izquierda, nuestra matriz está invertida. Para solucionarlo,
        dentro del codigo se tratará como una matriz normal, pero a la hora de mostrarlo
        al usuario, invertimos las filas y las columnas para que sea acorde a su perspectiva.

        Parametros:
        -----------
        fila : int
            Fila en la que se encuentra la casilla

        columna : int
            Columna en la que se encuentra la casilla

        Retorna:
        --------
        Casilla
            Retorna la casilla correspondiente
        """

        return self.tablero[fila][columna] if color else self.tablero[7-fila][7-columna]

    @staticmethod
    def limite(fila : int, columna : int) -> bool:
        """
        Comprueba si la posición (fila,columna) está dentro de los límites del tablero

        Parametros:
        -----------
        fila : int
            Fila en la que se encuentra la casilla

        columna : int
            Columna en la que se encuentra la casilla

        Retorna:
        --------
        bool
            Si es False es porque está fuera de los límites.
        """

        if 8 > fila >= 0 and 8 > columna >= 0:
            return True

        return False

    def mostrar_tablero(self, color : int) -> None:
        """
        Muestra el tablero por consola desde la perspeciva del color del jugador, es decir,
        las piezas situadas abajo son las del color pasada por parámetro

        Parametros:
        -----------
        color : int
            Representa el color del jugador para mostrar el tablero desde su perspectiva
        """

        for i in range(8):
            for j in range(8):
                print(str(self.obtener_casilla(i, j, color)), end=' ')
            print()

        return None

    def traduccion_FEN(self, turno : int) -> str:
        """
        Traduce la situación del tablero a formato FEN. Muy útil a la hora de guardar partidas,
        tratar con APIs de IA, comprimir la información del ajedrez, etc.

        Parametros:
        -----------
        turno : int
            Representa el turno de la partida. Útil para ordenar los eventos de una partida dentro de una BD

        Retorna:
        --------
        str
            Devuelve el formato FEN del tablero.
        """

        fen : str = ''

        for i in range(8):
            espacio = 0
            for j in range(8):

                if str(self[i][j]) != '.':
                    fen += str(espacio) if espacio != 0 else ''
                    fen += str(self[i][j])
                    espacio = 0
                    continue

                espacio += 1

            fen += str(espacio) if espacio != 0 else ''
            fen += '/' if i != 7 else ''

        fen += ' w ' if self.turno else ' b '

        enroque : str = ''

        enroque += 'KQ' if self.enroque[0] else ''
        enroque += 'kq' if self.enroque[1] else ''

        fen += enroque if enroque != '' else '-'

        fen += ' - ' if self.en_passant is None else f' {self.en_passant[0]} '

        fen +=  '0 ' #Va a ser siempre cero ya que no me ha dado tiempo a impliementar casos especiales
        fen += str(turno)

        return fen


    def casillas_intermedias(self, fila : int, columna : int, fila_m : int, columna_m : int) -> list[(int, int)]:
        """
        Metodo estático que calcula las casillas intermedias entre dos piezas (incluyendo la posicion
        de la pieza atacante)

        Parametros:
        -----------
        fila : int
            Fila en la que se encuentra la casilla o pieza 'víctima'

        columna : int
            Columna en la que se encuentra la casilla o pieza 'víctima'

        fila_m : int
            Fila en la que se encuentra la casilla o pieza 'agresor'

        columna_m : int
            Columna en la que se encuentra la casilla o pieza 'agresor'

        Retorna:
        --------
        list[(int,int)]
            Devuelve la lista de posiciones intermedias entre dos puntos, incluyendo la posicion
            de la pieza agresor (fila_m,columna_m)
        """
        dir_i = 1 if fila > fila_m else (-1 if fila < fila_m else 0)
        dir_j = 1 if columna > columna_m else (-1 if columna < columna_m else 0)

        if abs(fila - fila_m) != abs(columna - columna_m) and fila - fila_m != 0 and columna - columna_m != 0:
            return []

        generador = ((fila_m + landa * dir_i, columna_m + landa * dir_j) for landa in itertools.count(1))

        intermedias : list = []
        intermedias.append((fila_m,columna_m))
        for pos in generador:
            if pos == (fila,columna) or not self.limite(*pos):
                break
            intermedias.append((pos[0],pos[1]))

        return intermedias

    @staticmethod
    def quitar_permutaciones(mov : tuple, casillas_tocapelotas : list) -> list[(int,int)]:
        """
        Elimina las casillas peligrosas para la pieza 'victima' mediante la irrupción
        del camino por parte de otra pieza.

        Parametros:
        -----------
        mov : tuple
            Tupla que contiene la posicion de la pieza que iterrume en medio del camino

        casillas_tocapelotas : list
            Son el conjunto de casillas que representan los caminos que atacan a la pieza 'victima'.
            Puede haber más de un camíno

        Retorna:
        --------
        list[(int,int)]
            Devuelve la lista de posiciones intermedias entre dos puntos, incluyendo la posicion
            de la pieza agresor (fila_m,columna_m)
        """

        casillas_tocapelotas = [pos for pos in casillas_tocapelotas if mov not in pos]

        return casillas_tocapelotas


    def jaque_in(self, fila : int, columna : int, jugador : "Jugador", enemigo : "Jugador") -> bool:
        """
        Comprueba si el jaque producido es inevitable o no

        Parametros:
        -----------
        fila : int
            Fila en la que se encuentra la casilla o pieza 'víctima'

        columna : int
            Columna en la que se encuentra la casilla o pieza 'víctima'

        jugador : "Jugador"
            Representa el jugador que es dueño de la pieza 'vicitma'

        enemigo : "Jugador"
            Representa el jugador que ataca la pieza 'victima' con una o más piezas

        Retorna:
        --------
        bool
            Devuelve True si es inevitable y False si se puede evitar
        """

        amenazadores : list = self.amenazas(enemigo,fila,columna)

        casillas_tocapelotas : list = self.casillas_amenazadas(amenazadores,fila,columna)

        salir : bool = False
        for pieza in jugador.piezas:
            if pieza.posicion == (fila, columna):
                rey = pieza

            for mov in pieza.movimiento_valido(self):

                if salir:
                    break

                for casillas_intermedias in casillas_tocapelotas:

                    if salir:
                        break

                    if mov in casillas_intermedias:
                        casillas_tocapelotas = self.quitar_permutaciones(mov,casillas_tocapelotas)
                        salir = True

        if rey.movimiento_valido(self):
            return False

        if not casillas_tocapelotas:
            return False

        return True

    def amenazas(self, enemigo : "Jugador", fila : int, columna : int) -> list:
        """
        Obtiene todas las piezas que amenazan una casilla junto con su posición

        Parametros:
        -----------
        enemigo : "Jugador"
            Representa el jugador que ataca la pieza 'victima' con una o más piezas

        fila : int
            Fila en la que se encuentra la casilla o pieza 'víctima'

        columna : int
            Columna en la que se encuentra la casilla o pieza 'víctima'

        Retorna:
        --------
        list
            Devuelve una lista con la posición de la pieza y la pieza en sí
        """
        from Piezas import Rey

        casillas : list = []

        for pieza in enemigo.piezas:
            if isinstance(pieza, Rey):
                continue

            if (fila,columna) in pieza.movimiento_valido(self):
                if not (columna == pieza.posicion[1] and str(pieza).upper() == 'P'):
                    casillas.append((pieza.posicion, pieza))
        return casillas

    def casillas_amenazadas(self, amenazadores : list, fila : int, columna : int) -> list:
        """
        Obtiene todas las casillas amenazadas entre la posición de cada pieza amenazadora
        y la posición de la pieza víctima

        Parametros:
        -----------
        amenazadores : list
            Lista de posiciones de cada pieza que amenaza a la pieza víctima

        fila : int
            Fila en la que se encuentra la casilla o pieza 'víctima'

        columna : int
            Columna en la que se encuentra la casilla o pieza 'víctima'

        Retorna:
        --------
        list
            Devuelve una lista con la posición de la pieza y la pieza en sí
        """

        casillas : list = []

        for posicion, pieza in amenazadores:

            fila_p, columna_p = posicion

            if str(self[fila_p][columna_p]) not in ['N','n']:
                casillas.append(self.casillas_intermedias(fila, columna, posicion[0], posicion[1]))

            elif str(self[fila_p][columna_p]) in ['N','n']:
                casillas.append(posicion)

        return casillas

    def posibilidad_matar_con_rey(self, enemigo : "Jugador", fila : int, columna : int, rey : "Rey") -> bool:
        """
        Comprueba si la casilla a la que se puede mover el rey para matar una pieza del enemigo es realmente posible.
        Para ello simula que se mueve a dicha posición y se comprueba si alguna pieza la puede atacar.

        Parametros:
        -----------
        enemigo : list
            Jugador enemigo que va a sufrir del poder del rey Ö

        fila : int
            Fila en la que se encuentra el rey

        columna : int
            Columna en la que se encuentra el rey

        Retorna:
        --------
        bool
            Devuelve si puede matar a dicha pieza.
        """

        pieza_aux : Optional["Pieza"] = self[fila][columna].pieza
        if pieza_aux is None:
            return True

        indice : int = enemigo.piezas.index(pieza_aux)
        enemigo.piezas.remove(pieza_aux)

        self[fila][columna].pieza = rey

        pos_aux_rey = rey.posicion
        rey.posicion = (fila,columna)

        if not self.amenazas(enemigo, fila, columna):
            self[fila][columna].pieza = pieza_aux
            rey.posicion = pos_aux_rey
            enemigo.piezas.insert(indice,pieza_aux)
            return True

        else:
            self[fila][columna].pieza = pieza_aux
            rey.posicion = pos_aux_rey
            enemigo.piezas.insert(indice,pieza_aux)
            return False