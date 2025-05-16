import uuid

def generar_id() -> str:
    """
    Genera un identificador único universal (UUID) en formato de cadena.

    Utiliza la función uuid4() para crear un UUID aleatorio,
    útil para identificar usuarios.

    Retorna:
    --------
    str
        UUID generado como cadena.
    """
    return str(uuid.uuid4())
