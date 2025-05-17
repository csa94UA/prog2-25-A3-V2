from typing import Any, Dict,Optional
import os
import json

from usuario.usuario import Usuario
from juego.IAjedrez import IADeAjedrez
from config import PATH_USUARIOS                 # Ruta donde se guardan los archivos de usuario


class UsuarioIA(Usuario):
    """
    Subclase de Usuario que representa una inteligencia artificial (IA) que juega ajedrez.
    Esta clase permite que la IA actúe como un jugador dentro del sistema, con ELO, historial
    y capacidad para tomar decisiones de juego automáticamente.

    Atributos adicionales:
    ----------------------
    nivel : int
        Dificultad de la IA (afecta el comportamiento del motor).
    es_ia : bool
        Indicador de que esta instancia es una IA.
    ia : IADeAjedrez
        Instancia del motor de ajedrez encargado de calcular los movimientos.
    """

    def __init__(self, username: str, password: str = "", elo: int = 1000, nivel: int = 3,es_ia:bool =True,**kwargs) -> None:
        """
        Inicializa una instancia de UsuarioIA con su motor de ajedrez correspondiente.

        Parámetros:
        -----------
        username : str
            Nombre del usuario IA (puede ser visible en el historial de partidas).
        password : str
            Contraseña de la IA. Por lo general se deja vacía.
        elo : int
            Valor ELO inicial de la IA.
        nivel : int
            Nivel de dificultad de la IA. Puede influir en la profundidad de búsqueda.
        """
        super().__init__(username=username, password=password, elo=elo,**kwargs)
        self.nivel: int = nivel
        self.es_ia: bool = es_ia
        self.ia: IADeAjedrez = IADeAjedrez(self.nivel)  # Inicializa el motor IA con el nivel dado

    def to_dict(self) -> Dict[str, Any]:
        """
        Serializa los datos del usuario IA en un diccionario para su almacenamiento.

        Retorna:
        --------
        Dict[str, Any]
            Diccionario que representa al usuario IA, incluyendo atributos adicionales como 'nivel' y 'es_ia'.
        """
        base: Dict[str, Any] = super().to_dict()
        base.update({
            "nivel": self.nivel,
            "es_ia": True
        })
        return base

    @classmethod
    def cargar(cls, user_id: str) -> "UsuarioIA":
        """
        Carga una instancia de UsuarioIA desde un archivo utilizando su ID.

        Parámetros:
        -----------
        user_id : str
            ID único del usuario IA a cargar.

        Retorna:
        --------
        UsuarioIA
            Instancia de UsuarioIA reconstruida a partir del archivo guardado.

        Lanza:
        -------
        FileNotFoundError
            Si no existe un archivo correspondiente al ID.
        ValueError
            Si el archivo existe pero no representa a un usuario IA.
        """
        ruta: str = os.path.join(PATH_USUARIOS, f"{user_id}.json")
        if not os.path.exists(ruta):
            raise FileNotFoundError("Usuario no encontrado")

        with open(ruta, "r", encoding="utf-8") as f:
            datos: Dict[str, Any] = json.load(f)
            if datos.get("es_ia"):
                return cls(**datos)
            else:
                raise ValueError("El usuario no es una IA")
            

    @classmethod
    def cargar_por_username(cls, username: str) -> Optional["UsuarioIA"]:
        """
        Busca y carga una cuenta de IA por su nombre de usuario.

        Parámetros:
        -----------
        username : str
            Nombre de usuario a buscar.

        Retorna:
        --------
        UsuarioIA o None si no se encuentra o no es IA.
        """
        for archivo in os.listdir(PATH_USUARIOS):
            if archivo.endswith(".json"):
                ruta: str = os.path.join(PATH_USUARIOS, archivo)
                with open(ruta, "r", encoding="utf-8") as f:
                    datos: Dict[str, Any] = json.load(f)
                    if datos.get("username") == username and datos.get("es_ia"):
                        return cls(**datos)
        return None
    

    def elegir_movimiento(self, tablero: Any, color: str) -> Any:
        """
        Usa el motor de ajedrez interno para calcular el mejor movimiento para la IA.

        Parámetros:
        -----------
        tablero : Tablero
            Instancia del tablero de juego, que representa el estado actual de la partida.
        color : str
            Color con el que juega la IA ('blanco' o 'negro').

        Retorna:
        --------
        Any
            Movimiento elegido por la IA (según la implementación de IADeAjedrez).
        """
        self.ia.color = color
        return self.ia.encontrar_mejor_movimiento(tablero)
