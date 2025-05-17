import bcrypt
from typing import Optional
from usuario.usuario import Usuario
from juego.usuarioIA import UsuarioIA

def hashear_password(password: str) -> str:
    """
    Hashea una contraseña en texto plano utilizando bcrypt.

    Parámetros:
    -----------
    password : str
        Contraseña original del usuario.

    Retorna:
    --------
    str
        Contraseña hasheada lista para almacenar.
    """
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed.decode('utf-8')


def verificar_password(password: str, hashed_password: str) -> bool:
    """
    Verifica una contraseña contra su hash utilizando bcrypt.

    Parámetros:
    -----------
    password : str
        Contraseña ingresada por el usuario.
    hashed_password : str
        Hash almacenado.

    Retorna:
    --------
    bool
        True si coinciden, False en caso contrario.
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))


def registrar_usuario(username: str, password: str) -> Usuario:
    """
    Registra un nuevo usuario si el nombre no está en uso y la contraseña es válida.

    Lanza:
    ------
    ValueError si el nombre ya está  en uso o la contraseña es débil.
    """
    if Usuario.cargar_por_username(username):
        raise ValueError("El nombre de usuario ya está en uso.")

    if len(password) < 8:
        raise ValueError("La contraseña debe tener al menos 8 caracteres.")

    hashed_password: str = hashear_password(password)
    nuevo_usuario: Usuario = Usuario(username=username, password=hashed_password)
    nuevo_usuario.guardar()
    return nuevo_usuario


def iniciar_sesion(username: str, password: str) -> Usuario:
    """
    Inicia sesión validando las credenciales del usuario.

    Lanza:
    ------
    ValueError si el usuario no existe o la contraseña no coincide.
    """
    usuario: Optional[Usuario] = Usuario.cargar_por_username(username)

    if not usuario:
        raise ValueError("Usuario no encontrado.")
    
    if isinstance(usuario, UsuarioIA):
        raise ValueError("Las cuentas de IA no pueden iniciar sesión.")
    
    if not verificar_password(password, usuario.password):
        raise ValueError("Contraseña incorrecta.")

    return usuario


def cerrar_sesion() -> None:
    """
    Simula el cierre de sesión.
    """
    return None
