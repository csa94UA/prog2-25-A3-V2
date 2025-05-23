"""
Módulo que define la clase SesionDeJuego para gestionar partidas de ajedrez entre dos usuarios.

Contiene toda la lógica de juego, movimientos, validaciones, estado y guardado de partidas.
"""
import json
import os
from datetime import datetime
from typing import Tuple, Union, Dict, Any, Optional,Type

from juego.tablero import Tablero
from juego.validador_movimiento import ValidadorMovimiento
from utiles.file_menager import guardar_partida
from utiles.elo import calcular_elo
from usuario.usuario import Usuario
from juego.usuarioIA import UsuarioIA
from config import PATH_PARTIDAS_TEMP

class SesionDeJuego:
    """
    Clase que representa una sesión de juego entre dos usuarios.

    Atributos:
    ----------
    tablero : Tablero
        Tablero de ajedrez con las piezas y estado actual.
    jugador_blanco : Usuario
        Usuario que juega con blancas.
    jugador_negro : Usuario
        Usuario que juega con negras.
    turno_actual : str
        Color del jugador que tiene el turno ('blanco' o 'negro').
    validador : ValidadorMovimiento
        Validador para verificar movimientos legales.
    terminado : bool
        Indica si la partida ha finalizado.
    ganador : Optional[str]
        Color del ganador ('blanco', 'negro' o None si empate o en curso).
    movimientos : list
        Lista de movimientos realizados en la partida.
    """

    def __init__(self, jugador_blanco: Usuario, jugador_negro: Usuario) -> None:
        """
        Inicializa la sesión de juego con dos jugadores.

        Parámetros:
        -----------
        jugador_blanco : Usuario
            Usuario que jugará con las piezas blancas.
        jugador_negro : Usuario
            Usuario que jugará con las piezas negras.
        """
        self.tablero: Tablero = Tablero()
        self.jugador_blanco: Usuario = jugador_blanco
        self.jugador_negro: Usuario = jugador_negro
        self.turno_actual: str = "blanco"
        self.validador: ValidadorMovimiento = ValidadorMovimiento(self.tablero)
        self.terminado: bool = False
        self.ganador: Optional[str] = None
        self.movimientos: list = []
        self.archivos_temporales: list[str] = []

    def jugar_turno(self, entrada: Union[str, Tuple[Tuple[int, int], Tuple[int, int]]] = None,promocion = None) -> Dict[str, Any]:
        """
        Ejecuta un turno con la entrada dada. Si es el turno de una IA, se genera el movimiento automáticamente.

        Parámetros:
        -----------
        entrada : Union[str, Tuple[Tuple[int, int], Tuple[int, int]]], opcional
            Movimiento del jugador (origen, destino) o "abandono". Si el jugador es una IA, este parámetro se ignora.

        Retorna:
        --------
        dict
            Resultado del turno con mensajes, estado y datos relevantes.
        """
        if self.terminado:
            return {"error": "La partida ya ha terminado."}

        jugador_actual = self.jugador_blanco if self.turno_actual == "blanco" else self.jugador_negro

        if isinstance(jugador_actual, UsuarioIA):
            entrada = jugador_actual.elegir_movimiento(self.tablero, self.turno_actual)

        if entrada == "abandono" or (entrada == None and isinstance(jugador_actual, UsuarioIA)):
            return self.rendirse(self.turno_actual)

        origen, destino = entrada
        pieza = self.tablero.casillas[origen[0]][origen[1]]

        if not pieza :
            return {"error": "Movimiento inválido: no hay pieza."}
        
        if pieza.color != self.turno_actual:
            return {"error": "Movimiento inválido: no es tu turno."}

        if not self.validador.movimiento_es_legal(origen, destino, self.turno_actual):
            return {"error": "Movimiento ilegal."}
        
        pieza_destino = self.tablero.casillas[destino[0]][destino[1]]

        if pieza.__class__.__name__ == "peon":
            if (pieza.color == "blanco" and destino[0] == 0) or (pieza.color == "negro" and destino[0] == 7):
                if promocion is None:
                    promocion = "dama"

                if promocion not in ["dama","caballo","alfil","torre"]:
                    promocion = "dama"

        self.tablero.mover_pieza((origen, destino),promocion)

        self.movimientos.append({
            "origen": origen,
            "destino": destino,
            "pieza": pieza.__class__.__name__,
            "color": pieza.color,
            "captura": pieza_destino.__class__.__name__ if pieza_destino else None
        })

        estado_finalizado = False
        mensaje: Optional[str] = None

        if self.validador.esta_en_jaque(self._oponente()):
            if not self._hay_movimientos_legales(self._oponente()):
                self.terminado = True
                self.ganador = self.turno_actual
                nombre_archivo = self.finalizar_y_guardar()
                estado_finalizado = True
                mensaje = f"¡Jaque mate! {self.turno_actual} gana."
            else:
                mensaje = f"{self._oponente()} está en jaque."
        elif not self._hay_movimientos_legales(self._oponente()):
            self.terminado = True
            nombre_archivo = self.finalizar_y_guardar()
            estado_finalizado = True
            mensaje = "¡Tablas por ahogado!"

        if not estado_finalizado:
            temp_result = self.guardar_estado_temporal()
            self.turno_actual = self._oponente()
            return {
                "msg": "Movimiento realizado.",
                "estado": "continuar",
                "turno_siguiente": self.turno_actual,
                "temp_guardado": temp_result,
                "alerta": mensaje,
                "movimiento":f"({origen},{destino})",
                "tablero":str(self.tablero)
            }
        else:
            return {
                "msg": mensaje,
                "estado": "terminado",
                "ganador": self.ganador,
                "archivo": nombre_archivo,
                "movimiento":f"({origen},{destino})",
                "tablero":str(self.tablero)
            }

    def _oponente(self) -> str:
        """
        Obtiene el color del oponente al turno actual.

        Retorna:
        --------
        str
            Color del oponente ('blanco' o 'negro').
        """
        return "negro" if self.turno_actual == "blanco" else "blanco"

    def _hay_movimientos_legales(self, color: str) -> bool:
        """
        Verifica si hay movimientos legales para un color dado.

        Parámetros:
        -----------
        color : str
            Color de las piezas ('blanco' o 'negro').

        Retorna:
        --------
        bool
            True si existe al menos un movimiento legal, False en caso contrario.
        """
        for fila in range(8):
            for col in range(8):
                pieza = self.tablero.casillas[fila][col]
                if pieza and pieza.color == color:
                    for legal in pieza.obtener_movimientos_validos(
                        (fila, col), self.tablero
                    ):
                        
                        if self.validador.movimiento_es_legal((fila,col),legal,color):
                            return True
        return False
    def obtener_datos_partida(self, include_final: bool = True) -> Dict[str, Any]:
        """
        Obtiene los datos completos de la partida para guardado o análisis.
        """
        datos = {
            "jugador_blanco": {
                "user_id": self.jugador_blanco.user_id,
                "username": f"{self.jugador_blanco.username}(blanco)"
            },
            "jugador_negro": {
                "user_id": self.jugador_negro.user_id,
                "username": f"{self.jugador_negro.username}(negro)"
            },
            "ganador": self.ganador,
            "movimientos": self.movimientos,
            "fecha": str(datetime.now()),
            "turno_actual": self.turno_actual,
            "terminado": self.terminado
        }

        if include_final:
            datos["tablero_final"] = [
                [
                    {
                        "tipo": pieza.__class__.__name__,
                        "color": pieza.color
                    } if pieza else None
                    for pieza in fila
                ]
                for fila in self.tablero.casillas
            ]

        return datos

    def finalizar_y_guardar(self) -> Union[Dict[str, Any], Dict[str, str]]:
        """
        Finaliza la partida, calcula el elo, actualiza usuarios y guarda la partida.

        Retorna:
        --------
        dict
            Resultado del guardado con información o error.
        """
        if not self.terminado:
            return {"error": "La partida no ha terminado aún."}

        datos = self.obtener_datos_partida()
        try:
            nombre_archivo = guardar_partida(datos)
        except RuntimeError as e:
            return {"error": str(e)}

        self.jugador_blanco.historial.append(nombre_archivo)
        self.jugador_negro.historial.append(nombre_archivo)

        if self.ganador == "blanco":
            delta = calcular_elo(self.jugador_blanco.elo, self.jugador_negro.elo, 1)
            self.jugador_blanco.elo += delta
            self.jugador_negro.elo -= delta
        elif self.ganador == "negro":
            delta = calcular_elo(self.jugador_negro.elo, self.jugador_blanco.elo, 1)
            self.jugador_negro.elo += delta
            self.jugador_blanco.elo -= delta
        else:  # empate
            delta = calcular_elo(self.jugador_blanco.elo, self.jugador_negro.elo, 0.5)
            self.jugador_blanco.elo += delta
            self.jugador_negro.elo += delta

        self.jugador_blanco.guardar()
        self.jugador_negro.guardar()
        self.limpiar_archivos_temporales()
        return {
            "msg": "Partida finalizada y guardada con éxito",
            "archivo": nombre_archivo,
            "ganador": self.ganador,
            "elo_blanco": self.jugador_blanco.elo,
            "elo_negro": self.jugador_negro.elo,
            "tablero":str(self.tablero)
        }

    def rendirse(self, color_que_se_rinde: str) -> Dict[str, Any]:
        """
        Permite a un jugador rendirse y finalizar la partida.

        Parámetros:
        -----------
        color_que_se_rinde : str
            Color del jugador que se rinde ('blanco' o 'negro').

        Retorna:
        --------
        dict
            Resultado de la rendición y finalización.
        """
        if self.terminado:
            return {"error": "La partida ya ha terminado."}

        self.terminado = True
        self.ganador = self._oponente() if color_que_se_rinde == self.turno_actual else self.turno_actual

        resultado = self.finalizar_y_guardar()
        if "error" in resultado:
            return resultado

        resultado["msg"] = f"{color_que_se_rinde} se ha rendido. Gana {self.ganador}."
        return resultado

    def guardar_estado_temporal(self) -> Dict[str, Any]:
        """
        Guarda un estado temporal de la partida (sin incluir estado final).

        Retorna:
        --------
        dict
            Mensaje de éxito o error al guardar el estado temporal.
        """
        try:
            datos = self.obtener_datos_partida()
            nombre_archivo = f"{self.jugador_blanco.username}_vs_{self.jugador_negro.username}"
            nombre_archivo = guardar_partida(datos,nombre_archivo=nombre_archivo, temporal=True)
            self.archivos_temporales.append(nombre_archivo)
            return {"msg": "Estado temporal guardado correctamente.", "archivo": nombre_archivo}
        except Exception as e:
            return {"error": f"No se pudo guardar el estado temporal: {str(e)}"}

    def limpiar_archivos_temporales(self) -> None:
        """
        Elimina los archivos temporales creados durante la sesión de juego.
        """
        for archivo in self.archivos_temporales:
            ruta = os.path.join(PATH_PARTIDAS_TEMP, archivo)
            if os.path.exists(ruta):
                os.remove(ruta)

    @classmethod
    def cargar_desde_guardado(cls: Type["SesionDeJuego"], nombre_archivo: str) -> "SesionDeJuego":
        """
        Carga una sesión de juego desde un archivo JSON previamente guardado.

        Parámetros:
        -----------
        nombre_archivo : str
            Nombre del archivo de la partida guardada (ej. partida_A_vs_B_temp.json)

        Retorna:
        --------
        SesionDeJuego
            Instancia reconstruida de la partida.

        Lanza:
        ------
        FileNotFoundError
            Si el archivo especificado no existe.
        """
        ruta = os.path.join(PATH_PARTIDAS_TEMP, nombre_archivo)
        if not os.path.exists(ruta):
            raise FileNotFoundError(f"No se encontró el archivo de partida: {nombre_archivo}")

        with open(ruta, "r", encoding="utf-8") as f:
            datos: Dict[str, Any] = json.load(f)

        # Cargar jugadores (Usuario o UsuarioIA)
        jugador_blanco = Usuario.cargar(datos["jugador_blanco"]["user_id"])
        try:
            jugador_negro = Usuario.cargar(datos["jugador_negro"]["user_id"])
        except:
            jugador_negro = UsuarioIA.cargar(datos["jugador_negro"]["user_id"])

        # Crear la instancia sin iniciar desde cero
        instancia = cls(jugador_blanco, jugador_negro)
        instancia.turno_actual = datos["turno_actual"]
        instancia.terminado = datos["terminado"]
        instancia.ganador = datos["ganador"]
        instancia.movimientos = datos["movimientos"]

        # Restaurar estado del tablero
        instancia.tablero.restaurar_estado_lista(datos["tablero_final"])

        return instancia