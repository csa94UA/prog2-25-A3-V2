import os
import json
from typing import List, Dict, Any

from utiles.id_generator import generar_id
from utiles.file_menager import cargar_partida

# Ruta donde se almacenan los archivos de usuarios
from config import PATH_USUARIOS
class Usuario:
    """
    Clase que representa a un usuario del sistema.
    Incluye funcionalidades para gestionar sus datos, historial y amigos.
    """

    def __init__(self, username: str, password: str, elo: int = 1200) -> None:
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
        self.historial: List[str] = []  # Lista de nombres de archivos de partidas
        self.partidas_enjuego: List = [] # Lista de las partidas que esta jugando 
        self.amigos: List[str] = []     # Lista de IDs de amigos

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
            "password": self.password,
            "user_id": self.user_id,
            "elo": self.elo,
            "historial": self.historial,
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
                    "ganador": datos.get("ganador","empate") # Si no hay ningún key ganador es por que fue un empate
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
