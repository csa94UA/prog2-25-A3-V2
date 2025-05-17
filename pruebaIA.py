"""
Simula partidas de ajedrez con la IA, ya sea contra un humano o contra otra IA.
"""

from usuario.usuario import Usuario
from juego.usuarioIA import UsuarioIA
from juego.sesion_juego import SesionDeJuego

def simular_partida(ia_vs_ia: bool = True) -> None:
    """
    Simula una partida de ajedrez entre dos jugadores (IA vs IA o Humano vs IA).

    Parámetros:
    -----------
    ia_vs_ia : bool
        Si es True, ambas partes serán jugadas por instancias de IA.
        Si es False, se simula un jugador humano (realmente automático).
    """
    if ia_vs_ia:
        jugador_blanco: Usuario = UsuarioIA.cargar_por_username("IAVicente(3)")
        jugador_negro: Usuario = UsuarioIA.cargar_por_username("IAJulio(2)")


    sesion: SesionDeJuego = SesionDeJuego(jugador_blanco, jugador_negro)

    print("Comenzando partida...\n")

    while not sesion.terminado:
        turno = sesion.turno_actual
        jugador_actual = jugador_blanco if turno == "blanco" else jugador_negro

        print(f"Turno de: {jugador_actual.username} ({turno})")

        if isinstance(jugador_actual, UsuarioIA):
            resultado = sesion.jugar_turno()
        print(resultado.get("msg"))
        if "alerta" in resultado:
            print(">>", resultado["alerta"])
        for x in resultado.get("tablero"):
            print(x)
        if resultado["estado"] == "terminado":
            print("\n== Partida terminada ==")
            print("Ganador:", resultado.get("ganador"))
            print("Archivo guardado:", resultado.get("archivo"))
            break

if __name__ == "__main__":
    simular_partida(ia_vs_ia=True)
