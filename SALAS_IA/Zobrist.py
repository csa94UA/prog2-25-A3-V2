'''
new_bitmap = aplicar(bitmap, move)
new_hash   = update_zobrist(current_hash, move, before_info, after_info)
hist.push(new_hash)
if hist.is_repetition():
    score = 0   # tablas
else:
    score = -negamax(new_bitmap, depth-1, -beta, -alpha, -color, new_hash, hist)
hist.pop()
'''

# File: zobrist.py
# Módulo para Zobrist hashing y detección de repeticiones
import random

# Constantes de tablero
PIEZAS = [1,2,3,4,5,6,  -1,-2,-3,-4,-5,-6]  # códigos de piezas en tu bitmap
CASILLAS = 64
# Castling rights: usaremos 4 bits (K, Q, k, q)
# En passant: 8 columnas + 1 para "no ep"
MAX_CASTLING = 4
MAX_EP = 9

# 1) Inicializar tablas Zobrist aleatorias
table_piece = {
    pieza: [random.getrandbits(64) for _ in range(CASILLAS)]
    for pieza in PIEZAS
}
table_color = random.getrandbits(64)
table_castling = [random.getrandbits(64) for _ in range(MAX_CASTLING)]
table_ep = [random.getrandbits(64) for _ in range(MAX_EP)]

# 2) Init hash desde bitmap y estado auxiliar

def init_zobrist(bitmap, color_to_move, castling_rights, ep_file):
    """
    bitmap: lista de 64 ints de pieza (0 vacío o ± código)
    color_to_move: +1 o -1
    castling_rights: tuplas/bool de (K,Q,k,q)
    ep_file: 0-7 fila ep o None
    """
    h = 0
    # piezas
    for sq, pc in enumerate(bitmap):
        if pc != 0:
            h ^= table_piece[pc][sq]
    # color
    if color_to_move < 0:
        h ^= table_color
    # castling
    for i, ok in enumerate(castling_rights):
        if ok:
            h ^= table_castling[i]
    # en passant
    idx = ep_file if ep_file is not None else MAX_EP - 1
    h ^= table_ep[idx]
    return h

# 3) Update hash tras un movimiento
def update_zobrist(prev_hash, move, before, after):
    """
    move: (from_sq, to_sq, piece, capture_piece, prev_castle, new_castle, prev_ep, new_ep)
    before/after: tuplas de (bitmap, color_to_move, castling_rights, ep_file)
    """
    h = prev_hash
    from_sq, to_sq, pc, cap_pc, cast_before, cast_after, ep_before, ep_after = move
    # remover pieza origen
    h ^= table_piece[pc][from_sq]
    # añadir pieza destino
    h ^= table_piece[pc][to_sq]
    # captura
    if cap_pc != 0:
        h ^= table_piece[cap_pc][to_sq]
    # castling rights changed
    for i in range(MAX_CASTLING):
        if cast_before[i] != cast_after[i]:
            h ^= table_castling[i]
    # ep
    idx_b = ep_before if ep_before is not None else MAX_EP-1
    idx_a = ep_after  if ep_after  is not None else MAX_EP-1
    if idx_b != idx_a:
        h ^= table_ep[idx_b]
        h ^= table_ep[idx_a]
    # color flip
    h ^= table_color
    return h

# 4) Historial de hashes
type_alias = int

class ZobristHistory:
    def __init__(self, initial_hash: type_alias):
        self.history = [initial_hash]
        self.counts = {initial_hash: 1}

    def push(self, h: type_alias):
        self.history.append(h)
        self.counts[h] = self.counts.get(h, 0) + 1

    def pop(self):
        h = self.history.pop()
        self.counts[h] -= 1
        if self.counts[h] == 0:
            del self.counts[h]

    def is_threefold(self) -> bool:
        h = self.history[-1]
        return self.counts.get(h, 0) >= 3
