from Tablero import Tablero
from Piezas import Pieza

INF = 1000000


class IADeAjedrez:
    def __init__(self,, max_profundidad: int = 5) -> None:
        """
        Inicializa la inteligencia artificial con los parámetros de búsqueda.

        Parametros:
        -----------
        max_profundidad : int
            La máxima profundidad de búsqueda para el algoritmo Alfa-Beta. (Valor por defecto: 5)
        """
        self.max_profundidad = max_profundidad
        self.tabla_transposicion = {}

    def evaluar(self, tablero: Tablero) -> int:
        """
        Evalúa la posición actual del tablero en función de los valores de las piezas.

        Parametros:
        -----------
        tablero : Tablero
            El tablero de ajedrez sobre el cual se realiza la evaluación.

        Retorna:
        --------
        int
            El valor de la posición en función de las piezas, donde un valor positivo es favorable
            para las piezas de la IA y un valor negativo para las piezas del Jugador.
        """
        valor = 0
        for fila in tablero.tablero:
            for casilla in fila:
                if casilla.pieza:
                    valor += casilla.pieza.valor if casilla.pieza.color else -casilla.pieza.valor
        return valor

    def alfa_beta(self, tablero: Tablero, profundidad: int, alfa: float, beta: float, maximizando: bool) -> float:
        """
        Implementa el algoritmo de búsqueda Alfa-Beta para la selección del mejor movimiento.

        Parametros:
        -----------
        tablero : Tablero
            El tablero de ajedrez sobre el cual se realiza la búsqueda.
        profundidad : int
            La profundidad actual de la búsqueda.
        alfa : float
            El valor mínimo que el jugador maximizante está dispuesto a aceptar.
        beta : float
            El valor máximo que el jugador minimizante está dispuesto a aceptar.
        maximizando : bool
            Indica si es el turno del jugador maximizante (IA) o del minimizante (Jugador).

        Retorna:
        --------
        float
            El valor de la mejor jugada encontrada en el árbol de búsqueda.
        """
        tablero_fen = tablero.traduccion_FEN(tablero.turno, tablero.enroque[0] if tablero.enroque else False,
                                             tablero.enroque[1] if tablero.enroque else False, tablero.en_passant,
                                             tablero.contador, tablero.turno)
        if tablero_fen in self.tabla_transposicion and profundidad <= self.tabla_transposicion[tablero_fen][1]:
            return self.tabla_transposicion[tablero_fen][0]

        if profundidad == 0:
            return self.evaluar(tablero)

        movimientos = self.generar_movimientos(tablero, maximizando)
        mejor_valor = -INF if maximizando else INF

        for pieza, movimiento in movimientos:
            estado_anterior = tablero.guardar_estado()
            Pieza.mover(pieza, movimiento, tablero, self.jugador, self.enemigo, 1)
            valor = self.alfa_beta(tablero, profundidad - 1, alfa, beta, not maximizando)
            tablero.restaurar_estado(estado_anterior)

            if maximizando:
                mejor_valor = max(mejor_valor, valor)
                alfa = max(alfa, valor)
            else:
                mejor_valor = min(mejor_valor, valor)
                beta = min(beta, valor)

            if beta <= alfa:
                break

        self.tabla_transposicion[tablero_fen] = (mejor_valor, profundidad)
        return mejor_valor

    def generar_movimientos(self, tablero: Tablero, color: bool) -> list:
        """
        Genera todos los movimientos válidos para un jugador de un color dado.

        Parametros:
        -----------
        tablero : Tablero
            El tablero de ajedrez donde se generan los movimientos.
        color : bool
            El color del jugador que está por mover (True para IA, False para Jugador).

        Retorna:
        --------
        list
            Una lista de tuplas que contienen la pieza y el movimiento válido generado.
        """
        movimientos = []
        for fila in tablero.tablero:
            for casilla in fila:
                if casilla.pieza and casilla.pieza.color == color:
                    for movimiento in casilla.pieza.movimiento_valido(tablero):
                        movimientos.append((casilla.pieza, movimiento))
        return movimientos

    def encontrar_mejor_movimiento(self, tablero: Tablero) -> tuple:
        """
        Encuentra el mejor movimiento utilizando el algoritmo de búsqueda Alfa-Beta.

        Parametros:
        -----------
        tablero : Tablero
            El tablero de ajedrez donde se realizará la búsqueda del mejor movimiento.

        Retorna:
        --------
        tuple
            Devuelve el mejor movimiento encontrado, compuesto por la pieza y el movimiento seleccionado.
        """
        mejor_movimiento = None
        mejor_valor = -INF

        movimientos = self.generar_movimientos(tablero, True)

        for pieza, movimiento in movimientos:
            estado_anterior = tablero.guardar_estado()
            Pieza.mover(pieza, movimiento, tablero, self.jugador, self.enemigo, 1)
            valor = self.alfa_beta(tablero, self.max_profundidad - 1, -INF, INF, False)
            tablero.restaurar_estado(estado_anterior)

            if valor > mejor_valor:
                mejor_valor = valor
                mejor_movimiento = (pieza, movimiento)

        return mejor_movimiento
