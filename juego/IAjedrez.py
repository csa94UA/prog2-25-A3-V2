from typing import Optional 
from juego.tablero import Tablero

INF = 1000000

# Tablas de valores posicionales simplificadas para cada tipo de pieza (blancas).
# La posición [0][0] es la esquina inferior izquierda desde la perspectiva blanca.
# Las negras usarán la tabla invertida verticalmente.
PSQT_PEON = [
    [ 0,  0,  0,  0,  0,  0,  0,  0],
    [ 5, 10, 10,-20,-20, 10, 10,  5],
    [ 5, -5,-10,  0,  0,-10, -5,  5],
    [ 0,  0,  0, 20, 20,  0,  0,  0],
    [ 5,  5, 10, 25, 25, 10,  5,  5],
    [10, 10, 20, 30, 30, 20, 10, 10],
    [50, 50, 50, 50, 50, 50, 50, 50],
    [ 100,  100,  100,  100,  100,  100,  100,  100] # un incentivo para que la ia lleve el peon hasta el final y este se convierta en una dama (no elige si es ia, simplemente se convierte en dama)
]

PSQT_CABALLO = [
    [-50,-40,-30,-30,-30,-30,-40,-50],
    [-40,-20,  0,  0,  0,  0,-20,-40],
    [-30,  0, 10, 15, 15, 10,  0,-30],
    [-30,  5, 15, 20, 20, 15,  5,-30],
    [-30,  0, 15, 20, 20, 15,  0,-30],
    [-30,  5, 10, 15, 15, 10,  5,-30],
    [-40,-20,  0,  5,  5,  0,-20,-40],
    [-50,-40,-30,-30,-30,-30,-40,-50]
]

PSQT_ALFIL = [
    [-20,-10,-10,-10,-10,-10,-10,-20],
    [-10,  0,  0,  0,  0,  0,  0,-10],
    [-10,  0,  5, 10, 10,  5,  0,-10],
    [-10,  5,  5, 10, 10,  5,  5,-10],
    [-10,  0, 10, 10, 10, 10,  0,-10],
    [-10, 10, 10, 10, 10, 10, 10,-10],
    [-10,  5,  0,  0,  0,  0,  5,-10],
    [-20,-10,-10,-10,-10,-10,-10,-20]
]

PSQT_TORRE = [
    [ 0,  0,  0,  0,  0,  0,  0,  0],
    [ 5, 10, 10, 10, 10, 10, 10,  5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [ 0,  0,  0,  5,  5,  0,  0,  0]
]

PSQT_REY_MIDGAME = [
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-30,-40,-40,-50,-50,-40,-40,-30],
    [-20,-30,-30,-40,-40,-30,-30,-20],
    [-10,-20,-20,-20,-20,-20,-20,-10],
    [ 20, 20,  0,  0,  0,  0, 20, 20],
    [ 20, 30, 10,  0,  0, 10, 30, 20]
]

PSQT_REY_ENDGAME = [
    [-50,-40,-30,-20,-20,-30,-40,-50],
    [-30,-20,-10,  0,  0,-10,-20,-30],
    [-30,-10, 20, 30, 30, 20,-10,-30],
    [-30,-10, 30, 40, 40, 30,-10,-30],
    [-30,-10, 30, 40, 40, 30,-10,-30],
    [-30,-10, 20, 30, 30, 20,-10,-30],
    [-30,-30,  0,  0,  0,  0,-30,-30],
    [-50,-30,-30,-30,-30,-30,-30,-50]
]

class IADeAjedrez:
    def __init__(self,max_profundidad: int=3) -> None:
        self.max_profundidad = max_profundidad
        self.color = None
        self.color_enemigo = "blanco" if "negro" == self.color else "negro"
        self.transposition_table: dict[str, float] = {}

    def valor_posicional(self, pieza, fila: int, col: int, fase_juego: str="medio") -> int:
        tablas = {
            "peon": PSQT_PEON,
            "caballo": PSQT_CABALLO,
            "alfil": PSQT_ALFIL,
            "torre": PSQT_TORRE,
            "rey": PSQT_REY_MIDGAME if fase_juego=="medio" else PSQT_REY_ENDGAME,
        }
        tabla = tablas.get(pieza.__class__.__name__, 0)
        if tabla:
            if pieza.color == "blanco":
                return tabla[fila][col]
            else:
                return tabla[7-fila][col] 
        return 0

    def es_paso_final(self, tablero: Tablero) -> bool:
        piezas_totales = sum(1 for fila in tablero.casillas for c in fila if c)
        return piezas_totales <= 14 

    def evaluar_material(self, tablero: Tablero) -> int:
        valor = 0
        for fila in tablero.casillas:
            for pieza in fila:
                if pieza:
                    valor += pieza.valor if pieza.color == self.color else -pieza.valor
        return valor

    def evaluar_posicional(self, tablero: Tablero, fase_juego: str) -> int:
        valor = 0
        for fila in range(8):
            for col in range(8):
                pieza = tablero.casillas[fila][col]
                if pieza:
                    pos_val = self.valor_posicional(pieza, fila, col, fase_juego)
                    if pieza.color == self.color:
                        valor += pos_val
                    else:
                        valor -= pos_val
        return valor

    def movilidad(self, tablero: Tablero, color: str) -> int:
        # Cuenta movimientos legales del jugador para valorar movilidad
        movimientos = self.generar_movimientos(tablero, color)
        return len(movimientos)

    def generar_movimientos(self, tablero:Tablero,color:str)->list:
        """
        Genera todos los movimientos válidos para un jugador de un color dado.

        Parametros:
        -----------
        tablero : Tablero
            El tablero de ajedrez donde se generan los movimientos.
        color : str
            El color del jugador que está por mover.

        Retorna:
        --------
        list
            Una lista de tuplas que contienen la pieza y el movimiento válido generado.
        """
        movimientos = []
        for fila in range(8):
            for col in range(8):
                pieza = tablero.casillas[fila][col]
                if pieza and pieza.color == color:
                    legales = pieza.obtener_movimientos_validos(
                        (fila, col), tablero
                    )
                    for movimiento in legales:
                        movimientos.append(((fila,col),movimiento))
        return movimientos

    def evaluar(self, tablero: Tablero) -> int:
        fase_juego = "final" if self.es_paso_final(tablero) else "medio"

        valor = 0
        valor += self.evaluar_material(tablero)
        valor += self.evaluar_posicional(tablero, fase_juego)

        valor += (self.movilidad(tablero, self.color) - self.movilidad(tablero, self.color_enemigo)) * 10

        return valor

    def valor_pieza_en(casilla: tuple[int, int],tablero:Tablero) -> int:
        pieza = tablero.casillas[casilla[0]][casilla[1]]
        return pieza.valor if pieza else 0

    def alfa_beta(self, tablero:Tablero, profundidad:int, alfa:float, beta:float, maximizando:bool)->float:  
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
        tablero_hash = tablero.generar_hash()

        if (tablero_hash, profundidad, maximizando) in self.transposition_table:
            return self.transposition_table[(tablero_hash, profundidad, maximizando)]
        
        if profundidad == 0:
            evaluacion = self.evaluar(tablero)
            self.transposition_table[(tablero_hash, profundidad, maximizando)] = evaluacion
            return evaluacion

        color = self.color if maximizando else self.color_enemigo
        movimientos = self.generar_movimientos(tablero, color)
        movimientos.sort(key=lambda mov: self.valor_pieza_en(mov[1]), reverse=True) # ordeno movimientos para primero los que pueden eliminar algo de mayor valor para podar mejor los movimientos
        mejor_valor = -INF if maximizando else INF
        
        for origen, movimiento in movimientos:
            tablero.hacer_movimiento(origen, movimiento)
            valor = self.alfa_beta(tablero, profundidad - 1, alfa, beta, not maximizando)
            tablero.deshacer_ultimo_movimiento()
            
            if maximizando:
                mejor_valor = max(mejor_valor, valor)
                alfa = max(alfa, valor)
            else:
                mejor_valor = min(mejor_valor, valor)
                beta = min(beta, valor)
            
            if beta <= alfa:
                break
        self.transposition_table[(tablero_hash, profundidad, maximizando)] = mejor_valor
        return mejor_valor


    def encontrar_mejor_movimiento(self, tablero: Tablero) -> tuple:
        """
        Encuentra el mejor movimiento utilizando el algoritmo de búsqueda Alfa-Beta.

        Parámetros:
        -----------
        tablero : Tablero
            El tablero de ajedrez donde se realizará la búsqueda del mejor movimiento.

        Retorna:
        --------
        tuple
            Devuelve el mejor movimiento encontrado, como una tupla (origen, destino).
            Si no hay movimientos disponibles, devuelve None.
        """
        mejor_valor: float = -INF
        mejor_movimiento: Optional[tuple] = None
        self.transposition_table.clear()
        movimientos = self.generar_movimientos(tablero,self.color)
        self.color_enemigo = "blanco" if "negro" == self.color else "negro"
        if self.es_paso_final(tablero): # Aumenta la profundidad de busqueda en caso de que hayan menos piezas, ya que la respuesta en late game es mas rapida aprovechamos para que sea mas "inteligente"
            profundidad = self.max_profundidad + 1
        else:
            profundidad = self.max_profundidad

        if not movimientos:
            return None 

        for origen, destino in movimientos:

            tablero.hacer_movimiento(origen, destino)

            valor = self.alfa_beta(tablero,profundidad - 1, -INF, INF, False)

            tablero.deshacer_ultimo_movimiento()

            if valor > mejor_valor:
                mejor_valor = valor
                mejor_movimiento = (origen, destino)

        return mejor_movimiento