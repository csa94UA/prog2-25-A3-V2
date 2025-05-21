"""
Módulo para la representación y manipulación del tablero de ajedrez.

Este módulo define la clase `Tablero`, que encapsula la lógica del estado del juego,
incluyendo el movimiento de piezas, promoción de peones, interpretación de entradas
en notación algebraica y clonación/restauración del estado del juego.

Clases:
    - Tablero
"""

from typing import List, Optional, Tuple, Dict, Union
from piezas.peon import Peon
from piezas.torre import Torre
from piezas.caballo import Caballo
from piezas.alfil import Alfil
from piezas.reina import Reina
from piezas.rey import Rey
from piezas.pieza_base import Pieza
from juego.validador_movimiento import ValidadorMovimiento

class Tablero:
    """
    Clase que representa un tablero de ajedrez de 8x8.

    Atributos:
    ----------
    casillas : List[List[Optional[Pieza]]]
        Matriz 8x8 que contiene las piezas del tablero o None en casillas vacías.
    ultimo_movimiento : Optional[Tuple[Tuple[int, int], Tuple[int, int], Pieza]]
        Información sobre el último movimiento realizado.

    Métodos:
    --------
    colocar_piezas_iniciales() -> None:
        Coloca las piezas en su posición inicial (sin implementar).
    mover_pieza(origenydestino: Tuple[Tuple[int, int], Tuple[int, int]]) -> Dict[str, Union[bool, str, Tuple[int, int]]]:
        Mueve una pieza de una casilla a otra si el movimiento es válido.
    promocionar_peon(fila: int, columna: int, color: str) -> None:
        Realiza la promoción de un peón (sin implementar).
    interpretar_entrada(entrada: str) -> Optional[Tuple[Tuple[int, int], Tuple[int, int]]]:
        Convierte una entrada en notación algebraica a coordenadas internas.
    guardar_estado() -> Dict[str, Any]:
        Retorna una copia del estado actual del tablero.
    restaurar_estado(estado: Dict[str, Any]) -> None:
        Restaura el estado del tablero desde una copia previamente guardada.
    mover_pieza_tests(origenydestino: Tuple[Tuple[int, int], Tuple[int, int]]) -> bool:
        Mueve una pieza sin validación para pruebas internas.
    """

    def __init__(self) -> None:
        self.casillas: List[List[Optional[object]]] = [[None for _ in range(8)] for _ in range(8)]
        self.ultimo_movimiento: Optional[Tuple[Tuple[int, int], Tuple[int, int], object]] = None
        self.colocar_piezas_iniciales()
        self.historial_movimientos = []  
        self.validador: ValidadorMovimiento = ValidadorMovimiento(self)


    def __str__(self) -> str:
        """
        Devuelve una representación visual del tablero en forma de cadena de texto imprimible.

        Retorna:
        --------
        str
            Cadena que representa visualmente el tablero de ajedrez.
        """
        lineas: list[str] = ["  a b c d e f g h"]
        for fila in range(8):
            linea = f"{8 - fila} "
            for col in range(8):
                pieza = self.casillas[fila][col]
                linea += pieza.simbolo() + " " if pieza else ". "
            linea += f"{8 - fila}"
            lineas.append(linea)
        lineas.append("  a b c d e f g h")
        return '\n'.join(lineas)


    def colocar_piezas_iniciales(self) -> None:
        """
        Coloca las piezas en sus posiciones iniciales en el tablero.
        """
        self.casillas[7][0] = Torre("blanco")
        self.casillas[7][1] = Caballo("blanco")
        self.casillas[7][2] = Alfil("blanco")
        self.casillas[7][3] = Reina("blanco")
        self.casillas[7][4] = Rey("blanco")
        self.casillas[7][5] = Alfil("blanco")
        self.casillas[7][6] = Caballo("blanco")
        self.casillas[7][7] = Torre("blanco")
        for col in range(8):
            self.casillas[6][col] = Peon("blanco")
        self.casillas[0][0] = Torre("negro")
        self.casillas[0][1] = Caballo("negro")
        self.casillas[0][2] = Alfil("negro")
        self.casillas[0][3] = Reina("negro")
        self.casillas[0][4] = Rey("negro")
        self.casillas[0][5] = Alfil("negro")
        self.casillas[0][6] = Caballo("negro")
        self.casillas[0][7] = Torre("negro")
        for col in range(8):
            self.casillas[1][col] = Peon("negro")

    def mover_pieza(
        self,
        origenydestino: Tuple[Tuple[int, int], Tuple[int, int]],
        promocion: Optional[str] = None
    ) -> Dict[str, Union[bool, str, Tuple[int, int]]]:
        """
        Intenta mover una pieza del tablero desde una posición de origen a una de destino,
        validando la legalidad del movimiento, incluyendo enroque, captura al paso y promoción.

        Parámetros:
        -----------
        origenydestino : Tuple[Tuple[int, int], Tuple[int, int]]
            Coordenadas de origen y destino del movimiento.

        promocion : Optional[str]
            En caso de que se requiera promoción de peón, especifica la pieza deseada ("dama", "torre", "alfil", "caballo").

        Retorna:
        --------
        Dict[str, Union[bool, str, Tuple[int, int]]]
            Diccionario con información sobre el resultado del movimiento:
                - "exito": bool
                - "error": str, si hubo fallo
                - "requiere_promocion": bool, si se necesita seleccionar pieza para promoción
                - "pieza": str, nombre de la pieza movida
                - "origen" y "destino": coordenadas
        """

        origen, destino = origenydestino
        fila_origen, col_origen = origen
        fila_destino, col_destino = destino

        pieza = self.casillas[fila_origen][col_origen]
        if pieza is None:
            return {"exito": False, "error": "No hay pieza en la casilla de origen."}

        movimientos_validos = pieza.obtener_movimientos_validos(
            (fila_origen, col_origen), self
        )
        if (fila_destino, col_destino) not in movimientos_validos or self.validador.movimiento_es_legal((fila_origen,col_origen),(fila_destino,col_destino),pieza.color):
            return {"exito": False, "error": "Movimiento no válido para la pieza."}

        # Enroque
        if isinstance(pieza, Rey) and abs(col_destino - col_origen) == 2:
            fila = fila_origen
            if col_destino == 6:  # Enroque corto
                torre = self.casillas[fila][7]
                self.casillas[fila][5] = torre
                self.casillas[fila][7] = None
                torre.se_ha_movido = True
            elif col_destino == 2:  # Enroque largo
                torre = self.casillas[fila][0]
                self.casillas[fila][3] = torre
                self.casillas[fila][0] = None
                torre.se_ha_movido = True

        # Captura al paso
        if isinstance(pieza, Peon) and col_origen != col_destino and self.casillas[fila_destino][col_destino] is None:
            fila_captura = fila_origen
            self.casillas[fila_captura][col_destino] = None

        # Movimiento normal
        self.casillas[fila_destino][col_destino] = pieza
        self.casillas[fila_origen][col_origen] = None

        if hasattr(pieza, "se_ha_movido"):
            pieza.se_ha_movido = True

        # Promoción de peón
        if isinstance(pieza, Peon):
            if (pieza.color == "blanco" and fila_destino == 0) or (pieza.color == "negro" and fila_destino == 7):
                if promocion is None:
                    return {
                        "exito": False,
                        "error": "Se requiere una pieza para promoción: dama, torre, alfil o caballo.",
                        "requiere_promocion": True
                    }
                resultado_promocion = self.promocionar_peon(fila_destino, col_destino, pieza.color, promocion)
                if resultado_promocion is not True:
                    return {"exito": False, "error": resultado_promocion}

        self.ultimo_movimiento = ((fila_origen, col_origen), (fila_destino, col_destino), pieza)

        return {
            "exito": True,
            "pieza": pieza.__class__.__name__,
            "origen": origen,
            "destino": destino,
        }

    def promocionar_peon(self, fila: int, columna: int, color: str, eleccion: str) -> Union[bool, str]:
        """
        Promociona un peón en la posición dada a una nueva pieza, según la elección del usuario.

        Parámetros:
        -----------
        fila : int
            Fila en la que se encuentra el peón a promocionar.

        columna : int
            Columna en la que se encuentra el peón a promocionar.

        color : str
            Color del peón ("blanco" o "negro").

        eleccion : str
            Pieza a la que se desea promocionar ("dama", "torre", "alfil", "caballo").

        Retorna:
        --------
        Union[bool, str]
            True si la promoción fue exitosa, o un mensaje de error si la opción es inválida.
        """

        eleccion = eleccion.strip().lower()
        if eleccion == "dama":
            self.casillas[fila][columna] = Reina(color)
        elif eleccion == "torre":
            self.casillas[fila][columna] = Torre(color)
        elif eleccion == "alfil":
            self.casillas[fila][columna] = Alfil(color)
        elif eleccion == "caballo":
            self.casillas[fila][columna] = Caballo(color)
        else:
            return "Opción no válida. Elige dama, torre, alfil o caballo."

        return True


    def interpretar_entrada(self, entrada: str) -> Optional[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """
        Convierte una cadena en notación algebraica (ej. 'e2 e4') a coordenadas internas.

        Parámetros:
        -----------
        entrada : str
            Movimiento en formato algebraico.

        Retorna:
        --------
        Optional[Tuple[Tuple[int, int], Tuple[int, int]]]
            Tupla con coordenadas de origen y destino, o None si hay error de formato.
        """
        try:
            origen_str, destino_str = entrada.strip().lower().split()
            columnas = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}

            if len(origen_str) != 2 or len(destino_str) != 2:
                return None

            col1 = columnas.get(origen_str[0])
            fila1 = 8 - int(origen_str[1])
            col2 = columnas.get(destino_str[0])
            fila2 = 8 - int(destino_str[1])

            if None in (col1, col2) or not (0 <= fila1 < 8) or not (0 <= fila2 < 8):
                return None

            return ((fila1, col1), (fila2, col2))
        except Exception:
            return None
        

    def hacer_movimiento(self, origen: Tuple[int, int], destino: Tuple[int, int]) -> None:
        """
        Realiza un movimiento de una pieza en el tablero y guarda la información necesaria 
        para revertirlo posteriormente.

        Args:
            origen (Tuple[int, int]): Coordenada (fila, columna) de origen.
            destino (Tuple[int, int]): Coordenada (fila, columna) de destino.
        """
        fila_o, col_o = origen
        fila_d, col_d = destino

        pieza_origen: Optional[Pieza] = self.casillas[fila_o][col_o]
        pieza_capturada: Optional[Pieza] = self.casillas[fila_d][col_d]

        # Guardamos el movimiento para poder deshacerlo
        self.historial_movimientos.append((origen, destino, pieza_origen, pieza_capturada))

        # Realizamos el movimiento
        self.casillas[fila_d][col_d] = pieza_origen
        self.casillas[fila_o][col_o] = None

    def deshacer_ultimo_movimiento(self) -> None:
        """
        Revierte el último movimiento realizado en el tablero.
        Si no hay movimientos para deshacer, no hace nada.
        """
        if not self.historial_movimientos:
            return

        origen, destino, pieza_origen, pieza_capturada = self.historial_movimientos.pop()

        fila_o, col_o = origen
        fila_d, col_d = destino

        # Restauramos el estado anterior del tablero
        self.casillas[fila_o][col_o] = pieza_origen
        self.casillas[fila_d][col_d] = pieza_capturada

    def generar_hash(self) -> str:
        """
        Genera una representación en forma de cadena del estado actual del tablero.
        Útil para implementaciones de tablas de transposición o almacenamiento en caché.

        Returns:
            str: Cadena que representa el estado del tablero.
        """
        piezas: List[str] = []

        for fila in self.casillas:
            for p in fila:
                if p:
                    piezas.append(f"{p.__class__.__name__[0]}{p.color[0]}")
                else:
                    piezas.append("..")  # Casilla vacía

        return ''.join(piezas)
    
    def restaurar_estado_lista(self, lista: List[List[Optional[Dict[str, str]]]]) -> None:
        """
        Restaura el estado del tablero a partir de una lista bidimensional que representa 
        cada casilla con un diccionario que indica el tipo y color de la pieza, o None si está vacía.

        Parámetros:
        -----------
        lista : List[List[Optional[Dict[str, str]]]]
            Lista 2D que representa el tablero. Cada elemento puede ser:
            - Un diccionario con las claves "tipo" (str) y "color" (str) que identifican 
            la pieza que debe colocarse en esa casilla.
            - None, si la casilla está vacía.

        Retorna:
        --------
        None

        Efecto:
        --------
        Modifica el atributo `self.casillas` asignando instancias de las clases de piezas 
        correspondientes en las posiciones indicadas por la lista. Si un elemento es None, 
        deja la casilla vacía (None).
        """
        for x, fila in enumerate(lista):
            for y, dicc in enumerate(fila):
                if dicc is not None:
                    tipo: str = dicc["tipo"]
                    color: str = dicc["color"]
                    if tipo == "peon":
                        self.casillas[x][y] = Peon(color)
                    elif tipo == "torre":
                        self.casillas[x][y] = Torre(color)
                    elif tipo == "caballo":
                        self.casillas[x][y] = Caballo(color)
                    elif tipo == "alfil":
                        self.casillas[x][y] = Alfil(color)
                    elif tipo == "dama":
                        self.casillas[x][y] = Reina(color)
                    elif tipo == "rey":
                        self.casillas[x][y] = Rey(color)
                    else:
                        # En caso de que llegue un tipo desconocido
                        self.casillas[x][y] = None
                else:
                    self.casillas[x][y] = None