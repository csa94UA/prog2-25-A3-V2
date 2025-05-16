import os
from typing import Dict, List, Optional, Union

from usuario.usuario import Usuario
from juego.sesion_juego import SesionDeJuego # Todavía no implementado :P 
from config import PATH_SOLICITUDES


def _ruta_solicitudes(username: str) -> str: # Se usará una vez se empieze a mandar solicitudes de amistad y aceptarlas
    """
    Devuelve la ruta del archivo de solicitudes del usuario.

    Parámetros:
    -----------
    username : str
        Nombre del usuario.

    Retorna:
    --------
    str
        Ruta completa al archivo de solicitudes.
    """
    return os.path.join(PATH_SOLICITUDES, f"{username}.json")


def mostrar_perfil_amigo(usuario: Usuario, username_amigo: str) -> Dict[str, Union[str, int]]:
    """
    Devuelve el perfil de un amigo, incluyendo nombre de usuario, ELO y cantidad de partidas jugadas.

    Parámetros:
    -----------
    usuario : Usuario
        Usuario actual que consulta el perfil del amigo.
    username_amigo : str
        Nombre de usuario del amigo a consultar.

    Retorna:
    --------
    Dict[str, Union[str, int]]
        Diccionario con información del amigo.

    Lanza:
    ------
    ValueError
        Si el usuario no existe o no es un amigo del usuario actual.
    """
    amigo: Optional[Usuario] = Usuario.cargar_por_username(username_amigo)
    if not amigo:
        raise ValueError("Usuario no encontrado.")

    if amigo.user_id not in usuario.amigos:
        raise ValueError("Este usuario no es tu amigo.")

    return {
        "username": amigo.username,
        "elo": amigo.elo,
        "partidas_jugadas": len(amigo.historial)
    }


def agregar_amigo(usuario: Usuario, username_amigo: str) -> bool:
    """
    Agrega un usuario como amigo de manera mutua si ambos cumplen las condiciones.

    Parámetros:
    -----------
    usuario : Usuario
        Usuario actual que desea agregar un amigo.
    username_amigo : str
        Nombre del usuario que se desea agregar.

    Retorna:
    --------
    bool
        True si se agregó exitosamente, False si hubo algún problema.
    """
    if username_amigo == usuario.username:
        return False

    amigo: Optional[Usuario] = Usuario.cargar_por_username(username_amigo)
    if not amigo:
        return False

    if amigo.user_id in usuario.amigos:
        return False

    usuario.amigos.append(amigo.user_id)
    amigo.amigos.append(usuario.user_id)

    usuario.guardar()
    amigo.guardar()
    return True


def eliminar_amigo(usuario: Usuario, amigo_id: str) -> bool:
    """
    Elimina la amistad entre el usuario actual y otro usuario.

    Parámetros:
    -----------
    usuario : Usuario
        Usuario que quiere eliminar un amigo.
    amigo_id : str
        ID del amigo que se desea eliminar.

    Retorna:
    --------
    bool
        True si se eliminó correctamente, False si no se encontró o no era amigo.
    """
    amigo: Optional[Usuario] = Usuario.cargar(amigo_id)
    if not amigo:
        return False

    if amigo.user_id not in usuario.amigos:
        return False

    usuario.amigos.remove(amigo.user_id)
    if usuario.user_id in amigo.amigos:
        amigo.amigos.remove(usuario.user_id)

    usuario.guardar()
    amigo.guardar()
    return True


def mostrar_amigos(usuario_id: str) -> Dict[str, Union[List[str], str, Dict[str, str]]]:
    """
    Devuelve la lista de amigos de un usuario a partir de su nombre de usuario.

    Parámetros:
    -----------
    usuario_id : str
        Nombre de usuario del usuario que quiere ver su lista de amigos.

    Retorna:
    --------
    Dict[str, Union[List[str], str]]
        Diccionario con la lista de amigos (usernames) o mensaje de error.
    """
    usuario: Optional[Usuario] = Usuario.cargar_por_username(usuario_id)
    if not usuario:
        return {"error": "Usuario no encontrado."}

    if not usuario.amigos:
        return {"amigos": [], "mensaje": "No tienes amigos añadidos."}

    lista_amigos: List[str] = []
    for amigo_id in usuario.amigos:
        datos_amigo: Optional[Usuario] = Usuario.cargar(amigo_id)
        if datos_amigo:
            lista_amigos.append(datos_amigo.username)

    return {"amigos": lista_amigos}
