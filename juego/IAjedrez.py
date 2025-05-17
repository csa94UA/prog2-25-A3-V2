   
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
    [ 0,  0,  0,  0,  0,  0,  0,  0]
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

    def color_enemigo(self):
        return "blanco" if "negro" == self.color else "negro"

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
        return piezas_totales <= 12 

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

    def peones_doblados(self, tablero: Tablero, color: str) -> int:
        # Detecta peones doblados en columnas, penaliza
        columnas = {c:0 for c in range(8)}
        for fila in range(8):
            for col in range(8):
                pieza = tablero.casillas[fila][col]
                if pieza and pieza.__class__.__name__ == "peon" and pieza.color == color:
                    columnas[col] += 1
        doblados = sum(1 for c in columnas if columnas[c] > 1)
        return doblados

    def peones_aislados(self, tablero: Tablero, color: str) -> int:
        # Penaliza peones sin peones en columnas adyacentes
        columnas_con_peon = set()
        for fila in range(8):
            for col in range(8):
                p = tablero.casillas[fila][col]
                if p and p.__class__.__name__ == "peon" and p.color == color:
                    columnas_con_peon.add(col)

        aislados = 0
        for c in columnas_con_peon:
            if (c-1 not in columnas_con_peon) and (c+1 not in columnas_con_peon):
                aislados += 1
        return aislados

    def peones_pasados(self, tablero: Tablero, color: str) -> int:
        # Premia peones pasados (no tienen peones enemigos en la misma columna ni adyacentes por delante)
        def tiene_peon_enemigo_adelante(fila, col):
            paso = 1 if color == "blanco" else -1
            for r in range(fila + paso, 8 if color == "blanco" else -1, paso):
                for dc in [-1,0,1]:
                    c = col + dc
                    if 0 <= c < 8:
                        p = tablero.casillas[r][c]
                        if p and p.__class__.__name__ == "peon" and p.color != color:
                            return True
            return False

        pasados = 0
        for fila in range(8):
            for col in range(8):
                p = tablero.casillas[fila][col]
                if p and p.__class__.__name__ == "peon" and p.color == color:
                    if not tiene_peon_enemigo_adelante(fila, col):
                        pasados += 1
        return pasados


    def control_centro(self, tablero: Tablero, color: str) -> int:
        # Premia si el jugador controla el centro (d4,d5,e4,e5)
        centro = [(3,3),(3,4),(4,3),(4,4)]
        valor = 0
        for (f,c) in centro:
            p = tablero.casillas[f][c]
            if p:
                if p.color == color:
                    valor += 20
                else:
                    valor -= 20
        return valor

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
                        (fila, col), tablero, evitar_jaque=True
                    )
                    for movimiento in legales:
                        movimientos.append(((fila,col),movimiento))
        return movimientos

    def evaluar(self, tablero: Tablero) -> int:
        fase_juego = "final" if self.es_paso_final(tablero) else "medio"

        valor = 0
        valor += self.evaluar_material(tablero)
        valor += self.evaluar_posicional(tablero, fase_juego)

        valor += (self.movilidad(tablero, self.color) - self.movilidad(tablero, self.color_enemigo())) * 10
        valor -= (self.peones_doblados(tablero, self.color) - self.peones_doblados(tablero, self.color_enemigo())) * 25
        valor -= (self.peones_aislados(tablero, self.color) - self.peones_aislados(tablero, self.color_enemigo())) * 20
        valor += (self.peones_pasados(tablero, self.color) - self.peones_pasados(tablero, self.color_enemigo())) * 30
        valor += self.control_centro(tablero, self.color)

        return valor


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
        if profundidad == 0:
            return self.evaluar(tablero)
        
        movimientos = self.generar_movimientos(tablero, maximizando)
        mejor_valor = -INF if maximizando else INF
        
        for origen, movimiento in movimientos:
            estado_anterior = tablero.guardar_estado()
            tablero.mover_pieza_tests((origen,movimiento))
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
        return mejor_valor


    def encontrar_mejor_movimiento(self, tablero: Tablero)->tuple:
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
        mejor_valor = -INF
        
        movimientos = self.generar_movimientos(tablero, True)
        
        for origen, movimiento in movimientos:
            estado_anterior = tablero.guardar_estado()
            tablero.mover_pieza_tests((origen,movimiento))
            valor = self.alfa_beta(tablero, self.max_profundidad - 1, -INF, INF, False)
            tablero.restaurar_estado(estado_anterior)
            
            if valor > mejor_valor:
                mejor_valor = valor
                origen_best, movimiento_best = origen, movimiento
        
        return (origen_best, movimiento_best)