import os
from dotenv import load_dotenv
from image_processing.fire_detection import process_folder
from utils.file_utils import create_folder_if_not_exists, process_images
from image_processing.simulated_fire import add_fire

# Load environment variables
load_dotenv()

if __name__ == "__main__":
    source_folder = 'data/images'
    simulated_fire_folder = 'data/simulated_fire'
    mask_folder = 'data/masks'
    
    # Crear los directorios de destino si no existen
    create_folder_if_not_exists(simulated_fire_folder)
    create_folder_if_not_exists(mask_folder)
    
    # Generar imágenes con zonas de fuego y guardarlas
    process_images(source_folder, simulated_fire_folder, add_fire)
    
    # Crear máscaras para las imágenes con zonas de fuego generadas
    process_folder(simulated_fire_folder, mask_folder)