'''
Inteligencia Artificial

Parte Indiscutible:
- Recibe un FEN
- Saca un FEN

Mejoras:
- Lo Sanitaze con la libreria Chess tanto al principio como a la salida.

Flujo de Inteligencia:
 1ª Opción: Se juega una partida integra contra Stockfish. Cero complicaciones. - ESTÁ (NO CONECTADO).

 2ª Opción: Algoritmo de la Casa
    - La IA elige un movimiento inicial aleatorio. - NO ESTÁ
    - Activamos MinMax o Nega-Max para que elijan la mejor opción. - IDK
    - Se delega la búsqueda a Alpha-Beta para mayor eficiencia. - ESTÁ (NO SE SABE ESTADO)
    - Hacemos que influyan los PeSTOs. - ESTÁ (NO CONECTADO)
    - Cuando haya 7 piezas en el Tablero, la API con Lichess toma control. ESTÁ (NO CONECTADO)

 3ª Sistema de ELO:
    - Se compara como juega el usuario con stockfish y se le calcula un ELO fruto de esta comparación.

FUNCIONAMIENTO ALPHA-BETA

El Valor será el peso de cada pieza por el valor de su nueva posición. (ENCONTRAREMOS PROPORCIÓN)

Iterative Deepening

Archivos:
- mainai. - 49
- Fenbit - 65
- pesto - 78
- movimientos 99
- negamax,- 82
- foreignai - 30
- Lichess - 71


ORDEN
BITMAP >>> POSICIÓN >>> Direcciones >>> Aliados >>> Enemigos >>> Color


'''