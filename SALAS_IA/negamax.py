from pesto import calc_tablero
from movimientos import acumular_movimientos, aplicar, enroque
from Zobrist import init_zobrist, update_zobrist, ZobristHistory

from fenbit import bitmap_to_fen

import chess

import chess
import math


# Ejemplo de uso:
# board = chess.Board()
# best = select_best_move(board, 4)
# print(f"Mejor jugada: {best}")


'''
def find_best_move(bitmap, depth, color, castling, ep_file):
    # init hash e historia
    h0 = init_zobrist(bitmap, color, castling, ep_file)
    hist = ZobristHistory(h0)
    best, _ = negamax(bitmap, depth, -float('inf'), float('inf'), color,
                       castling, ep_file, h0, hist)
    return best

MATE_SCORE = 100_000

def negamax(bitmap, depth, alpha, beta, color,
            castling, ep_file, hash_val, hist: ZobristHistory):
    # Terminales y hojas
    moves = acumular_movimientos(bitmap, color)
    if depth == 0:
        return color * calc_tablero(bitmap, color), None
    if not moves:
        return 0, None
    # repetición triple -> tablas
    if hist.is_threefold():
        return 0, None

    best_move = None
    best_score = -float('inf')
    moves.sort(key=lambda x: x[2], reverse=True)
    for mv in moves:
        # mv debe extenderse: from,to,piece,capture,cast_before,cast_after,ep_before,ep_after
        mv = {
            'from_sq': mv[0],
            'to_sq': mv[1],
            'piece': bitmap[mv[0]],
            'capture': bitmap[mv[1]] if bitmap[mv[1]] != 0 else 0,
            'cast_before': castling,
            'cast_after': [False, False, False, False],
            'ep_before': None,
            'ep_after': None
        }
        new_bitmap = aplicar(bitmap, mv)
        # calcula nuevos castling, ep
        new_cast = [False, False, False, False]
        new_ep   = None
        # update hash
        new_hash = update_zobrist(hash_val, mv,
                                  (bitmap, color, castling, ep_file),
                                  (new_bitmap, -color, new_cast, new_ep))
        hist.push(new_hash)

        score, _ = negamax(new_bitmap, depth-1, -beta, -alpha, -color,
                            new_cast, new_ep, new_hash, hist)
        score = -score
        hist.pop()

        if score > best_score:
            best_score = score
            best_move = mv
        alpha = max(alpha, score)
        if alpha >= beta:
            break

    return best_score, best_move


# Función principal para encontrar el mejor movimiento
def find_best_move(bitmap, depth, color):
    best_move = None
    best_value = -float('inf')
    alpha = -float('inf')
    beta = float('inf')

    movimientos = acumular_movimientos(bitmap, color)
    if len(movimientos) == 1:
        return movimientos[0]

    # Ordenar movimientos por puntuación (mejores primero para pruning)
    movimientos.sort(key=lambda x: x[2], reverse=True)

    for move in movimientos:
        # Generar nueva posición aplicando el movimiento
        n_table = aplicar(bitmap, move)
        # Llamar a negamax recursivamente
        value = -negamax(n_table, depth - 1, -beta, -alpha, -color)
        # Actualizar mejor movimiento
        if value > best_value:
            best_value = value
            best_move = move

        # Actualizar alpha
        alpha = max(alpha, value)
        if alpha >= beta:
            break  # Poda beta

    return best_move, best_value


# Algoritmo Negamax básico con poda alpha-beta
def negamax(board, depth, alpha, beta, color):
    print('DEPTH =======', depth)
    best_value = -float('inf') # El Mejor valor se Incializa como Infinito
    legal_moves = acumular_movimientos(board, color) # Generar Movimientos Legales
    legal_moves.sort(key=lambda x: x[2], reverse=True) # Ordenarolos

    # Condición de terminación
    if depth <= 0:
        print('Finsihed')
        return color * calc_tablero(board, color)
    if not legal_moves:
        return 0

    for move in legal_moves: # Para cada Movimiento
        new_board = aplicar(board, move) # Aplicar Movimiento
        value = -negamax(new_board, depth - 1, -beta, -alpha, -color)

        best_value = max(best_value, value)
        alpha = max(alpha, value)

        if alpha >= beta:
            break  # Poda

    return best_value

MATE_SCORE = 100_000


def is_terminal(board):
    tablero = bitmap_to_fen(board)
    try:
        board = chess.Board(tablero)
    except ValueError:
        raise ValueError("Posición inválida generada desde el bitmap")

        # Verificar condiciones terminales
    return any([
        board.is_checkmate(),  # Jaque mate
        board.is_stalemate(),  # Ahogado
        board.is_insufficient_material(),  # Material insuficiente
        board.is_seventyfive_moves(),  # Regla de 75 movimientos
        board.is_fivefold_repetition()  # Repetición 5 veces
    ])
'''