# TFG - Detección temprana de anomalías térmicas en escenas a larga distancia mediante una cámara térmico-óptica 📷

Este proyecto tiene como objetivo desarrollar un modelo de aprendizaje automático para la identificación precisa de zonas o puntos de calor en imágenes capturadas por cámaras PTZ. El desafío se aborda a través de la manipulación y análisis de termogramas o imágenes en escala de grises que reflejan variaciones de temperatura. Esto permite un tratamiento detallado y específico sobre las máscaras de calor en escenas a larga distancia. La cámara mencionada no facilita el acceso a los datos RAW, lo que dificulta el análisis de los datos pero supone un desafío mayor, ya que debemos analizar anomalías a partir de las propias imágenes.

## 📁 Estructura de Directorios

TFG/ <br>
|-- main.py **# Punto de entrada de la aplicación.** <br>
|-- .env **# Archivo para variables de entorno.** <br>
|-- README.md **# Documentación del proyecto.** <br>
|-- requirements.txt **# Dependencias del proyecto.** <br>
|-- camera/ **# Módulo para la gestión de la cámara.** <br>
|   |-- \__init__.py **# Hace que Python trate los directorios como módulos.** <br>
|   |-- thermal_camera.py **# Gestiona la funcionalidad térmica de la cámara.** <br>
|-- data/ **# Directorio para almacenar datos de entrada y salida.** <br>
|   |-- images/ **# Imágenes originales.** <br>
|   |-- masks/ **# Máscaras generadas.** <br>
|   |-- simulated_fire/ **# Imágenes con fuego simulado.** <br>
|-- image_processing/ **# Módulo para procesamiento de imágenes.** <br>
|   |-- \__init__.py **# Hace que Python trate los directorios como módulos.** <br>
|   |-- fire_detection.py **# Detección de zonas de fuego.** <br>
|   |-- image_processor.py **# Procesamiento básico de imágenes.** <br>
|   |-- simulated_fire.py **# Generación de fuego simulado en imágenes.** <br>
|   |-- perlin_noise.py **# Generación de ruido Perlin para simular fuego.** <br>
|-- utils/ **# Utilidades y funciones auxiliares.** <br>
|   |-- \__init__.py **# Hace que Python trate los directorios como módulos.** <br>
|   |-- file_utils.py **# Funciones para manejo de archivos y directorios.** <br>
|   |-- test_image_processor.py **# Pruebas para el módulo de procesamiento de imágenes.** <br>
|-- .gitignore **# Archivos y directorios ignorados por Git.** <br>

## 📄 Archivo .env

El archivo `.env` contiene las variables de entorno necesarias para configurar la aplicación. Debes crear este archivo e inicializar las variables con tus parámetros.

Variables de entorno necesarias:

- `PTZ_IP_ADDRESS`: Dirección IP de la cámara PTZ.
- `PTZ_PORT`: Puerto de la cámara PTZ.
- `PTZ_USER`: Usuario para la autenticación con la cámara.
- `PTZ_PASS`: Contraseña para la autenticación con la cámara.
- `PTZ_WSDL_ROUTE`: Ruta al archivo WSDL para los servicios ONVIF.

## 🛠️ Construido con

- [Python](https://www.python.org/) - El lenguaje de programación usado.
- [ONVIF](https://www.onvif.org/) - Estándar para la comunicación en sistemas de videovigilancia.
- [OpenCV](https://opencv.org/) - Biblioteca de procesamiento de imágenes en tiempo real.

## ✒️ Autores

- **Alejandro Vialard Santana**  - [GitHub](https://github.com/AlejandroVialardSantana)
