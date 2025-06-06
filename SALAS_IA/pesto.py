# Carlos Salas Alarcón

PAWN, KNIGHT, BISHOP, ROOK, QUEEN, KING = 0, 1, 2, 3, 4, 5
mg_value = [82, 337, 365, 477, 1025, 50000000]

# Tablas de bonificación posicional (middlegame)
mg_pesto_table = [
    [  # Peones
        0, 0, 0, 0, 0, 0, 0, 0, 98, 134, 61, 95, 68, 126, 34, -11,
        -6, 7, 26, 31, 65, 56, 25, -20, -14, 13, 6, 21, 23, 12, 17, -23,
        -27, -2, -5, 12, 17, 6, 10, -25, -26, -4, -4, -10, 3, 3, 33, -12,
        -35, -1, -20, -23, -15, 24, 38, -22, 0, 0, 0, 0, 0, 0, 0, 0
    ],
    [  # Caballos
        -167, -89, -34, -49, 61, -97, -15, -107, -73, -41, 72, 36, 23, 62, 7, -17,
        -47, 60, 37, 65, 84, 129, 73, 44, -9, 17, 19, 53, 37, 69, 18, 22,
        -13, 4, 16, 13, 28, 19, 21, -8, -23, -9, 12, 10, 19, 17, 25, -16,
        -29, -53, -12, -3, -1, 18, -14, -19, -105, -21, -58, -33, -17, -28, -19, -23
    ],
    [  # Alfiles
        -29, 4, -82, -37, -25, -42, 7, -8, -26, 16, -18, -13, 30, 59, 18, -47,
        -16, 37, 43, 40, 35, 50, 37, -2, -4, 5, 19, 50, 37, 37, 7, -2,
        -6, 13, 13, 26, 34, 12, 10, 4, 0, 15, 15, 15, 14, 27, 18, 10,
        4, 15, 16, 0, 7, 21, 33, 1, -33, -3, -14, -21, -13, -12, -39, -21
    ],
    [  # Torres
        32, 42, 32, 51, 63, 9, 31, 43, 27, 32, 58, 62, 80, 67, 26, 44,
        -5, 19, 26, 36, 17, 45, 61, 16, -24, -11, 7, 26, 24, 35, -8, -20,
        -36, -26, -12, -1, 9, -7, 6, -23, -45, -25, -16, -17, 3, 0, -5, -33,
        -44, -16, -20, -9, -1, 11, -6, -71, -19, -13, 1, 17, 16, 7, -37, -26
    ],
    [  # Damas
        -28, 0, 29, 12, 59, 44, 43, 45, -24, -39, -5, 1, -16, 57, 28, 54,
        -13, -17, 7, 8, 29, 56, 47, 57, -27, -27, -16, -16, -1, 17, -2, 1,
        -9, -26, -9, -10, -2, -4, 3, -3, -14, 2, -11, -2, -5, 2, 14, 5,
        -35, -8, 11, 2, 8, 15, -3, 1, -1, -18, -9, 10, -15, -25, -31, -50
    ],
    [  # Reyes
        -65, 23, 16, -15, -56, -34, 2, 13, 29, -1, -20, -7, -8, -4, -38, -29,
        -9, 24, 2, -16, -20, 6, 22, -22, -17, -20, -12, -27, -30, -25, -14, -36,
        -49, -1, -27, -39, -46, -44, -33, -51, -14, -14, -22, -46, -44, -30, -15, -27,
        1, 7, -8, -64, -43, -16, 9, 8, -15, 36, 12, -54, 8, -28, 24, 14
    ]
]


def calc_pieza(piece_type, color, square):
    """
    Calcula el valor de una pieza en el medio juego SIN tablas precalculadas.

    Args:
        piece_type (int): Tipo de pieza (PAWN=0, KNIGHT=1, ..., KING=5).
        color (int): WHITE (0) o BLACK (1).
        square (int): Casilla (0-63).

    Returns:
        int: Valor total (base + bonificación).
    """

    # Convertir código a índice (0-5)
    piece_type = abs(piece_type) - 1  # ¡Asume que el bitmap usa 1-6/-1-6!

    # Validar rango
    if piece_type < 0 or piece_type > 5:
        raise ValueError(f"Código de pieza inválido: {piece_type}")

    if color == -1:
        # Espejamos verticalmente la casilla para piezas negras (a1 <-> a8)
        square = square ^ 0x38  # Equivalente a 63 - square - 8 * (square // 8 - 7)

    # Obtenemos el valor base y la bonificación posicional
    base_value = mg_value[piece_type]
    pos_bonus = mg_pesto_table[piece_type][square]

    return base_value + pos_bonus


def calc_tablero(bitmap, color):
    puntuacion = 0
    for i in range(64):
        tipo = bitmap[i]
        if tipo > 0 and color > 0:
            puntuacion += calc_pieza(tipo, color, i)
        elif tipo < 0 and color < 0:
            puntuacion += calc_pieza(tipo, color, i)
        else:
            pass

    return puntuacion

