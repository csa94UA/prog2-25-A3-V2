def calcular_elo(
    elo_ganador: int,
    elo_perdedor: int,
    resultado: float,
    k: int = 48
) -> int:
    """
    Calcula el cambio en el puntaje ELO para un jugador después de una partida.

    Parámetros:
    -----------
    elo_ganador : int
        ELO actual del jugador cuya variación se va a calcular.
    elo_perdedor : int
        ELO del oponente.
    resultado : float
        Resultado de la partida :
        - 1.0 si ganó
        - 0.5 si fue empate
        - 0 si perdió
    k : int, opcional
        Constante de ajuste del sistema ELO. Por defecto es 48.

    Retorna:
    --------
    int
        El cambio de elo (esto se sumaría al ganador y restaría al perdedor).
    """
    # Probabilidad esperada de victoria para el jugador
    esperado_ganador = 1 / (1 + 10 ** ((elo_perdedor - elo_ganador) / 400))

    # Cambio de ELO basado en el resultado real y esperado
    cambio_ganador = k * (resultado - esperado_ganador)

    return int(round(cambio_ganador))
