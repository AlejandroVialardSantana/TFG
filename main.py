import os
from dotenv import load_dotenv
from image_processing.fire_detection import process_folder
from utils.file_utils import create_folder_if_not_exists, process_images
from image_processing.simulated_fire import add_fire, add_fire_pattern

# Load environment variables
load_dotenv()

def main():
    source_folder = 'data/images'
    simulated_fire_folder = 'data/simulated_fire'
    mask_folder = 'data/masks'

    # Crear los directorios de destino si no existen
    create_folder_if_not_exists(simulated_fire_folder)
    create_folder_if_not_exists(mask_folder)

    # Seleccionar el método para añadir fuego
    method = input("Seleccione el método para agregar fuego (1: Perlin Noise, 2: Pattern): ")

    if method == "1":
        # Generar imágenes con zonas de fuego utilizando Perlin Noise y guardarlas
        process_images(source_folder, simulated_fire_folder, add_fire)
    elif method == "2":
        # Generar imágenes con zonas de fuego utilizando el patrón definido y guardarlas
        process_images(source_folder, simulated_fire_folder, add_fire_pattern)
    else:
        print("Método no válido.")
        return

    # Crear máscaras para las imágenes con zonas de fuego generadas
    process_folder(simulated_fire_folder, mask_folder)

if __name__ == "__main__":
    main()