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
            fen = fen[1:]
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
    board_part, turn, enroques, en_passant = parts[0], parts[1], parts[2], parts[3]

    # Usamos tu función existente para construir el tablero
    bitmap = fen_to_bitmap(fen)

    # Convertimos 'w'/'b' a +1/-1
    color = +1 if turn == 'w' else -1

    return bitmap, color, enroques, en_passant

def copy_bitmap(bitmap):
    return list(bitmap)


def bitmap_to_fen(bitmap):
    reversed_piece_map = {
        v: k for k, v in {
            'P': 1, 'N': 2, 'B': 3, 'R': 4, 'Q': 5, 'K': 6,
            'p': -1, 'n': -2, 'b': -3, 'r': -4, 'q': -5, 'k': -6
        }.items()
    }

    fen_rows = []
    for row in range(7, -1, -1):  # Filas de 8th a 1st (como en FEN)
        fen_row = []
        empty = 0
        for col in range(8):
            piece_code = bitmap[row * 8 + col]
            if piece_code == 0:
                empty += 1
            else:
                if empty > 0:
                    fen_row.append(str(empty))
                    empty = 0
                fen_row.append(reversed_piece_map[piece_code])
        if empty > 0:
            fen_row.append(str(empty))
        fen_rows.append(''.join(fen_row))

    return '/'.join(fen_rows) + ' w - - 0 1'  # Asume turno blanco y otros campos básicos