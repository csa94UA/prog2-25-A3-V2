"""
Modulo para la gestión y uso de una pieza genérica

Este módulo define la clase abstracta 'Pieza' que representa una pieza de ajedrez genérica
y contiene la información más esencial. Posee modulos que permite realizar las funciones básicas.

Clases:
    - Tablero
"""

from .casilla import Casilla
from Jugador import Jugador
from typing import Union
import itertools
#import pygame
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
    turno : int
        Marca el número de turno de la partida

    Métodos:
    -----------
    obtener_casilla(self, fila : int, columna : int) -> Casilla:
        Devuelve la casilla coherente a la perspectiva del jugador actual
    limite(fila : int, columna : int) -> bool:
        Comprueba si se ha digitado una posicion fuera de los limites
    mostrar_tablero(self, color : bool) -> None:
        Representa el tablero en función de la persepctiva del jugador actual
    traduccion_FEN(self, color : int, enroque_n : int, enroque_b : int, en_passant : Union[str,None], contador : int, turno : int) -> str:
        Devuelve toda la información del tablero en formato FEN. Util para guardar partidas y comunicarse con otras IA
    casillas_intermedias(fila : int, columna : int, fila_m : int, columna_m : int) -> list[(int, int)]:
        Retorna las casillas intermedias entre dos piezas. Usado para comprobar las casillas problematicas dentro de un jaque
    quitar_permutaciones(self, mov : tuple, casillas_tocapelotas : list, fila : int, columna : int) -> None:
        Elimina las permutaciones que contengan a la posicoin de la pieza. Se usa para eliminar casillas intermedias
    jaque_in(self, fila : int, columna : int, jugador : Jugador, enemigo : Jugador) -> bool:
        Comprueba si el jaque es inevitable o no
    amenazas(self, enemigo : Jugador, fila : int, columna : int) -> list:
        Revisa las piezas que amenazan una casilla
    casillas_amenazadas(self, amenazadores : list, fila : int, columna : int) -> list:
        Obtiene todas las casillas amenazadas entre la posición de cada pieza amenazadora y la posición de la pieza
        víctima. En ella se emplea la funcion casillas_intermedias (por eso su similitud), pero este tiene en cuenta
        el caso especial del caballo (que no tiene casillas intermedias)
    """

    def __init__(self) -> None:
        """
        Inicializa una instacia de la clase Casilla
        """

        self.tablero : list[list["Casilla"]]= [[Casilla(i,j) for i in range(8)] for j in range(8)]
        self.enroque : Union[list[bool,bool],None] = None
        self.en_passant : Union[tuple[str,int],None] = None
        self.contador : int = 0
        self.jugadas : int = 0
        self.turno : int = 1 #Representa el color que tiene el turno (por defecto es el blanco)


    def __getitem__(self, indice : int):
        """
        Metodo especial para poder acceder a un elemento de la matriz
        solamente con la variable de la clase Tablero.
        En resumen -> tablero.tablero[i][j] es igual a tablero[i][j]

        Parametros:
        -----------
        index : int
            Es el índice que nos ayuda a seleccionar las casillas.

        Retorna:
        --------
        Casilla
            Retorna la casilla (o las casillas) que ha sido seleccionado
        """
        return self.tablero[indice]

    def obtener_casilla(self, fila : int, columna : int, color : int) -> Casilla:
        """
        Permite encontrar la casilla concreta. La diferencia se encuentra en que,
        como las matrices comienzan arriba a la izquierda y el tablero de ajedrez
        comienza abajo a la izquierda, nuestra matriz está invertida. Para solucionarlo,
        dentro del codigo se tratará como una matriz normal, pero a la hora de mostrarlo
        al usuario, invertimos las filas para que sea acorde a su perspectiva.

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

        return self.tablero[fila][columna] if color else self.tablero[7-fila][columna]

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

    def mostrar_tablero(self, color : bool) -> None:
        """
        Muestra el tablero por consola desde la perspeciva del color del jugador, es decir,
        las piezas situadas abajo son las del color pasada por parámetro

        Parametros:
        -----------
        color : bool
            Representa el color del jugador para mostrar el tablero desde su perspectiva
        """

        for i in range(8):
            for j in range(8):
                #print(self[abs(fila-i)][j].representacion(),end=" ")
                print(self.obtener_casilla(i, j, color).representacion(), end=' ')
            print()

        return None

    def traduccion_FEN(self, color : int, enroque_n : int, enroque_b : int, en_passant : Union[str,None], contador : int, turno : int) -> str:
        """
        Traduce la situación del tablero a formato FEN. Muy útil a la hora de guardar partidas,
        tratar con APIs de IA, comprimir la información del ajedrez, etc.

        Parametros:
        -----------
        color : bool
            Representa el turno del jugador. Si es 1 entonces es el blanco y si es 0 entonces es el negro
        enroque_n : bool
            Representa la posibilidad del jugador negro en hacer enroque
        enroque_b : bool
            Representa la posibilidad del jugador blanco en hacer enroque
        en_passant : str
            Muestra en que casilla (representado con coordenadas de ajedrez) se puede capturar al paso.
            Este valor cambia en cada turno, por lo que no tiene dependencia del color.
        contador : int
            Cuenta la cantidad de semimovimientos realizados. Los semimovimientos son aquellos donde
            no se han capturado ni movido peones. Si el valor llega a 50, se proclama tablas (empate).
            Este valor se reanuda a 0 cuando se pierde la racha (creo).
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

                if self[i][j].representacion() != ' ':
                    fen += str(espacio) if espacio != 0 else ''
                    fen += self[i][j].representacion()
                    espacio = 0
                    continue

                espacio += 1

            fen += str(espacio) if espacio != 0 else ''
            fen += '/' if i != 7 else ''

        fen += ' w ' if color else ' b '

        fen += 'KQ' if enroque_b else ''
        fen += 'kq' if enroque_n else ''

        fen += f' {en_passant[0]} ' if en_passant is not None else ' - '

        fen += str(contador) + ' '
        fen += str(turno)

        return fen

    @staticmethod
    def casillas_intermedias(fila : int, columna : int, fila_m : int, columna_m : int) -> list[(int, int)]:
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

        dir_i = 1 if fila > fila_m else -1
        dir_j = 1 if columna > columna_m else -1

        if (fila - fila_m != 0 and abs(fila - fila_m) != abs(columna - columna_m)) and (fila - fila_m == 0):
            return []

        generador = ((fila_m + landa * dir_i, columna_m + landa * dir_j) for landa in itertools.count(1))

        intermedias = [(fila_m,columna_m)]
        for pos in generador:
            if pos == (fila,columna):
                break
            intermedias.append((fila,columna))

        return intermedias


    def quitar_permutaciones(self, mov : tuple, casillas_tocapelotas : list, fila : int, columna : int) -> None:
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
        fila : int
            Fila en la que se encuentra la casilla o pieza 'víctima'
        columna : int
            Columna en la que se encuentra la casilla o pieza 'víctima'

        Retorna:
        --------
        list[(int,int)]
            Devuelve la lista de posiciones intermedias entre dos puntos, incluyendo la posicion
            de la pieza agresor (fila_m,columna_m)
        """

        #fila_p, columna_p = mov

        #Posiblemente este código sea redundante porque el simple hecho de estar en medio de un
        #camino te hace pertenecer al subconjunto de ese camino

        #caminos_a_eliminar = self.casillas_intermedias(fila,columna,fila_p,columna_p)

        casillas_tocapelotas[:] = [pos for pos in casillas_tocapelotas if mov not in pos]

        return None


    def jaque_in(self, fila : int, columna : int, jugador : Jugador, enemigo : Jugador) -> bool:
        """
        Comprueba si el jaque producido es inevitable o no

        Parametros:
        -----------
        fila : int
            Fila en la que se encuentra la casilla o pieza 'víctima'
        columna : int
            Columna en la que se encuentra la casilla o pieza 'víctima'
        jugador : Jugador
            Representa el jugador que es dueño de la pieza 'vicitma'
        enemigo : Jugador
            Representa el jugador que ataca la pieza 'victima' con una o más piezas

        Retorna:
        --------
        bool
            Devuelve True si es inevitable y False si se puede evitar
        """

        amenazadores : list = self.amenazas(enemigo,fila,columna)

        casillas_tocapelotas : list = self.casillas_amenazadas(amenazadores,fila,columna)

        for pieza in jugador.piezas:

            fila, columna = pieza.posicion

            for mov in pieza.movimiento_valido(self):

                if mov in casillas_tocapelotas:
                    self.quitar_permutaciones(mov,casillas_tocapelotas,fila,columna)

        if casillas_tocapelotas is []:
            return False

        return True

    def amenazas(self, enemigo : Jugador, fila : int, columna : int) -> list:
        """
        Obtiene todas las piezas que amenazan una casilla junto con su posición

        Parametros:
        -----------
        enemigo : Jugador
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

        casillas : list = []

        for pieza in enemigo.piezas:
            if (fila,columna) in pieza.movimiento_valido(self):
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

            if tablero[fila_p][columna_p].representacion() != 'Nn':
                casillas.append(self.casillas_intermedias(fila, columna, posicion[0], posicion[1]))

            elif tablero[fila_p][columna_p].representacion() == 'Nn':
                casillas.append(posicion)

        return casillas

    def imagenes_piezas(self, tamano_casilla):
        piezas = {}
        nombres_piezas = {"r", "n", "b", "q", "k", "p", "R", "N", "B", "Q", "K", "P"}
        for nombre in nombres_piezas:
            pieza = pygame.image.load(os.path.join("..", "piezas", f"{nombre}.png"))
            pieza = pygame.transform.scale(pieza, (tamano_casilla, tamano_casilla))
        return piezas

    def crear_tablero(self):
        tablero = []
        for i in range(8):
            fila = []
            for j in range(8):
                fila.append("")
            tablero.append(fila)

        piezas_negras = ["r", "n", "b", "q", "k", "b", "n", "r"]
        piezas_blancas = ["R", "N", "B", "Q", "K", "B", "N", "R"]
        for i in range(8):
            tablero[0][i] = piezas_negras[i]
            tablero[7][i] = piezas_blancas[i]
            tablero[1][i] = "p"
            tablero[6][i] = "P"
        return tablero

    def dibujar_tablero(self, ventana, filas, columnas, tamano_casilla, color_claro, color_oscuro, color_texto):
        for fila in range(filas):
            for columna in range(columnas):
                if (fila + columna) % 2 == 0:
                    color = color_claro
                else:
                    color = color_oscuro

                pygame.draw.rect(ventana, color,
                                 (columna * tamano_casilla, fila * tamano_casilla, tamano_casilla, tamano_casilla))
                columna_letra = chr(65 + columna)
                fila_numero = filas - fila
                coordenada = columna_letra + str(fila_numero)
                fuente = pygame.font.SysFont(None, 24)
                texto = fuente.render(coordenada, True, color_texto)
                ventana.blit(texto, (columna * tamano_casilla + 5, fila * tamano_casilla + 5))

    def dibujar_piezas(self, ventana, tablero, piezas, tamano_casilla):
        for fila in range(8):
            for columna in range(8):
                pieza = tablero[fila][columna]
                if pieza in piezas:
                    x = columna * tamano_casilla
                    y = fila * tamano_casilla
                    ventana.blit(piezas[pieza], (x, y))

    def representacion_grafica(self):
        pygame.init()
        ancho, alto = 600, 600
        filas, columnas = 8, 8
        tamano_casilla = ancho // columnas
        color_claro = (238, 238, 210)
        color_oscuro = (118, 150, 86)
        color_texto = (255, 0, 0)

        piezas = self.imagenes_piezas(tamano_casilla)
        tablero = self.crear_tablero()
        ventana = pygame.display.set_mode((ancho, alto))

        inicio = True
        while inicio:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    inicio = False

            ventana.fill((0, 0, 0))
            self.dibujar_tablero(ventana, filas, columnas, tamano_casilla, color_claro, color_oscuro, color_texto)
            self.dibujar_piezas(ventana, tablero, piezas, tamano_casilla)
            pygame.display.flip()

        pygame.quit()


if __name__ == "__main__":
    tablero = Tablero()
    tablero.mostrar_tablero(0)
    print(tablero.traduccion_FEN(1,1,1,None,0,1))