from foreignai import get_best_move
from fenbit import parse_fen
from movimientos import acumular_movimientos
from negamax import select_best_move


# Recibe fen, opción.

def gestor(fen, opcion):

    match opcion:
        case 1:
            aimove = get_best_move(fen)
        case 2:
            bitmap, turno = parse_fen(fen)
            movimientos = acumular_movimientos(turno, bitmap)
            mejor_movimiento = select_best_move(bitmap, 1)


# FEN - Hecho
# Movimientos - Peones








def numpiezas (fen):
    ...

fen = "8/1B1P2pp/1q3pR1/1p1p3n/7p/4PK2/6R1/r1k5 w - - 0 1"
bitmap, turno, enroques, en_passant = parse_fen(fen)
print(bitmap)
print(turno)

mejor_movimiento = select_best_move(bitmap, 1, turno)
print(mejor_movimiento)


'''
movimientos = acumular_movimientos(bitmap, turno)
print(movimientos)'''