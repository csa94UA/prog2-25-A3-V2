import os
import json
from datetime import datetime
from typing import Any, Dict, List

# Directorio donde se almacenan las partidas
from config import PATH_PARTIDAS

def guardar_partida(partida_data: Dict[str, Any], temporal: bool = False) -> str:
    """
    Guarda los datos de una partida en un archivo JSON en el directorio definido.

    Parámetros:
    -----------
    partida_data : Dict[str, Any]
        Diccionario con los datos de la partida a guardar.
    temporal : bool, opcional
        Si es True, el archivo se marcará como temporal con el sufijo "_temp".

    Retorna:
    --------
    str
        Nombre del archivo JSON guardado.

    Lanza:
    ------
    RuntimeError
        Si ocurre un error al escribir el archivo.
    """
    # Generar nombre único basado en fecha y hora
    nombre_archivo = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_archivo = f"partida_{nombre_archivo}"
    if temporal:
        nombre_archivo += "_temp"
    nombre_archivo += ".json"

    # Ruta completa del archivo
    ruta = os.path.join(PATH_PARTIDAS, nombre_archivo)

    try:
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(partida_data, f, indent=4)
        return nombre_archivo
    except Exception as e:
        raise RuntimeError(f"Error al guardar partida: {e}")

def cargar_partida(nombre_archivo: str) -> Dict[str, Any]:
    """
    Carga una partida desde un archivo JSON.

    Parámetros:
    -----------
    nombre_archivo : str
        Nombre del archivo de partida a cargar.

    Retorna:
    --------
    Dict[str, Any]
        Diccionario con los datos de la partida cargada.

    Lanza:
    ------
    FileNotFoundError
        Si el archivo no existe.
    """
    ruta = os.path.join(PATH_PARTIDAS, nombre_archivo)

    if not os.path.exists(ruta):
        raise FileNotFoundError("La partida no existe.")

    with open(ruta, "r", encoding="utf-8") as f:
        return json.load(f)

def listar_partidas() -> List[str]:
    """
    Lista todos los archivos de partida disponibles en el directorio.

    Retorna:
    --------
    List[str]
        Lista de nombres de archivos JSON correspondientes a partidas guardadas.
    """
    return [
        f for f in os.listdir(PATH_PARTIDAS)
        if f.endswith(".json")
    ]
