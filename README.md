# [Yorkshire Chess]
[//]: # (Incluid aquí la descripción de vuestra aplicación. Por cierto, así se ponen comentarios en Markdown)

## Autores

* (Coordinador) [Julio Alfonso De la Torre León](https://github.com/JulioAlfonsoUA)
* [Carlos Salas Alarcón](https://github.com/csa94UA)
* [Mohammed Alí Arshad Bhatti](https://github.com/MohammedAli-Biar)
* [Vicente Pérez Pourtau](https://github.com/vicenteprzz)
* [Sofía Pérez Vásquez](https://github.com/sofiaaperezz)

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
La API Flask ofrece funcionalidades para gestionar partidas de ajedrez, movimientos y autenticación de usuarios.


Rutas Principales

* POST /signup: Registro de usuarios.

* GET /login: Inicio de sesión y generación de tokens.

* GET /perfil: Muestra datos del perfil del usuario.

* PUT /perfil: Modificar perfil del usuario.

* DELETE /perfil: Eliminar perfil del usuario.

* GET /partida/json: Obtener partida en json.

* POST /partida: Inicializar nueva partida.

* DELETE /partida: Eliminar partida existente.

* GET /partida: Obtener partidas existentes.