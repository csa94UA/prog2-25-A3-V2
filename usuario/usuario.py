import os
import json
from typing import List, Dict, Any, Optional

from utiles.id_generator import generar_id
from utiles.file_menager import cargar_partida

# Ruta donde se almacenan los archivos de usuarios
from config import PATH_USUARIOS


class Usuario:
    """
    Clase que representa a un usuario del sistema.
    Incluye funcionalidades para gestionar sus datos, historial y amigos.
    """

    def __init__(
        self,
        username: str,
        password: str,
        elo: int = 1000
    ) -> None:
        """
        Inicializa un nuevo usuario.

        Parámetros:
        -----------
        username : str
            Nombre de usuario.
        password : str
            Contraseña del usuario.
        elo : int, opcional
            Puntuación ELO inicial del usuario (por defecto es 1200).
        """
        self.username: str = username
        self.password: str = password
        self.user_id: str = generar_id()
        self.elo: int = elo
        self.historial: List[str] = [] # Lista de nombres de archivos de partidas
        self.partidas_enjuego: List =  [] # Lista de las partidas que esta jugando 
        self.amigos: List[str] = [] # Lista de IDs de amigos

    def to_dict(self) -> Dict[str, Any]:
        """
        Convierte los datos del usuario a un diccionario serializable.

        Retorna:
        --------
        Dict[str, Any]
            Representación en diccionario del usuario.
        """
        return {
            "username": self.username,
            "password_crypted": self.password,
            "user_id": self.user_id,
            "elo": self.elo,
            "historial": self.historial,
            "partidas_enjuego": self.partidas_enjuego,
            "amigos": self.amigos
        }

    def guardar(self) -> None:
        """
        Guarda los datos del usuario en un archivo JSON utilizando su ID como nombre.
        """
        ruta: str = os.path.join(PATH_USUARIOS, f"{self.user_id}.json")
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=4)

    def mostrar_historial(self) -> Dict[str, Any]:
        """
        Devuelve el historial de partidas del usuario, extrayendo datos clave de cada archivo.

        Retorna:
        --------
        Dict[str, Any]
            Diccionario con el nombre de usuario y una lista con detalles de cada partida.
        """
        historial: List[Dict[str, Any]] = []

        for archivo in self.historial:
            try:
                datos: Dict[str, Any] = cargar_partida(archivo)
                # Asumimos que tendrá toda esta información la partida
                historial.append({
                    "fecha": datos.get("fecha"),
                    "jugador_blanco": datos["jugador_blanco"]["username"],
                    "jugador_negro": datos["jugador_negro"]["username"],
                    "ganador": datos.get("ganador", "empate")  # Si no hay key 'ganador', asumimos empate
                })
            except Exception as e:
                # En caso de error al cargar una partida, se registra el error en el historial
                historial.append({
                    "archivo": archivo,
                    "error": str(e)
                })

        return {
            "usuario": self.username,
            "partidas": historial
        }

    @classmethod
    def cargar(cls, user_id: str) -> "Usuario":
        """
        Carga un usuario desde archivo por su ID.

        Parámetros:
        -----------
        user_id : str
            ID del usuario a cargar.

        Retorna:
        --------
        Usuario
            Instancia de Usuario cargada desde el archivo.

        Lanza:
        -------
        FileNotFoundError si el archivo no existe.
        """
        ruta: str = os.path.join(PATH_USUARIOS, f"{user_id}.json")
        if not os.path.exists(ruta):
            raise FileNotFoundError("Usuario no encontrado")

        with open(ruta, "r", encoding="utf-8") as f:
            datos: Dict[str, Any] = json.load(f)
            return cls(**datos)

    @classmethod
    def cargar_por_username(cls, username: str) -> Optional["Usuario"]:
        """
        Busca y carga un usuario por su nombre de usuario.

        Parámetros:
        -----------
        username : str
            Nombre de usuario a buscar.

        Retorna:
        --------
        Usuario o None si no se encuentra.
        """
        for archivo in os.listdir(PATH_USUARIOS):
            if archivo.endswith(".json"):
                ruta: str = os.path.join(PATH_USUARIOS, archivo)
                with open(ruta, "r", encoding="utf-8") as f:
                    datos: Dict[str, Any] = json.load(f)
                    if datos.get("username") == username:
                        return cls(**datos)
        return None
