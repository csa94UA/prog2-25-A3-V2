"""
Modulo para la ejecucion de una partida, ya sea JcJ, JcE o EcE.

Este modulo proporciona funciones para el intercambio de turnos, manejo de excepciones e
inicialización de la partida.

Funciones:
    - partida(jugador1 : Jugador, jugador2 : Jugador) -> Jugador:
    Simula la partida y determina el ganador. Es la funcion nucleo de todo el programa.

    - crear_piezas(color : bool, tablero : Tablero) -> list[Pieza]:
    Inicializa el tablero y las fichas de cada jugador.

    - encontrar_pieza(tablero : "Tablero", jugador : "Jugador", origen : tuple[int]) -> Union["Pieza",None]:
    Busca la pieza digitada dentro de del conjunto de piezas del jugador. Si lo encuentra devuelve dicha pieza.

    - comprobar_enroque_corto(tablero : "Tablero", enemigo : "Jugador", rey : "Rey", torre : "Torre") -> bool:
    En caso de digitar un enroque corto comprueba si es posible.

    - comprobar_enroque_largo(tablero : "Tablero", enemigo : "Jugador", rey : "Rey", torre : "Torre") -> bool:
    Igual que con el enroque corto solo que para el caso de enroque largo.

    - comprobar_promocion(pieza : "Peon", promocion : Union[str,int], jugador_actual : "Jugador") -> bool:
    Comprueba si la promocion es valido. En caso afirmativo se intercambia el peon por la pieza deseada (dentro de
    las permitidas).

    - comprobar_jaque_enemigo(tablero : "Tablero", jugador_actual : "Jugador", enemigo : "Jugador", pieza : Union["Pieza",None]) -> bool:
    Comprueba si el movimiento que hemos realizado provoca un jaque al rey enemigo.

    - caso_jaque(tablero : "Tablero", jugador_actual : "Jugador", enemigo : "Jugador", movimiento : tuple) -> bool:
    Determina si tu movimiento evita el jaque. Solo se activa cuando se ejecuta el caso especial de jaque.

    - comprobar_tablas(tablero : "Tablero", jugador_actual : "Jugador", enemigo : "Jugador") -> bool:
    Comprueba si se ha producido un empate (por el momento solo devuelve True si solo hay en el tablero los reyes).
"""
import random
from wsgiref.util import request_uri

from Piezas import Caballo, Alfil, Rey, Reina, Peon, Torre, Pieza
from Piezas.error_creacion_pieza import ErrorCrearPieza
from Partidas.error_partidas import ErrorPartida
from Jugador import Jugador
from random import randint
from typing import Union, Any
from Partidas.aflabeto_FEN import digitar_movimiento, transformacion_a_LAN_hipersimplificado, traduccion_inversa, \
    traducir_movimiento_ia, traduccion_posicion
from Tablero import Tablero
from app import movimiento_ia
from stockfish import Stockfish
import time

stockfish = Stockfish(path="./stockeje", depth=10)
stockfish.update_engine_parameters({"MultiPV": 5})

def partida(jugador1 : Jugador, jugador2 : Jugador, bot : bool = False) -> Union["Jugador",None]:
    """
    Es la función principal de este archivo. En ella se trata toda la logica general de una partida de ajedrez (trato de
    turnos, manejo de movimientos especiales, manejo de errores, etc.).

    Parametros:
    -----------
    jugador_1 : Jugador -> Representa el primer jugador

    jugador_2 : Jugador -> Representa el segundo jugador

    Retorna:
    ----------
    Jugador
        Devuelve el jugador que ha ganado. Si hay empate devuelve None.
    """

    # Inicializamos tablero
    tablero = Tablero()

    jaque, turno = inicializacion_partida(jugador1, jugador2, tablero)

    while True:
        # Se inicializa los turnos de cada jugador, siendo enemigo el jugador que no tiene turno.
        jugador_actual : Jugador = jugador1 if turno else jugador2
        enemigo : Jugador = jugador1 if not turno else jugador2

        tablero.turno = jugador_actual.color
        act_en_passant : bool = False

        # Mostramos el tablero
        print(tablero)

        # Se comprueba si son tablas.
        if comprobar_tablas(tablero, jugador_actual, enemigo):
            jugador_actual = None #Nadie gana
            print("Nadie gana")
            break

        print(f"\nTurno de {jugador_actual.nombre}")

        # Pedimos el movimiento del jugador / IA
        if jugador_actual.nombre == "StockFish" and bot:
            movimiento = movimiento_digitado_por_IA(tablero, jugador_actual)
        else:
            movimiento = digitar_movimiento(jugador_actual.color)

        # Si el jugador actual está en jaque se procede a efectuar el caso especial de jaque.
        if jaque:
            intento : bool = caso_jaque(tablero, jugador_actual, enemigo, movimiento)

            # Si no se ha logrado evitar el jaque, se regresa al principio
            if not intento:
                continue

        # Comprobamos si quieren hacer enroque. Si es así se simula y se comprueba su validez
        if type(movimiento[2]) == int and movimiento[2] in [1,2] and not jaque:

            bandera, pieza = comprobar_enroque(movimiento, jugador_actual, enemigo, tablero)

            if not bandera:
                continue

            if jugador_actual.color:
                tablero.enroque[0] = False
            else:
                tablero.enroque[1] = False
            act_en_passant = True

        # Busca la pieza en esa posicion. Si no la encuentra, dará un mensaje de error y repetirá el movimiento
        if not(type(movimiento[2]) == int and movimiento[2] in [1,2]) and not jaque:
            intento, pieza = comprobar_movimiento(movimiento, jugador_actual, enemigo, tablero)

            if not intento:
                continue

        #En caso de que sea un peon y se haya digitado una promoción, debemos comprobar si es válida. En caso afirmativo
        #transformamos ese peon a la pieza deseada

        if str(movimiento[2]).isalpha() and not jaque:

            intento : bool = comprobar_promocion(pieza, movimiento[2], jugador_actual, tablero)

            if not intento:
                print("Error. No se ha podido realizar la promoción")
                continue

        #Vemos si produce la pieza un jaque. En caso afirmativo lo guardamos para el jugador del siguiente turno
        rey = next((rey for rey in enemigo.piezas if isinstance(rey, Rey)), None)
        jaque : bool = comprobar_jaque_enemigo(tablero, jugador_actual, enemigo, pieza)

        # Si está en jaque y resulta que no se puede evitar, entonces se termina la partida.
        if jaque and tablero.jaque_in(rey.posicion[0], rey.posicion[1], enemigo, jugador_actual):
            break

        turno = 1 - turno
        tablero.contador += 1
        print(tablero.traduccion_FEN(tablero.contador))
        if act_en_passant:
            tablero.en_passant = None

    if jugador_actual is not None:
        print(f"Ha ganado el jugador {jugador_actual.nombre}")
        print("Felicidades!!!!!")

    return jugador_actual

def inicializacion_partida(jugador1 : "Jugador", jugador2 : "Jugador", tablero : "Tablero") -> (bool,int):
    """
    Función que inicializa el inicio de una partida.

    Parametros:
    -----------
    jugador1 : Jugador
        Uno de los jugadores.

    jugador2 : Jugador
        Otro de los jugadores.

    tablero : Tablero
        Tablero en sí para inicializar las posiciones de las piezas.

    Retorna:
    ----------
    (bool, int)
        Retorna la inicialización de la variable jaque y el turno del jugador, siendo 1 turno de blancas y 0 el de negras.
    """

    # Establecemos un inicio de turno aleatorio
    if randint(0, 1000) < 499:
        jugador1.color = 1
        jugador2.color = 0
    else:
        jugador2.color = 1
        jugador1.color = 0

    # Insertamos las piezas en el tablero y en el inventario del jugador
    jugador1.piezas = crear_piezas(jugador1.color, tablero, jugador1, jugador2)
    jugador2.piezas = crear_piezas(jugador2.color, tablero, jugador2, jugador1)

    tablero.enroque = [True,True]
    tablero.en_passant = None
    tablero.contador = 0

    return False, 1 if jugador1.color else 0


def crear_piezas(color : int, tablero : Tablero, jugador : "Jugador", enemigo : "Jugador") -> list["Pieza"]:
    """
    Función que inicializa las piezas de un jugador al comenzar una partida. Tiene en cuanta el color del jugador para
    colocar las piezas en su lugar.

    Parametros:
    -----------
    color : int -> Color del jugador a quien se le van a crear las piezas.

    tablero : Tablero -> Tablero en sí para guardar la posición de las piezas creadas.

    Retorna:
    ----------
    list[Pieza]
        Retorna la lista de piezas que se han creado y que se asignaran al jugador correspondiente
    """

    piezas = []

    #Inicializamos primero todos los peones
    fila_p : int = 6 if color else 1
    for j in range(8):
        peon = Peon((fila_p, j), color)
        try:
            if peon in jugador.piezas or peon in enemigo.piezas:
                raise ErrorCrearPieza(peon, "Se ha intentado crear una pieza que ya existe")
            if any(p.posicion == peon.posicion and p != peon for p in jugador.piezas) or \
                    any(p.posicion == peon.posicion for p in enemigo.piezas):
                raise ErrorCrearPieza(peon, "Se ha intentado crear una pieza en una posición previamente ocupada")
        except ErrorCrearPieza as e:
            print(e)
        else:
            piezas.append(peon)
            tablero[fila_p][j].pieza = peon

    #A continuación se inicializan el resto de piezas de manera ordenada.
    fila_r : int = 7 if color else 0
    piezas_ext = [Torre((fila_r,0),color), Caballo((fila_r,1),color), Alfil((fila_r,2),color),
                  Reina((fila_r,3),color), Rey((fila_r,4),color, enemigo),
                  Alfil((fila_r,5),color), Caballo((fila_r,6),color), Torre((fila_r,7),color)]

    #Se va insertando cada una de las piezas en la lista que se devolverá.
    for pieza in piezas_ext:
        try:
            if pieza in jugador.piezas or pieza in enemigo.piezas:
                raise ErrorCrearPieza(pieza, "Se ha intentado crear una pieza que ya existe")
            if any(p.posicion == pieza.posicion and p != pieza for p in jugador.piezas) or \
                    any(p.posicion == pieza.posicion for p in enemigo.piezas):
                raise ErrorCrearPieza(pieza, "Se ha intentado crear una pieza en una posición previamente ocupada")
        except ErrorCrearPieza as e:
            print(e)
        else:
            piezas.append(pieza)
            fila, columna = pieza.posicion
            tablero[fila][columna].pieza = pieza

    return piezas

def encontrar_pieza(jugador : "Jugador", origen : tuple[int]) -> Union["Pieza",None]:
    """
    Busca la pieza en la posicion de origen digitada por el jugador. Para lograrlo recorre toda la lista de piezas del
    jugador hasta dar con aquella cuya posicion coincide con la posicion origen digitada anteriormente.

    Parametros:
    -----------
    tablero : Tablero -> Tablero en sí. Solo está para comprobar si es exactamente esa pieza.

    jugador : Jugador -> Jugador que ha digitado el movimiento.

    origen : tuple[int] -> Es la posicion origen digitada por el jugador.

    Retorna:
    ----------
    Pieza
        Retorna la pieza que coincide su posicion con la posicion origen digitada. Si no se encuentra devuelve None.
    """

    for piezas in jugador.piezas:
            if origen == tuple(piezas.posicion): #Si la posición de origen coincide con el de la pieza.
                return piezas

    return None

def movimiento_digitado_por_IA(tablero : "Tablero", jugador_actual : "Jugador") -> tuple:
    try:
        #lan = movimiento_ia(tablero.traduccion_FEN(tablero.contador))
        #if lan == '404':
        stockfish.set_fen_position(tablero.traduccion_FEN(tablero.contador))
        lan : str = random.choice(stockfish.get_top_moves())['Move']
        #time.sleep(1)

    except Exception:
        print("Problemas con movimiento IA StockFish: No se ha podido obtener su movimiento. Se procederá a realizar un movimiento"
              "aleatorio")
        movimiento = movimimiento_aleatorio_IA(tablero, jugador_actual)
        time.sleep(3)
        return movimiento
    else:
        lan_hipersimplificado = comprobar_enroque_IA(transformacion_a_LAN_hipersimplificado(lan), tablero)
        time.sleep(1)

        movimiento = traducir_movimiento_ia(lan_hipersimplificado)

        return movimiento

def movimimiento_aleatorio_IA(tablero : "Tablero", jugador_actual : "Jugador") -> tuple[tuple, tuple, int] | tuple[
    tuple[int, Any], tuple[int, Any], int | Any]:
    promocion = ['R','N','B','Q'] if jugador_actual.color else ['r','n','b','q']

    while True:
        pieza = random.choice(jugador_actual.piezas)
        movimientos : list = list(pieza.movimiento_valido(tablero))
        if movimientos:
            break

    if str(pieza).upper() == 'K':
        movimientos.append(((),(),1))
        movimientos.append(((),(),2))

    movimiento = random.choice(movimientos)

    if str(pieza).upper() == 'P' and movimiento[0] in [0,7]:
        return pieza.posicion, movimiento, random.choice(promocion)

    if len(movimiento) == 3:
        return movimiento

    return pieza.posicion, movimiento, 0

def comprobar_enroque(movimiento : tuple, jugador_actual : "Jugador", enemigo : "Jugador", tablero : "Tablero") -> (bool, "Torre"):
    """
    Se ejecuta el caso especial de enroque en caso de que se digite dicho movimiento.

    Parametros:
    -----------
    movimiento : tuple
        Contiene en realidad solo un entero, pues no existe como tal la posición inicial y la final ya que están vacías.

    jugador_actual : Jugador
        Es el jugador que efectua el enroque.

    enemigo : Jugador
        Jugador de color contrario. Usado para comprobar si sus piezas amenazan las casillas intermedias.

    tablero : Tablero
        Tablero en sí. De ella se obtienen las casillas intermedias entre el rey y la torre.

    Retorna:
    ----------
    (bool, Torre)
        Devuelve True si se ha producido el enroque y devuelve también la torre que se ha movido para comprobar más tarde
        si ha hecho jaque al enemigo
    """

    # Buscamos el rey del jugador actual
    rey = next((rey for rey in jugador_actual.piezas if isinstance(rey, Rey)), None)

    # Buscamos la torre adecuada al enroque digitado
    if movimiento[2] == 1:
        torre = next((torre for torre in jugador_actual.piezas if isinstance(torre, Torre) \
                      and torre.posicion[1] == 7), None)
    else:
        torre = next((torre for torre in jugador_actual.piezas if isinstance(torre, Torre) \
                      and torre.posicion[1] == 0), None)
    try:
        # Si no se encuentra la torre se cancela el enroque
        if torre is None:
            raise ErrorPartida("No se ha encontrado una torre para hacer enroque","enroque")

        # Si por alguna razon no se encuentra se considera invalido (aunque nunca debería pasar esto).
        if rey is None:
            raise ErrorPartida("No se ha encontrado un rey para hacer enroque", "enroque")

    except ErrorPartida as e:
        print(e)
        return False, torre
    else:
        # Se acceden a sus posiciones.
        pos_rey = rey.posicion
        pos_torre = torre.posicion

        # Se comprueba si ha sido un exito el enroque
        intento: bool = comprobar_mov_enroque(tablero, enemigo, rey, torre, movimiento[2])

        # Si no ha sido un éxito se devuelve todo a su estado original
        if not intento:
            rey.posicion = pos_rey
            torre.posicion = pos_torre
            print("No ha sido posible hacer el enroque")
            return False, torre

        return True, torre

def comprobar_mov_enroque(tablero : "Tablero", enemigo : "Jugador", rey : "Rey",
                            torre : "Torre", enroque : int) -> bool:
    """
    Comprueba si el enroque es posible. Para ello comprueba cada una de las exigencias que se deben cumplir para
    realizar un enroque. Puede comprobar tanto el enroque largo como el corto

    Parametros:
    -----------
    tablero : Tablero -> Tablero en sí. De ella se obtienen las casillas intermedias entre el rey y la torre.

    enemigo : Jugador -> Jugador de color contrario. Usado para comprobar si sus piezas amenazan las casillas intermedias.

    rey : Rey -> Rey del jugador actual. Necesario para poder comprobar si puede hacer enroque.

    torre : Torre -> Torre del jugador actual. Necesario para poder comprobar si puede hacer enroque.

    enroque : int
        Marca el tipo de enroque siendo 2 un enroque largo y 1 un enroque corto

    Retorna:
    ----------
    bool
        Devuelve True si se ha producido el eroque corto
    """
    try:
        # Comprobamos si ambos pueden hacer enroque
        if not rey.enroque():
            raise ErrorPartida(f"{type(rey).__name__} no puede hacer enroque porque ya se ha movido.", "hacer enroque")
        if not torre.enroque():
            raise ErrorPartida(f"{type(torre).__name__} no puede hacer enroque porque ya se ha movido.", "hacer enroque")

        #Calculamos el número de casillas intermedias
        intermedias = abs(rey.posicion[1] - torre.posicion[1])
        fila = 7 if rey.color else 0
        i = 1 if enroque == 1 else -1

        #Comprobamos cada una de las casillas intermedias si están libres completamente.
        for j in range(1, intermedias):
            columna : int = rey.posicion[1] + j * i
            if tablero.amenazas(enemigo, fila, columna):
                raise ErrorPartida("Una casilla es amenazada por alguna pieza enemiga", "hacer enroque")

            if tablero[fila][columna].pieza is not None:
                raise ErrorPartida(f"El camino entre {type(rey).__name__} y {type(torre).__name__} no está despejado", "hacer enroque")
    except ErrorPartida as e:
        print(e)
        return False
    else:
        #Se realiza el enroque según si es largo o corto
        columna : int = rey.posicion[1]
        rey.posicion = (fila, columna + 2*i)
        rey.movido = True
        tablero[fila][columna].pieza = None
        tablero[fila][rey.posicion[1]].pieza = rey

        columna : int = torre.posicion[1]
        torre.posicion = (fila, columna - 2*i) if enroque == 1 else (fila, columna - 2*i + 1)
        tablero[fila][columna].pieza = None
        tablero[fila][torre.posicion[1]].pieza = torre

        print("Enroque exitoso")

        return True

def comprobar_enroque_IA(san : list[str,str] | str, tablero : "Tablero") -> str:
    if type(san) == str:
        return san

    posicion = traducir_movimiento_ia(san[1])[0]

    if isinstance(tablero[posicion[0]][posicion[1]].pieza,Rey):
        return san[0]

    return san[1]

def comprobar_movimiento(movimiento : tuple, jugador_actual : "Jugador", enemigo : "Jugador", tablero : "Tablero") -> (bool,"Pieza"):
    """
    Se ejecuta el movimiento digitado por el jugador actual.

    Parametros:
    -----------
    movimiento : tuple
        Contiene el movimiento del jugador actual.

    jugador_actual : Jugador
        Es el jugador que efectua el movimiento.

    enemigo : Jugador
        Jugador de color contrario.

    tablero : Tablero
        Tablero en sí.

    Retorna:
    ----------
    (bool, Pieza)
        Devuelve True si se ha producido el movimiento y devuelve también la pieza que se ha movido.
    """

    # Se busca la pieza
    pieza: Union["Pieza", None] = encontrar_pieza(jugador_actual, movimiento[0])

    try:
        # Si no se ha encontrado la pieza se anula el movimiento.
        if pieza is None:
            raise ErrorPartida("No se ha encontrado ninguna pieza.","buscar una pieza")

        # Si el movimiento es incorrecto se considera invalido el movimiento.
        if not pieza.mover(movimiento[1], tablero, jugador_actual, enemigo, str(movimiento[2])):
            raise ErrorPartida("El movimiento es inválido (autojaque, movimiento impromio de la pieza, etc)", "movimiento inválido")
    except ErrorPartida as e:
        print(e)
        return False, pieza
    else:
        # Se inicializa su atributo movido si lo contiene.
        if str(pieza).upper() in ['K', 'R', 'P']:
            pieza.movido = True

        #tablero.en_passant[0] = traduccion_inversa(tablero.en_passant[1])
        return True, pieza

def comprobar_promocion(pieza : "Pieza", promocion : Union[str,int], jugador_actual : "Jugador", tablero : "Tablero") -> bool:
    """
    Comprueba si la promocion es válida. En caso afirmativo realiza la promoción correspondiente

    Parametros:
    -----------
    pieza : Peon -> Es el peon que se va a promocionar.

    promocion : Union[str,int] -> Promocion digitado por el usuario.

    jugador_actual : Jugador -> Dueño del peon que se va a promocionar

    Retorna:
    ----------
    bool
        Devuelve True si se ha producido la promocion
    """
    try:
        if pieza not in jugador_actual.piezas:
            raise ErrorPartida(f"No existe dicha pieza en el inventario de {jugador_actual.nombre}", pieza)

    except ErrorPartida as e:
        print(e)
        return False
    else:
        # Se almacena la pieza y su posición dentro del inventario
        indice = jugador_actual.piezas.index(pieza)
        jugador_actual.piezas.remove(pieza)

    try:
        if promocion.upper() not in ['Q','R','B','N']:
            raise ErrorPartida(str(ErrorCrearPieza(pieza,"Se ha intentado promocionar a una pieza prohibida o no definida",True)),
                               f"promocionar con {type(pieza).__name__}")

    except ErrorPartida as e:
        print(e)
        jugador_actual.piezas.insert(indice, pieza)
        return False

    else:
        # Se comprueba que promoción ha hecho, en caso afirmativo se sustituye por dicha pieza.
        match promocion:
            case 'Q':
                pieza = Reina(pieza.posicion, pieza.color)
                jugador_actual.piezas.insert(indice,pieza)
                tablero[pieza.posicion[0]][pieza.posicion[1]].pieza = pieza

            case 'R':
                pieza = Torre(pieza.posicion, pieza.color)
                pieza.movido = True
                jugador_actual.piezas.insert(indice, pieza)
                tablero[pieza.posicion[0]][pieza.posicion[1]].pieza = pieza

            case 'B':
                pieza = Alfil(pieza.posicion, pieza.color)
                jugador_actual.piezas.insert(indice, pieza)
                tablero[pieza.posicion[0]][pieza.posicion[1]].pieza = pieza

            case 'N':
                pieza = Caballo(pieza.posicion, pieza.color)
                jugador_actual.piezas.insert(indice, pieza)
                tablero[pieza.posicion[0]][pieza.posicion[1]].pieza = pieza

        print("Promoción exitosa")
        return True

def comprobar_jaque_enemigo(tablero : "Tablero", jugador_actual : "Jugador", enemigo : "Jugador",
                            pieza : Union["Pieza",None]) -> bool:
    """
    Comprueba si el movimiento del jugador actual ha hecho jaque al enemigo.

    Parametros:
    -----------
    tablero : Tablero -> Tablero en sí.

    jugador_actual : Jugador -> Jugador que ha realizado el jaque.

    enemgio : Jugador -> Dueño del rey que se ha puesto en jaque.

    pieza : Pieza -> Pieza que ha sido movido y que podria haber puesto en jaque al enemigo

    Retorna:
    ----------
    bool
        Devuelve True si se ha producido un jaque
    """
    try:
        # Se busca al rey enemigo
        rey_enemigo = next((rey for rey in enemigo.piezas if isinstance(rey, Rey)), None)

        # Si por alguna razon no se encuentra se considera invalido (aunque nunca debería pasar esto).
        if rey_enemigo is None:
            raise ErrorPartida("No se ha encontrado el rey enemigo","buscar rey enemigo")
    except ErrorPartida as e:
        print(e)
        return True
    else:
        # Si por alguna razon no hay una pieza que amenace, se comprueba si alguna pieza del jugador actual ataca al rey enemigo
        if pieza is None:
            return True if tablero.amenazas(jugador_actual, rey_enemigo.posicion[0], rey_enemigo.posicion[1]) else False

        # Se comprueba si la pieza ataca al rey enemigo
        return True if rey_enemigo.posicion in pieza.movimiento_valido(tablero) else False

def caso_jaque(tablero : "Tablero", jugador_actual : "Jugador", enemigo : "Jugador", movimiento : tuple) -> bool:
    """
    Función que trata el caso especial de jaque. En ella se tratan todos los casos posibles dentro de un jaque para
    determinar si el movimiento evita el jaque.

    Parametros:
    -----------
    tablero : Tablero -> Tablero en sí.

    jugador_actual : Jugador -> Jugador que ha recibido el jaque

    enemgio : Jugador -> Jugador que ha hecho jaque

    movimiento : tuple -> Movimiento digitado por el jugador actual

    Retorna:
    ----------
    bool
        Retorna True si ha evitado el jaque
    """
    try:
        # Si se intenta hacer enroque en medio de un jaque se considera inválido el movimiento
        if type(movimiento[2]) == int and movimiento[2] in [1,2]:
            raise ErrorPartida("Se ha intentado hacer un enroque en medio de un jaque","movimiento digitado")

        # Buscamos la pieza que queremos mover
        pieza : Union["Pieza",None] = encontrar_pieza(jugador_actual, movimiento[0])

        # Si no se ha encontrado ninguna se considera inválido.
        if pieza is None:
            raise ErrorPartida("No se ha encontrado ninguna pieza.","buscar una pieza")

        # No se puede promocionar si no eres un peon.
        if str(movimiento[2]).isalpha() and not isinstance(pieza, Peon):
            raise ErrorPartida("Se ha intentado promocionar una pieza que no es peón","promoción")

        # Se busca el rey del jugador actual
        rey = next((rey for rey in jugador_actual.piezas if isinstance(rey, Rey)), None)

        # Si por alguna razon no se encuentra se considera invalido (aunque nunca debería pasar esto).
        if rey is None:
            raise ErrorPartida("No se ha encontrado el rey del jugador","buscar rey del jugador")

        # Se comprueba si el movimiento es capaz de evitar el jaque
        if not pieza.mover(movimiento[1], tablero, jugador_actual, enemigo, str(movimiento[2])):
            raise ErrorPartida("El movimiento es inválido (autojaque, movimiento impromio de la pieza, etc)", "movimiento inválido")

    except ErrorPartida as e:
        print(e)
        return False
    else:
        return True

def comprobar_tablas(tablero : "Tablero", jugador_actual : "Jugador", enemigo : "Jugador") -> bool:
    """
    Comprueba si se ha producido un empate

    Parametros:
    -----------
    tablero : Tablero -> Tablero en sí.

    jugador_actual : Jugador -> Jugador que ha realizado el jaque.

    enemgio : Jugador -> Dueño del rey que se ha puesto en jaque.

    Retorna:
    ----------
    bool
        Devuelve True si son tablas
    """
    try:
        # Se busca al rey del jugador actual
        rey = next((rey for rey in jugador_actual.piezas if isinstance(rey, Rey)), None)

        # Si por alguna razon no se encuentra se considera invalido (aunque nunca debería pasar esto).
        if rey is None:
            bandera = True
            raise ErrorPartida("No se ha encontrado el rey del jugador", "buscar rey del jugador")

    except ErrorPartida as e:
        print(e)
        return True
    else:
        # Si ambos solo tienen el rey se considera tablas.
        if len(jugador_actual.piezas) == 1 and len(enemigo.piezas) == 1:
            return True

        # Si el rey está amenazado entonces no puede ser tablas.
        if tablero.amenazas(enemigo, rey.posicion[0], rey.posicion[1]):
            return False

        # Si resulta que alguna pieza del jugador actual se puede mover entonces no es tablas.
        for pieza in jugador_actual.piezas:
            movimientos = pieza.movimiento_valido(tablero) if not isinstance(pieza, Rey) else []
            if movimientos:
                return False

if __name__ == "__main__":

    jug1 = Jugador("StockFish",1000)
    jug2 = Jugador("StockFish",2300)
    partida(jug1, jug2, True)
    """
    print(Tablero.creacion_con_FEN('rnbqk2r/pp3ppp/5n2/3p4/1b2p3/2N3P1/PP1PPPBP/R1BQK1NR b KQkq - 0 14'))
    stockfish.set_fen_position("rnbqk2r/pp3ppp/5n2/3p4/1b2p3/2N3P1/PP1PPPBP/R1BQK1NR b KQkq - 0 14")
    print("Mejor movimiento:", stockfish.get_best_move())
    """