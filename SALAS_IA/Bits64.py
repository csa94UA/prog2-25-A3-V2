def fen_to_bitmap(fen):
    # Mapeo de caracteres FEN a valores numéricos
    piece_map = {
        'P': 1, 'N': 2, 'B': 3, 'R': 4, 'Q': 5, 'K': 6,
        'p': -1, 'n': -2, 'b': -3, 'r': -4, 'q': -5, 'k': -6
    }

    # Extraer la parte del tablero del FEN (antes del primer espacio)
    board_part = fen.split()[0]

    bitmap = [0] * 64  # Array unidimensional de 64 ceros

    row = 0  # Fila actual (0 = primera fila, 7 = última)
    col = 0  # Columna actual (0 = a, 7 = h)

    for char in board_part:
        if char == '/':
            # Nueva fila
            row += 1
            col = 0
        elif char.isdigit():
            # Espacios vacíos (avanzar columnas)
            col += int(char)
        else:
            # Pieza: asignar valor al bitmap
            index = row * 8 + col
            bitmap[index] = piece_map[char]
            col += 1

    return bitmap  # Devuelve un array de 1x64


# Ejemplo de uso
fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
bitmap = fen_to_bitmap(fen)

# Mostrar el array de 64 elementos
print(bitmap)


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


def get_sliding_moves(bitmap, index, directions):
    moves = []
    piece = bitmap[index]
    color = 1 if piece > 0 else -1
    for delta in directions:
        new_pos = index + delta
        while True:
            if new_pos < 0 or new_pos >= 64:
                break
            # Validar movimiento horizontal (misma fila)
            if abs(delta) == 1 and (new_pos // 8 != index // 8):
                break
            # Validar movimiento vertical (misma columna)
            if abs(delta) == 8 and (new_pos % 8 != index % 8):
                break
            target = bitmap[new_pos]
            if target == 0:
                moves.append(new_pos)
            else:
                if (color == 1 and target < 0) or (color == -1 and target > 0):
                    moves.append(new_pos)
                break
            new_pos += delta
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


# --- Ejemplo de uso ---
fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
bitmap = fen_to_bitmap(fen)

# Movimientos de la torre blanca en a1 (index 56)
rook_moves = get_rook_moves(bitmap, 56)
print(f"Movimientos de la torre en a1: {rook_moves}")  # Output: [] (no puede moverse)

# Movimientos del caballo negro en b8 (index 1)
knight_moves = get_knight_moves(bitmap, 1)
print(f"Movimientos del caballo en b8: {knight_moves}")  # Output: [16, 18]

###### TERCERA ADICIÓN

def copy_bitmap(bitmap):
    return list(bitmap)

def get_king_position(bitmap, color):
    king = 6 if color == 'white' else -6
    for i in range(64):
        if bitmap[i] == king:
            return i
    return -1

def is_in_check(bitmap, color):
    king_pos = get_king_position(bitmap, color)
    if king_pos == -1:
        return False
    opponent = 'black' if color == 'white' else 'white'
    for i in range(64):
        piece = bitmap[i]
        if piece == 0 or (color == 'white' and piece < 0) or (color == 'black' and piece > 0):
            continue
        moves = []
        if abs(piece) == 1:  # Peón (ataques)
            dirs = [-7, -9] if piece > 0 else [7, 9]
            for d in dirs:
                pos = i + d
                if 0 <= pos < 64 and (pos // 8 == (i // 8) + (-1 if piece > 0 else 1)):
                    moves.append(pos)
        elif abs(piece) == 2:  # Caballo
            moves = [i + d for d in [-17, -15, -10, -6, 6, 10, 15, 17] if 0 <= i + d < 64]
        elif abs(piece) == 3:  # Alfil
            for d in [-9, -7, 7, 9]:
                pos = i
                while True:
                    pos += d
                    if not (0 <= pos < 64) or (pos % 8 - (pos - d) % 8 not in [-1, 1]):
                        break
                    moves.append(pos)
                    if bitmap[pos] != 0:
                        break
        elif abs(piece) == 4:  # Torre
            for d in [-8, -1, 1, 8]:
                pos = i
                while True:
                    pos += d
                    if not (0 <= pos < 64) or (abs((pos % 8) - (i % 8)) not in [0, 1] if d in [-1, 1] else True):
                        break
                    moves.append(pos)
                    if bitmap[pos] != 0:
                        break
        elif abs(piece) == 5:  # Reina (combinación de torre y alfil)
            moves = []
            for d in [-9, -7, 7, 9, -8, -1, 1, 8]:
                pos = i
                while True:
                    pos += d
                    if not (0 <= pos < 64) or (d in [-1, 1] and (pos // 8 != i // 8)) or (d in [-8, 8] and (pos % 8 != i % 8)):
                        break
                    moves.append(pos)
                    if bitmap[pos] != 0:
                        break
        elif abs(piece) == 6:  # Rey
            moves = [i + d for d in [-9, -8, -7, -1, 1, 7, 8, 9] if 0 <= i + d < 64]
        if king_pos in moves:
            return True
    return False

def generate_pseudo_legal_moves(bitmap, color):
    moves = []
    for i in range(64):
        piece = bitmap[i]
        if piece == 0 or (color == 'white' and piece < 0) or (color == 'black' and piece > 0):
            continue
        if abs(piece) == 1:  # Peón
            dir = -8 if color == 'white' else 8
            if 0 <= i + dir < 64 and bitmap[i + dir] == 0:
                moves.append((i, i + dir))
                # Doble paso inicial
                if (color == 'white' and i // 8 == 6) or (color == 'black' and i // 8 == 1):
                    if bitmap[i + 2 * dir] == 0:
                        moves.append((i, i + 2 * dir))
            # Capturas
            for delta in [-1, 1]:
                target = i + dir + delta
                if 0 <= target < 64 and (target // 8 == (i // 8) + (-1 if color == 'white' else 1)):
                    if bitmap[target] != 0 and ((color == 'white' and bitmap[target] < 0) or (color == 'black' and bitmap[target] > 0)):
                        moves.append((i, target))
        elif abs(piece) == 2:  # Caballo
            offsets = [-17, -15, -10, -6, 6, 10, 15, 17]
            for d in offsets:
                target = i + d
                if 0 <= target < 64 and (bitmap[target] == 0 or (color == 'white' and bitmap[target] < 0) or (color == 'black' and bitmap[target] > 0)):
                    moves.append((i, target))
        elif abs(piece) == 3:  # Alfil
            for d in [-9, -7, 7, 9]:
                target = i
                while True:
                    target += d
                    if not (0 <= target < 64) or (abs((target % 8) - (i % 8)) != 1):
                        break
                    if bitmap[target] == 0:
                        moves.append((i, target))
                    else:
                        if (color == 'white' and bitmap[target] < 0) or (color == 'black' and bitmap[target] > 0):
                            moves.append((i, target))
                        break
        elif abs(piece) == 4:  # Torre
            for d in [-8, -1, 1, 8]:
                target = i
                while True:
                    target += d
                    if not (0 <= target < 64) or (d in [-1, 1] and (target // 8 != i // 8)):
                        break
                    if bitmap[target] == 0:
                        moves.append((i, target))
                    else:
                        if (color == 'white' and bitmap[target] < 0) or (color == 'black' and bitmap[target] > 0):
                            moves.append((i, target))
                        break
        elif abs(piece) == 5:  # Reina
            for d in [-9, -7, 7, 9, -8, -1, 1, 8]:
                target = i
                while True:
                    target += d
                    if not (0 <= target < 64) or (d in [-1, 1] and (target // 8 != i // 8)):
                        break
                    if bitmap[target] == 0:
                        moves.append((i, target))
                    else:
                        if (color == 'white' and bitmap[target] < 0) or (color == 'black' and bitmap[target] > 0):
                            moves.append((i, target))
                        break
        elif abs(piece) == 6:  # Rey
            for d in [-9, -8, -7, -1, 1, 7, 8, 9]:
                target = i + d
                if 0 <= target < 64 and (abs((target % 8) - (i % 8)) <= 1):
                    if (color == 'white' and bitmap[target] <= 0) or (color == 'black' and bitmap[target] >= 0):
                        moves.append((i, target))
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

# Ejemplo de uso
fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
bitmap = fen_to_bitmap(fen)
legal_moves = generate_legal_moves(bitmap, 'white')

print(f"Número de movimientos legales iniciales: {len(legal_moves)}")


