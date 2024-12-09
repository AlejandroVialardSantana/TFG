# TFG - Detección temprana de anomalías térmicas en escenas a larga distancia mediante una cámara térmico-óptica 📷

En este trabajo de fin de título (TFT) se investigaron diversas técnicas de aprendizaje automático para desarrollar un modelo capaz de detectar anomalías térmicas, como fuego y humo, en entornos portuarios, empleando una cámara Hikvision bi-espectro. Se exploraron y evaluaron distintos modelos hasta lograr un enfoque óptimo. Para el entrenamiento, se creó un dataset sintético con imágenes térmicas de incendios, que luego se combinó con imágenes reales para validar el rendimiento del sistema. El modelo final es capaz de generar alertas tempranas, contribuyendo a la prevención de daños y a la seguridad en áreas costeras. Este enfoque integra técnicas avanzadas para mejorar la vigilancia en infraestructuras portuarias.

El repositorio contiene diferentes utilidades y casos de uso que fueron utilizados en el desarrollo e investigación, como puede ser procesamiento de imágenes, operaciones con ficheros o preparación de datos para entrenamiento de modelos.

## 📁 Estructura de Directorios

TFG/ <br>
|-- main.py **# Punto de entrada de la aplicación.** <br>
|-- .env **# Archivo para variables de entorno.** <br>
|-- README.md **# Documentación del proyecto.** <br>
|-- requirements.txt **# Dependencias del proyecto.** <br>
|-- camera/ **# Módulo para la gestión de la cámara.** <br>
|-- data/ **# Directorio para almacenar datos de entrada y salida.** <br>
|-- image_processing/ **# Módulo para procesamiento de imágenes.** <br>
|-- utils/ **# Utilidades y funciones auxiliares.** <br>
|-- scripts/ **# Casos de uso completos de algunas funciones** <br>
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
- [PyTorch](https://pytorch.org/) - Biblioteca de código abierto para machine learning que permite desarrollar y entrenar modelos de aprendizaje profundo de manera flexible y eficiente.
- [OpenCV](https://opencv.org/) - Biblioteca de procesamiento de imágenes en tiempo real.

## ✒️ Autor

- **Alejandro Vialard Santana**  - [GitHub](https://github.com/AlejandroVialardSantana)
