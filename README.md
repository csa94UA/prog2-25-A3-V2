# [Ace Chess]
[//]: # (Incluid aquí la descripción de vuestra aplicación. Por cierto, así se ponen comentarios en Markdown)

Ace Chess es una plataforma de ajedrez online desarrollada en Python que permite a los usuarios jugar partidas de ajedrez contra otros jugadores o contra una IA, gestionar su lista de amigos, enviar y aceptar retos, chatear, y consultar rankings. El proyecto está compuesto por una API RESTful construida con Flask y un cliente de consola interactivo para la gestión y visualización de partidas y usuarios.

## Características principales

- **Registro e inicio de sesión de usuarios** con autenticación JWT.
- **Gestión de partidas de ajedrez**: creación, movimientos, historial y visualización paso a paso.
- **Sistema de amigos**: solicitudes, aceptación, eliminación y visualización de perfiles.
- **Retos entre usuarios**: enviar, aceptar y rechazar retos para iniciar partidas.
- **Chat entre amigos**: mensajería privada entre usuarios conectados.
- **Ranking ELO**: consulta del ranking global y posición individual.
- **Soporte para partidas contra IA** y usuarios reales.
- **Visualización de partidas** con símbolos Unicode para las piezas.
- **API RESTful** documentada y extensible.

## Autores

* [Carlos Salas Alarcón](https://github.com/csa94UA)
* [Mohammed Alí Arshad Bhatti](https://github.com/MohammedAli-Biar)

## Profesor
[//]: # (Dejad a quien corresponda)
[Miguel A. Teruel](https://github.com/materuel-ua)

## Requisitos
[//]: # (Indicad aquí los requisitos de vuestra aplicación, así como el alumno responsable de cada uno de ellos)
* Diseño y Programación del Juego [Mohammed Alí] 

* Compatibilidad con Base de Datos y Algoritmos [Carlos] 

* API y contacto con servidor [Mohammed Alí] 

* Optimización de Algoritmos y creación de IA básica [Mohammed Alí] 

* Interacción con una IA avanzada  [Carlos] 

## Instrucciones de instalación y ejecución
[//]: # (Indicad aquí qué habría que hacer para ejecutar vuestra aplicación)

1. Clonar el repositorio en un directorio
```bash
git clone <repositorio>
cd <directorio>
```

2. Crear entorno virtual e instalar las librerías necesarias con el archivo requirements.txt
```bash
python3 -m venv <entorno_virtual>
source venv/bin/activate
pip install -r requirements.txt
```
3. Ejecutar el servidor Flask
```bash
python api.py
```

4. Seguidamente ejecutamos el programa de pruebas
```bash
python examples.py
```

## Resumen de la API
[//]: # (Cuando tengáis la API, añadiréis aquí la descripción de las diferentes llamadas.)
[//]: # (Para la evaluación por pares, indicaréis aquí las diferentes opciones de vuestro menú textual, especificando para qué sirve cada una de ellas)

La API Flask ofrece funcionalidades para gestionar partidas de ajedrez, movimientos, amigos, chat y autenticación de usuarios.

### Endpoints de la API

#### Generales
- **GET /**  
  Estado de la API.

#### Autenticación y usuario
- **POST /registrar**  
  Registro de usuarios.
- **POST /iniciarsesion**  
  Inicio de sesión y generación de tokens.
- **POST /salir**  
  Cierre de sesión (logout).
- **GET /perfil**  
  Muestra datos del perfil del usuario autenticado.

#### Ranking
- **GET /ranking**  
  Obtener ranking de usuarios por ELO.
- **GET /ranking/posicion/<username>**  
  Obtener la posición de un usuario en el ranking.

#### Amigos
- **GET /amigos**  
  Listar amigos del usuario autenticado.
- **GET /amigos/perfil/<username_amigo>**  
  Ver perfil de un amigo.
- **GET /amigos/solicitudes**  
  Ver solicitudes de amistad recibidas.
- **POST /amigos/solicitud**  
  Enviar solicitud de amistad (requiere `destinatario_username` en JSON).
- **POST /amigos/aceptar**  
  Aceptar solicitud de amistad (requiere `remitente_username` en JSON).
- **DELETE /amigos/eliminar**  
  Eliminar amigo (requiere `amigo_id` en JSON).

#### Partidas
- **POST /partidas/nueva**  
  Inicializar nueva partida.
- **GET /partidas**  
  Obtener partidas finalizadas (historial).
- **GET /partidas/<nombre_sesion>**  
  Obtener información de una partida finalizada.
- **DELETE /partidas/<sesion_id>**  
  Eliminar partida existente.
- **POST /partidas/cargar_temp/<nombre_archivo>**  
  Cargar una partida temporal.
- **GET /partidas/activas**  
  Obtener partidas activas del usuario autenticado.
- **POST /partidas/<sesion_id>/mover**  
  Realizar un movimiento en una partida activa.
- **GET /partidas/<sesion_id>/estado**  
  Obtener el estado actual del tablero de una partida activa.

#### Retos
- **GET /retos**  
  Ver retos recibidos.
- **POST /retos/enviar/<username_amigo>**  
  Enviar reto a un amigo.
- **POST /retos/aceptar/<retador_username>**  
  Aceptar reto.
- **POST /retos/rechazar/<retador_username>**  
  Rechazar reto.

#### Chat y mensajes
- **POST /amigos/<receptor_username>/mensaje**  
  Enviar mensaje a un amigo.
- **GET /amigos/<otro_username>/chat**  
  Obtener chat con un amigo.
