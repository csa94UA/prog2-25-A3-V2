from movimientos import hayjaque



bitmap = [0, 0, 0, 0, -2, 0, -6, 0, 6, 0, 1, 0, 0, -2, 0, 5, 1, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, 1, 0, 0, 0, 0, -3, 0, 0, 0, 0, 0, -1, -4, -3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

aliados = [8, 10, 15, 16, 19, 40]
enemigos =  [4, 6, 13, 39, 45, 51, 52, 53]
color = 1

resultado = hayjaque(bitmap, aliados, enemigos, color)

print(resultado)