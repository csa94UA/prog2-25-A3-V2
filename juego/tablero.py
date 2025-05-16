"""
Módulo para la representación y manipulación del tablero de ajedrez.

Este módulo define la clase `Tablero`, que encapsula la lógica del estado del juego,
incluyendo el movimiento de piezas, promoción de peones, interpretación de entradas
en notación algebraica y clonación/restauración del estado del juego.

Clases:
    - Tablero
"""

from typing import List, Optional, Tuple, Dict, Union


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
    obtener_tablero_como_texto() -> List[str]:
        Devuelve una representación textual del tablero.
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

    def colocar_piezas_iniciales(self) -> None:
        """
        Coloca las piezas en sus posiciones iniciales en el tablero.

        (Este método debe ser implementado en otro momento).
        """
        pass

    def mover_pieza(
        self, origenydestino: Tuple[Tuple[int, int], Tuple[int, int]]
    ) -> Dict[str, Union[bool, str, Tuple[int, int]]]:
        """
        Mueve una pieza en el tablero desde la posición de origen hasta el destino, validando la legalidad.

        Parámetros:
        -----------
        origenydestino : Tuple[Tuple[int, int], Tuple[int, int]]
            Coordenadas de origen y destino del movimiento.

        Retorna:
        --------
        Dict[str, Union[bool, str, Tuple[int, int]]]
            Diccionario que indica si el movimiento fue exitoso y detalles relevantes.
        """
        origen, destino = origenydestino
        fila_origen, col_origen = origen
        fila_destino, col_destino = destino

        pieza = self.casillas[fila_origen][col_origen]
        if pieza is None:
            return {"exito": False, "error": "No hay pieza en la casilla de origen."}

        movimientos_validos = pieza.obtener_movimientos_validos(
            (fila_origen, col_origen), self, evitar_jaque=False
        )
        if (fila_destino, col_destino) not in movimientos_validos:
            return {"exito": False, "error": "Movimiento no válido para la pieza."}

        # Enroque (sin implementar)
        pass

        # Captura al paso (sin implementar)
        pass

        # Movimiento normal
        self.casillas[fila_destino][col_destino] = pieza
        self.casillas[fila_origen][col_origen] = None

        if hasattr(pieza, "se_ha_movido"):
            pieza.se_ha_movido = True

        # Promoción de peón (sin implementar)
        pass

        self.ultimo_movimiento = ((fila_origen, col_origen), (fila_destino, col_destino), pieza)

        return {
            "exito": True,
            "pieza": pieza.__class__.__name__,
            "origen": origen,
            "destino": destino,
        }

    def promocionar_peon(self, fila: int, columna: int, color: str) -> None:
        """
        Promociona un peón ubicado en la fila y columna especificadas.

        Parámetros:
        -----------
        fila : int
            Fila del peón a promocionar.
        columna : int
            Columna del peón a promocionar.
        color : str
            Color de la nueva pieza (usualmente se convierte en dama).

        (Este método debe ser implementado).
        """
        pass

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

    def obtener_tablero_como_texto(self) -> List[str]:
        """
        Genera una representación visual del tablero en forma de texto.

        Retorna:
        --------
        List[str]
            Lista de líneas que representan el tablero.
        """
        tablero_str = ["  a b c d e f g h"]
        for fila in range(8):
            linea = f"{8 - fila} "
            for col in range(8):
                pieza = self.casillas[fila][col]
                linea += pieza.simbolo() + " " if pieza else ". "
            linea += f"{8 - fila}"
            tablero_str.append(linea)
        tablero_str.append("  a b c d e f g h")
        tablero_str.append("")
        return tablero_str

    def guardar_estado(self) -> Dict[str, object]:
        """
        Devuelve una copia segura del estado actual del tablero, clonando manualmente cada pieza.

        Retorna:
        --------
        Dict[str, object]
            Diccionario con la copia de las casillas y del último movimiento.
        """
        estado_casillas = []
        for fila in self.casillas:
            nueva_fila = [pieza.clonar() if pieza else None for pieza in fila]
            estado_casillas.append(nueva_fila)

        estado_movimiento = None
        if self.ultimo_movimiento:
            origen, destino, pieza = self.ultimo_movimiento
            estado_movimiento = (origen, destino, pieza.clonar() if pieza else None)

        return {
            "casillas": estado_casillas,
            "ultimo_movimiento": estado_movimiento
        }

    def restaurar_estado(self, estado: Dict[str, object]) -> None:
        """
        Restaura el estado del tablero a partir del diccionario dado.

        Parámetros:
        -----------
        estado : Dict[str, object]
            Diccionario que contiene la información del estado anterior del tablero.
        """
        self.casillas = estado["casillas"]
        self.ultimo_movimiento = estado["ultimo_movimiento"]

    def mover_pieza_tests(
        self, origenydestino: Tuple[Tuple[int, int], Tuple[int, int]]
    ) -> bool:
        """
        Mueve una pieza de forma directa, sin validaciones, útil para pruebas internas.

        Parámetros:
        -----------
        origenydestino : Tuple[Tuple[int, int], Tuple[int, int]]
            Coordenadas de origen y destino.

        Retorna:
        --------
        bool
            True si la pieza fue movida, False si no había pieza en la casilla de origen.
        """
        origen, destino = origenydestino
        fila_origen, col_origen = origen
        fila_destino, col_destino = destino

        pieza = self.casillas[fila_origen][col_origen]
        if pieza is None:
            return False

        self.casillas[fila_origen][col_origen] = None
        self.casillas[fila_destino][col_destino] = pieza

        return True
