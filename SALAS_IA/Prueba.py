from pesto import *


WHITE = +1
BLACK = -1


def fen_to_bitmap(fen):
    piece_map = {
        'P': 1, 'N': 2, 'B': 3, 'R': 4, 'Q': 5, 'K': 6,
        'p': -1, 'n': -2, 'b': -3, 'r': -4, 'q': -5, 'k': -6
    }
    board_part = fen.split()[0]
    bitmap = [0] * 64
    row, col = 7, 0
    for char in board_part:
        if char == '/':
            row -= 1
            col = 0
        elif char.isdigit():
            col += int(char)
        else:
            bitmap[row * 8 + col] = piece_map[char]
            col += 1
    return bitmap

def parse_fen(fen):
    """
    Devuelve (bitmap, color_to_move) donde color_to_move es +1 para blancas, -1 para negras.
    """
    parts = fen.split()
    board_part, turn = parts[0], parts[1]

    # Usamos tu función existente para construir el tablero
    bitmap = fen_to_bitmap(fen)

    # Convertimos 'w'/'b' a +1/-1
    color = +1 if turn == 'w' else -1

    return bitmap, color


def copy_bitmap(bitmap):
    return list(bitmap)

# Hecho
def get_king_position(bitmap, color):
    king = 6 if color == 'white' else -6
    for i in range(64):
        if bitmap[i] == king:
            return i
    return -1

def get_sliding_moves(bitmap, index, directions):
    moves = []
    piece = bitmap[index]
    color = 1 if piece > 0 else -1

    for delta in directions:
        current_pos = index
        while True:
            current_pos += delta
            if not (0 <= current_pos < 64):
                break

            # Calcular diferencias de fila y columna
            prev_row = (current_pos - delta) // 8
            prev_col = (current_pos - delta) % 8
            new_row = current_pos // 8
            new_col = current_pos % 8

            # Validar movimiento horizontal/vertical
            if abs(delta) == 1:  # Horizontal
                if new_row != prev_row: break
            elif abs(delta) == 8:  # Vertical
                if new_col != prev_col: break
            else:  # Diagonal
                row_diff = abs(new_row - prev_row)
                col_diff = abs(new_col - prev_col)
                if row_diff != 1 or col_diff != 1: break

            target = bitmap[current_pos]
            if target == 0:
                moves.append(current_pos)
            else:
                if (color == 1 and target < 0) or (color == -1 and target > 0):
                    moves.append(current_pos)
                break
    return moves

def get_pawn_moves(bitmap, index):
    moves = []
    piece = bitmap[index]
    if piece not in [1, -1]:  # 1 = peón blanco, -1 = peón negro
        return moves

    color = 1 if piece == 1 else -1
    row = index // 8
    col = index % 8

    # Dirección de avance (blancas: hacia arriba, negras: hacia abajo)
    direction = -8 if color == 1 else 8

    # Movimiento hacia adelante 1 casilla
    forward = index + direction
    if 0 <= forward < 64 and bitmap[forward] == 0:
        moves.append(forward)
        # Movimiento de 2 casillas desde posición inicial
        if (row == 6 and color == 1) or (row == 1 and color == -1):
            double_forward = forward + direction
            if bitmap[double_forward] == 0:
                moves.append(double_forward)

    # Capturas diagonales
    for delta in [-1, 1]:
        capture_pos = index + direction + delta
        if 0 <= capture_pos < 64:
            # Verificar misma fila (evitar bordes)
            if (capture_pos // 8) == (forward // 8):
                target = bitmap[capture_pos]
                if target != 0 and ((color == 1 and target < 0) or (color == -1 and target > 0)):
                    moves.append(capture_pos)

    return moves


def get_knight_moves(bitmap, index):
    moves = []
    piece = bitmap[index]
    if piece not in [2, -2]:  # 2 = caballo blanco, -2 = negro
        return moves

    color = 1 if piece > 0 else -1
    # Movimientos en L (±1 y ±2 combinados)
    offsets = [-17, -15, -10, -6, 6, 10, 15, 17]
    for offset in offsets:
        new_pos = index + offset
        if 0 <= new_pos < 64:
            # Validar que el movimiento no cruce bordes (ej: de columna 0 a 7)
            current_col = index % 8
            new_col = new_pos % 8
            if abs(current_col - new_col) <= 2:
                target = bitmap[new_pos]
                if target == 0 or ((color == 1 and target < 0) or (color == -1 and target > 0)):
                    moves.append(new_pos)
    return moves


def get_king_moves(bitmap, index):
    moves = []
    piece = bitmap[index]
    if piece not in [6, -6]:  # 6 = rey blanco, -6 = negro
        return moves

    color = 1 if piece > 0 else -1
    # Movimientos adyacentes (±1, ±7, ±8, ±9)
    offsets = [-9, -8, -7, -1, 1, 7, 8, 9]
    for offset in offsets:
        new_pos = index + offset
        if 0 <= new_pos < 64:
            # Validar que no se salte columnas (ej: de columna 0 a 7)
            current_col = index % 8
            new_col = new_pos % 8
            if abs(current_col - new_col) <= 1:
                target = bitmap[new_pos]
                if target == 0 or ((color == 1 and target < 0) or (color == -1 and target > 0)):
                    moves.append(new_pos)
    return moves


def get_bishop_moves(bitmap, index):
    # Movimientos diagonales (±7, ±9)
    return get_sliding_moves(bitmap, index, [-9, -7, 7, 9])

def get_rook_moves(bitmap, index):
    # Movimientos rectos (±1, ±8)
    return get_sliding_moves(bitmap, index, [-8, -1, 1, 8])

def get_queen_moves(bitmap, index):
    # Combinación de torre y alfil
    return get_rook_moves(bitmap, index) + get_bishop_moves(bitmap, index)

# Funciones de movimiento para cada pieza (las mismas que antes)
# ... [Las funciones get_pawn_moves, get_knight_moves, etc. permanecen iguales] ...

# Función mejorada para detectar jaque
def is_in_check(bitmap, color):
    king_pos = get_king_position(bitmap, color)
    if king_pos == -1:
        return False  # No hay rey: no en jaque

    for i in range(64):
        piece = bitmap[i]
        if piece == 0 or (color == 1 and piece < 0) or (color == -1 and piece > 0):
            continue

        if abs(piece) == 1:  # Peón
            attack_dirs = [-9, -7] if piece > 0 else [7, 9]
            for d in attack_dirs:
                target = i + d
                if 0 <= target < 64:
                    if abs((i % 8) - (target % 8)) == 1 and target == king_pos:
                        return True
        elif abs(piece) == 2:  # Caballo
            if king_pos in get_knight_moves(bitmap, i):
                return True
        elif abs(piece) in [3, 4, 5]:  # Alfil, Torre, Reina
            moves = []
            if abs(piece) == 3:
                moves = get_bishop_moves(bitmap, i)
            elif abs(piece) == 4:
                moves = get_rook_moves(bitmap, i)
            else:
                moves = get_queen_moves(bitmap, i)
            if king_pos in moves:
                return True
        elif abs(piece) == 6:  # Rey
            if king_pos in get_king_moves(bitmap, i):
                return True
    return False


def generate_pseudo_legal_moves(bitmap, color):
    """
    Genera movimientos pseudolegales para todas las piezas en el bitmap.
    Utiliza las funciones get_<piece>_moves ya definidas para cada tipo.
    Devuelve una lista de tuplas (origen, destino).
    """
    moves = []
    for i, piece in enumerate(bitmap):
        # Saltar casillas vacías y piezas del bando contrario
        if piece == 0:
            continue
        if color == 1 and piece < 0:
            continue
        if color == -1 and piece > 0:
            continue

        # Obtener movimientos según el tipo de pieza
        abs_piece = abs(piece)
        if abs_piece == 1:  # Peón
            for dest in get_pawn_moves(bitmap, i):
                moves.append((i, dest))
        elif abs_piece == 2:  # Caballo
            for dest in get_knight_moves(bitmap, i):
                moves.append((i, dest))
        elif abs_piece == 3:  # Alfil
            for dest in get_bishop_moves(bitmap, i):
                moves.append((i, dest))
        elif abs_piece == 4:  # Torre
            for dest in get_rook_moves(bitmap, i):
                moves.append((i, dest))
        elif abs_piece == 5:  # Reina
            # Combina movimientos de torre y alfil
            for dest in get_rook_moves(bitmap, i):
                moves.append((i, dest))
            for dest in get_bishop_moves(bitmap, i):
                moves.append((i, dest))
        elif abs_piece == 6:  # Rey
            for dest in get_king_moves(bitmap, i):
                moves.append((i, dest))

    return moves

def generate_legal_moves(bitmap, color):
    pseudo_legal = generate_pseudo_legal_moves(bitmap, color)
    legal_moves = []
    for (start, end) in pseudo_legal:
        new_bitmap = copy_bitmap(bitmap)
        new_bitmap[end] = new_bitmap[start]
        new_bitmap[start] = 0
        if not is_in_check(new_bitmap, color):
            legal_moves.append((start, end))
    return legal_moves

### Algoritmos
# Valor grande para representar mate
MATE_SCORE = 100_000

def negamax(board, depth, color, alpha, beta):
    if depth == 0:
        return evaluate(board, color), None

    side = WHITE if color == +1 else BLACK
    legal_moves = generate_legal_moves(board, color)

    # ←———— Inserta aquí el chequeo de mate/ahogado ————
    if not legal_moves:
        if is_in_check(board, color):
            # Jaque mate: valor muy bajo, restamos depth para preferir mates rápidos
            return -MATE_SCORE - depth, None
        else:
            # Ahogado: tablas → valoración neutra
            return 0, None
    # ——————————————————————————————————————————————

    best_move = None
    max_score = -float('inf')

    for move in legal_moves:
        new_board = make_move(board, move)
        sc, _ = negamax(new_board, depth - 1, -color, -beta, -alpha)
        score = -sc

        if score > max_score:
            max_score, best_move = score, move
            alpha = max(alpha, score)
            if alpha >= beta:
                break

    return max_score, best_move

def make_move(board, move):
    new_board = board.copy()
    start, end = move
    new_board[end] = new_board[start]
    new_board[start] = 0
    return new_board


def find_best_move(board, color, depth=3):
    score, best_move = negamax(board, depth, color, -float('inf'), float('inf'))
    return best_move


# PeSTO Initialization and Evaluation
# PeSTO Initialization and Evaluation

PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING = range(6)
WHITE, BLACK = +1, -1

# Midgame and endgame base values
mg_value = [82, 337, 365, 477, 1025, 0]
eg_value = [94, 281, 297, 512, 936, 0]

# PeSTO tables for each piece type (0..5)
mg_pesto = [mg_pawn_table, mg_knight_table, mg_bishop_table,
            mg_rook_table, mg_queen_table, mg_king_table]
eg_pesto = [eg_pawn_table, eg_knight_table, eg_bishop_table,
            eg_rook_table, eg_queen_table, eg_king_table]


def evaluate(bitmap, color):
    """
    Evaluación PeSTO combinada (negamax perspective).

    - bitmap: lista de 64 ints, piezas blancas > 0, negras < 0 (valores ±1..±6).
    - color: +1 para blancas al mover, -1 para negras.

    Devuelve un entero, mayor = mejor para quien mueva (color).
    """
    mg_score = 0
    eg_score = 0
    phase = 0

    max_phase = 24
    for sq, pc in enumerate(bitmap):
        if pc == 0:
            continue
        idx = abs(pc) - 1  # 0..5 index into tables
        if pc > 0:
            # White piece: normal table
            mg_score += mg_value[idx] + mg_pesto[idx][sq]
            eg_score += eg_value[idx] + eg_pesto[idx][sq]
        else:
            # Black piece: mirrored square
            flip_sq = sq ^ 56
            mg_score -= mg_value[idx] + mg_pesto[idx][flip_sq]
            eg_score -= eg_value[idx] + eg_pesto[idx][flip_sq]
        phase += [0,0,1,1,1,1][idx]

    # Blend midgame and endgame
    phase = min(phase, max_phase)
    total = (mg_score * phase + eg_score * (max_phase - phase)) // max_phase

    # Perspective: si es turno negro, invertir signo
    return total * color

if __name__ == "__main__":
    init_tables()
    fen = "b7/PnK4p/8/4Q1N1/1p2p1p1/pp3p2/8/B4k1q w - - 0 1"

    bitmap, color = parse_fen(fen)
    best_move = find_best_move(bitmap, color, 3)

    print(f"Mejor movimiento: {best_move}")

