

class Tablero:

    def __init__(self):
        #Inicializa una matriz de orden 8 con clases Casilla
        self.tablero = [[Casilla(i,j) for i in range(8)] for j in range(8)]

    def ocupado(self, fila : int, columna : int) -> bool:

        return self.tablero[fila][columna].ocupado

    def limite(self, fila : int, columna : int) -> bool:

        if fila < 8 and fila >= 0 and columna < 8 and columna >= 0:
            return True

        return False

    def jaque_in(self, fila : int, columna : int, jugador : Jugador):

        #Pridmero comprobamos todas las casillas amenazadoras

        casillas_amenazadas = tablero[fila,columna].amenazas()

        #Esto es para el caso especial del caballo ya que puede saltar sobre piezas

        caballo = [(1,2),(1,-2),(2,1),(2,-1),(-1,2),(-1,-2),(-2,1),(-2,-1)]

        for fila, columna in caballo
            if not tablero.ocupado(fila, columna):
                casillas_amenazadas.append(tuple(fila, columna))

        for pieza in Jugador.piezas:
            fila, columna = pieza.posicion
            for mov in pieza.movimiento_valido(fila, columna):
                if mov in casillas_amenazadas:
                    quitar_permutaciones(mov,casillas_amenazadas)

        if casillas_amenazadas = []:
            return False

        return False


