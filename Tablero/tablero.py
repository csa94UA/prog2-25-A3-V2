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
    turno : int
        Marca el número de turno de la partida

    Métodos:
    -----------
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
    traduccion_FEN(self, color : int, enroque_n : int, enroque_b : int, en_passant : Union[str,None], contador : int, turno : int) -> str:
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
    """

    def __init__(self) -> None:
        """
        Inicializa una instacia de la clase Casilla
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
        index : int
            Es el índice que nos ayuda a seleccionar las casillas.

        Retorna:
        --------
        Casilla
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
        color : bool
            Representa el turno del jugador. Si es 1 entonces es el blanco y si es 0 entonces es el negro

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
        print(f"Amenazas para {self[fila][columna].pieza}: ", casillas)
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
        print("Pieza que se podría matar: ",pieza_aux)
        if pieza_aux is None:
            print("No era una pieza")
            return True

        indice : int = enemigo.piezas.index(pieza_aux)
        enemigo.piezas.remove(pieza_aux)

        self[fila][columna].pieza = rey
        print("El rey que va a matar: ",rey)

        pos_aux_rey = rey.posicion
        rey.posicion = (fila,columna)

        print(f"Nueva posición del rey (definida en su atributo): {rey.posicion}")

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


    def imagenes_piezas(self, tamano_casilla):
        """
        Carga y ajusta las imágenes de las piezas del ajedrez desde la carpeta 'imagenes', donde se encuentran los archivos png.

        Parametros:
        -----------
        tamano_casilla : int
            El tamaño de cada casilla del tablero, que se usa para ajustar el tamaño de las imágenes de las piezas.

        Retorna:
        --------
        dict
            Devuelve un diccionario con las imágenes de las piezas.
        """
        piezas = {}
        nombres_piezas = {"r", "n", "b", "q", "k", "p", "R", "N", "B", "Q", "K", "P"}
        carpeta = os.path.join(os.path.dirname(__file__),  "imagenes")

        for nombre in nombres_piezas:
            if nombre.isupper():
                archivo = f"b{nombre.upper()}.png"
                
            else:
                archivo = f"{nombre}.png"
            ruta_imagen = os.path.join(carpeta, archivo)
            imagen = pygame.image.load(ruta_imagen)
            imagen = pygame.transform.scale(imagen, (tamano_casilla, tamano_casilla))
            piezas[nombre] = imagen
        return piezas

    def crear_tablero(self):
        """
        Crea un tablero de ajedrez representado como una lista de listas (matriz).

        Retorna:
        --------
        list
            Devuelve una lista de 8x8 que representa el tablero de ajedrez con las piezas colocadas en su
            posición inicial.
        """
        tablero = [["" for _ in range(8)] for _ in range(8)]

        piezas_negras = ["r", "n", "b", "q", "k", "b", "n", "r"]
        piezas_blancas = ["R", "N", "B", "Q", "K", "B", "N", "R"]
        for i in range(8):
            tablero[0][i] = piezas_negras[i]
            tablero[7][i] = piezas_blancas[i]
            tablero[1][i] = "p"
            tablero[6][i] = "P"
        return tablero

    def dibujar_tablero(self, ventana, filas, columnas, tamano_casilla, color_claro, color_oscuro):
        """
        Dibuja el tablero de ajedrez en la ventana de pygame.

        Parametros:
        -----------
        ventana :
            La ventana de pygame donde se dibujará el tablero.
        filas : int
            Número de filas del tablero.
        columnas : int
            Número de columnas del tablero.
        tamano_casilla : int
            El tamaño de cada casilla del tablero.
        color_claro : tuple
            El color de los cuadrados claros del tablero.
        color_oscuro : tuple
            El color de los cuadrados oscuros del tablero.
        """
        for fila in range(filas):
            for columna in range(columnas):
                if (fila + columna) % 2 == 0:
                    color = color_claro
                else:
                    color = color_oscuro
                pygame.draw.rect(ventana, color, (columna * tamano_casilla + 30, fila * tamano_casilla, tamano_casilla, tamano_casilla))

    def dibujar_piezas(self, ventana, piezas, tamano_casilla):
        """
        Coloca las piezas del ajedrez en el tablero.

        Parametros:
        -----------
        ventana :
            La ventana de pygame donde se dibujarán las piezas.
        tablero : list
            El tablero de ajedrez que contiene las posiciones de las piezas.
        piezas : dict
            El diccionario donde se han guardado anteriormente las piezas.
        tamano_casilla : int
            El tamaño de cada casilla en el tablero.
        """
        cambio = {
            "Peon": "p",
            "Torre": "r",
            "Caballo": "n",
            "Alfil": "b",
            "Reina": "q",
            "Rey": "k",
        }

        for fila in range(8):
            for columna in range(8):
                pieza = self.tablero[fila][columna].pieza
                if pieza:
                    x = columna * tamano_casilla + 30
                    y = fila * tamano_casilla
                    letra = cambio[type(pieza).__name__]
                    if pieza.color:
                        ventana.blit(piezas[letra.upper()], (x, y))
                    else:
                        ventana.blit(piezas[letra.lower()], (x, y))

    def dibujar_coordenadas(self, ventana, tamano_casilla, color_texto=(255, 255, 255)):
        """
        Dibuja las coordenadas del tablero (a-h y 1-8) en los bordes del tablero.

        Parametros:
        -----------
        ventana : Surface
            La ventana de pygame donde se dibujarán las coordenadas.
        tamano_casilla : int
            El tamaño de cada casilla en el tablero.
        color_texto : tuple
            El color del texto para las coordenadas.
        """
        fuente = pygame.font.SysFont(None, tamano_casilla // 3)
        letras = "abcdefgh"
        numeros = "87654321"  # Para que 1 esté en la parte inferior

        for i in range(8):
            # Letras (abajo)
            letra = fuente.render(letras[i], True, color_texto)
            x = i * tamano_casilla + tamano_casilla // 2 - letra.get_width() // 2 + 30
            y = 8 * tamano_casilla + 5  # justo debajo del tablero
            ventana.blit(letra, (x, y))

            # Números (izquierda)
            numero = fuente.render(numeros[i], True, color_texto)
            x = 5  # margen izquierdo
            y = i * tamano_casilla + tamano_casilla // 2 - numero.get_height() // 2
            ventana.blit(numero, (x, y))


    def representacion_grafica(self):
        """
        Inicia pygame y crea una ventana gráfica para mostrar el tablero con las piezas.

        Esta función también gestiona el bucle principal de la interfaz gráfica donde se dibujan el tablero y las piezas.
        """
        pygame.init()
        ancho, alto = 600, 600
        filas, columnas = 8, 8
        tamano_casilla = ancho // columnas
        color_claro = (238, 238, 210)
        color_oscuro = (118, 150, 86)
        clock = pygame.time.Clock()

        piezas = self.imagenes_piezas(tamano_casilla)
        ventana = pygame.display.set_mode((ancho + 30, alto + 30))

        inicio = True
        while inicio:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    inicio = False

            ventana.fill((0, 0, 0))
            self.dibujar_tablero(ventana, filas, columnas, tamano_casilla, color_claro, color_oscuro)
            self.dibujar_coordenadas(ventana, tamano_casilla)
            self.dibujar_piezas(ventana, piezas, tamano_casilla)
            pygame.display.flip()
            clock.tick(60)
        pygame.quit()

    def iniciar_grafica(self):
        """
        Inicia Pygame y crea la ventana gráfica para mostrar el tablero con las piezas.
        Lanza el bucle gráfico en un hilo.
        """
        pygame.init()
        self.ancho, self.alto = 600, 600
        self.tamano_casilla = self.ancho // 8
        self.color_claro = (238, 238, 210)
        self.color_oscuro = (118, 150, 86)
        self.clock = pygame.time.Clock()
        self.piezas_graficas = self.imagenes_piezas(self.tamano_casilla)
        self.ventana = pygame.display.set_mode((self.ancho + 30, self.alto + 30))
        self.ventana_activa = True

        # Inicia el hilo gráfico
        threading.Thread(target=self.bucle_grafico, daemon=True).start()

    def bucle_grafico(self):
        """
        Bucle infinito que mantiene actualizada la ventana gráfica.
        Corre en un hilo separado.
        """
        while self.ventana_activa:
            self.actualizar_grafica()

    def actualizar_grafica(self):
        """
        Actualiza la ventana del tablero con las piezas, coordenadas y el estado del juego.
        """
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.ventana_activa = False
                pygame.quit()
                sys.exit()

        self.ventana.fill((0, 0, 0))  # Limpiar la pantalla
        self.dibujar_tablero(self.ventana, 8, 8, self.tamano_casilla, self.color_claro, self.color_oscuro)
        self.dibujar_coordenadas(self.ventana, self.tamano_casilla)
        self.dibujar_piezas(self.ventana, self.piezas_graficas, self.tamano_casilla)
        pygame.display.flip()
        self.clock.tick(60)

if __name__ == "__main__":
    tablero = Tablero()
    print(tablero)
    print(tablero.traduccion_FEN(1,1,1,None,0,1))
    tablero.representacion_grafica()