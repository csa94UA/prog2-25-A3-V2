# Carlos Salas Alarcón
from pesto import calc_pieza, calc_tablero

# Prohibiciones
mov_prohi = [(a, a + 1) for a in range(7, 56, 8)]
mov_prohi = mov_prohi + [(a, a - 1) for a in range(8, 63, 8)]
mov_prohi = mov_prohi + [(a, a + 9) for a in range(7, 65, 8)]
mov_prohi = mov_prohi + [(a, a + 7) for a in range(0, 65, 8)]
mov_prohi = mov_prohi + [(a, a - 9) for a in range(56, 0, -8)]
mov_prohi = mov_prohi + [(a, a - 7) for a in range(63, 0, -8)]
mov_prohi += [(40, 14)]
print('AAAAAAAA', mov_prohi)


# Listas de Movimientos
movs_bpeon = [8, 7, 9]
movs_npeon = [-8,-7,-9]
movs_torre = [-8, -1, 1, 8]
movs_alfil = [-9, -7, 7, 9]
movs_caballo = [-17, -15, -10, -6, 6, 10, 15, 17]
movs_reina = movs_alfil + movs_torre
movs_rey = movs_alfil + movs_torre
bmovs = [0, movs_bpeon, movs_caballo, movs_alfil, movs_torre, movs_reina, movs_rey]
nmovs = [0, movs_rey, movs_reina, movs_torre, movs_alfil, movs_caballo, movs_npeon]
amenaza_rey = movs_alfil + movs_torre + movs_caballo
solo_una = [1,2,6, -1, -2, -6]
print(movs_reina)

# Prohibición Caballo
for a in range(64):
    area = []
    sumas = movs_torre + movs_torre * 2 + movs_alfil + movs_alfil * 2
    for b in sumas:
        area.append(a + b)

    for c in movs_caballo:
        if a + c not in area:
            mov_prohi = mov_prohi + [(a, a - c)]

def acumular_movimientos(bitmap, color):
    movimientos = []
    aliados, enemigos = friend_or_foe(bitmap, color)
    amenaza = hayjaque(bitmap, aliados, enemigos, color)

    print('Amenaza = ', amenaza)

    if amenaza:
        #print('ESTOY AQUIIIIIII')
        if color > 0:
            for i in aliados:
                movimientos += god_save_the_king(bitmap, i, bmovs[bitmap[i]], aliados, enemigos, color)
        else:
            for i in aliados:
                movimientos += god_save_the_king(bitmap, i, nmovs[bitmap[i]], aliados, enemigos, color)
        print('GOD SAVE DA ESTO', movimientos)
        return movimientos
    else:
        print('Modo Papi Guapo Puesto-------------------------------------------------------------------------------------------------------------------------------------------------------------------')
        for i in range(64):
            pieza = bitmap[i]
            if color > 0 and pieza != 0:
                movimientos += movimientos + crear_movimientos(bitmap, i, bmovs[pieza], aliados, enemigos)
            elif color < 0 and pieza != 0:
                movimientos += movimientos + crear_movimientos(bitmap, i, nmovs[pieza], aliados, enemigos)
            else:
                pass
        print('LUCHA LIBRE DA ESTO', movimientos)
        return movimientos

def hayjaque(bitmap, aliados, enemigos, color): # Bien Hecho
    direcciones = amenaza_rey
    if color == -1:
        rey = -6
        movs = bmovs
    else:
        rey = 6
        movs = nmovs

    pos = None
    for i, pieza in enumerate(bitmap):
        if pieza == rey:
            pos = i
            break

    if pos is None:
        raise RuntimeError("se han comido al rey")

    for i in direcciones:
        pos_actual = pos
        pos_ant = pos # Reset before each array
        while True:
            pos_actual += i
            if not (0 <= pos_actual <64):
                break
            if (pos, pos_actual) in mov_prohi or (pos_ant, pos_actual) in mov_prohi:
                break
            if pos_actual in aliados:
                break
            if pos_actual in enemigos and (not (-i in movs[bitmap[pos_actual]]) or (bitmap[pos_actual] in solo_una)):
                break
            if pos_actual in enemigos and -i in movs[bitmap[pos_actual]]:
                print('Me Amenaza: ', pos_actual)
                return 1
            pos_ant = pos_actual

    return 0

def god_save_the_king(bitmap, pos, direcciones, aliados, enemigos, color):
    jugadas = []
    pieza = bitmap[pos]
    print('aliados: ', aliados)
    print('enemigos: ', enemigos)
    for direccion in direcciones:
        pos_actual = pos
        pos_ant = pos
        while True:
            pos_actual += direccion
            if not (0 <= pos_actual < 64):
                break
            elif (pos, pos_actual) in mov_prohi:
                break
            elif (pos_ant, pos_actual) in mov_prohi:
                break
            elif pos_actual in aliados:
                break
            elif pos_actual in enemigos:
                #print('IN DANGER')
                nuevo_tablero = aplicar(bitmap, (pos, pos_actual))
                aliados, enemigos = friend_or_foe(nuevo_tablero, color)
                a = hayjaque(nuevo_tablero, aliados, enemigos, color)
                if a == 0:
                    jugadas = jugadas + [(pos, pos_actual, calc_tablero(nuevo_tablero, color))]
                    break
                else:
                    break
            else:
                #print('MESCAPO')
                if bitmap[pos] in [-1, 1]:
                    break
                nuevo_tablero = aplicar(bitmap, (pos, pos_actual))
                aliados, enemigos = friend_or_foe(nuevo_tablero, color)
                a = hayjaque(nuevo_tablero, aliados, enemigos, color)
                if a == 0:
                    jugadas = jugadas + [(pos, pos_actual, calc_tablero(nuevo_tablero, color))]
                    break

            if pieza in solo_una:
                break
            pos_ant += direccion
    #print('HEMOS CONEGUIDO ESTO: ', jugadas)
    return jugadas

# Crea Movimientos para Cada Pieza
def crear_movimientos(bitmap, pos, direcciones, aliados, enemigos):
    jugadas = []
    pos_ant = 0
    pieza = bitmap[pos]
    color = 1 if pieza > 0 else -1

    for i in direcciones:
        pos_actual = pos
        while True:
            pos_actual += i
            if not (0 <= pos_actual < 64):
                break
            elif (pos, pos_actual) in mov_prohi:
                break
            elif (pos_ant, pos_actual) in mov_prohi:
                break
            elif pos_actual in aliados:
                break
            elif pos_actual in enemigos:
                jugadas = jugadas + [(pos, pos_actual, calc_pieza(bitmap[pos_actual], -color, pos_actual) + (calc_pieza(pieza, color, pos_actual) - calc_pieza(pieza, color, pos)))]
                break
            else:
                if bitmap[pos] in [-1, 1]:
                    break
                jugadas = jugadas + [(pos, pos_actual, calc_pieza(pieza, color, pos_actual) - calc_pieza(pieza, color, pos))]
                pos_ant = pos_actual
            if pieza in solo_una:
                break

    return jugadas

# Funciones que debes implementar según tu estructura
def aplicar(board, move):
    # Crear una copia del tablero para no modificar el original
    new_board = board.copy()
    origen = move[0]
    destino = move[1]
    new_board[destino] = new_board[origen]
    new_board[origen] = 0
    return new_board

def friend_or_foe(bitmap, color):
    aliados = []
    enemigos = []

    if color not in (1, -1):
        raise ValueError("turno must be 1 (white's turn) or -1 (black's turn)")
    if not all(isinstance(num, (int, float)) for num in bitmap):
        raise ValueError("bitmap must contain numbers")

    for i, num in enumerate(bitmap):
        if num * color > 0:
            aliados.append(i)
        elif num * color < 0:
            enemigos.append(i)
    return aliados, enemigos

def enroque(bitmap, aliados, enemigos, color, derechos):
    blresu = [0, 0, 6, 4, 0]
    bcresu = [0, 4, 6, 0]
    nlresu = [0, 0, -6, .4, 0]
    ncresu = [0, -4, -6, 0]
    nuevos_movs = []
    estatus = [False, False, False, False]

    if not True in derechos:
        return nuevos_movs
    if derechos[0] == True:
        blfila = [4, 0, 0, 0, 6]
    else:
        blfila = []
    if derechos[0] == True:
        bcfila = [6, 0, 0, 4]
    else:
        bcfila = []
    if derechos[0] == True:
        nlfila = [-4, 0, 0, 0, -6]
    else:
        nlfila = []
    if derechos[0] == True:
        ncfila = [-6, 0, 0, -4]
    else:
        ncfila = []

    if (bitmap [0:5] == blfila) and (not hayjaque(blresu + bitmap[:5], aliados, enemigos, color)):
        estatus[0] = True
    if bitmap[4:8] == bcfila and (not hayjaque(bitmap[:4] + bcresu + bitmap[8:], aliados, enemigos, color)):
        estatus[1] = True
    if bitmap[56:61] == nlfila and (not hayjaque(bitmap[:56] + nlresu + bitmap[61:], aliados, enemigos, color)):
        estatus[2] = True
    if bitmap[60:64] == ncfila  and (not hayjaque(bitmap[:60] + ncresu, aliados, enemigos, color)):
        estatus[3] = True

    return estatus, nuevos_movs

def en_passant(bitmap, color, atacada):
    jugada = []
    definitivos = []
    if atacada == '-':
        return 0
    if color > 0 and (bitmap[atacada-7] == 1):
        jugada += [(atacada, atacada-7, 100)]
    if color > 0 and (bitmap[atacada-9] ==1):
        jugada += [(atacada, atacada -9, 100)]
    if color < 0 and (bitmap[atacada+7] == 1):
        jugada += [(atacada, atacada+7, 100)]
    if color < 0 and (bitmap[atacada+9] ==1):
        jugada += [(atacada, atacada +9, 100)]
    for i in jugada:
        if not i in mov_prohi:
            definitivos += i

    return definitivos


'''
aliados = []
enemigos = []
turno = 1
bitmap = [0, 0, 0, 0, -2, 0, -6, 0, 6, 0, 1, 0, 0, -2, 0, 5, 1, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 1, 0, 0, 0, 0, -3, 0, 0, 0, 0, 0, -1, -4, -3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

acumular_movimientos(turno, bitmap)
for i, num in enumerate(bitmap):
    if num * turno > 0:
        aliados.append(i)
    elif num * turno < 0:
        enemigos.append(i)

print("alidaos ", aliados)
print('enemigos ', enemigos)


fen = "8/3prb2/P4b2/7p/8/P2B4/K1P2n1Q/4n1k1 b - - 0 1"
'''


