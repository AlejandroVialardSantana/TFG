import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import random

def generate_binary_mask(image):
    """Genera una máscara binaria para áreas con valores de luminosidad entre 200 y 239 en la imagen."""
    # Define los límites inferior y superior para el rango de luminosidad
    lower_bound = 200
    upper_bound = 239

    mask = cv2.inRange(image, lower_bound, upper_bound)

    kernel = np.ones((5, 5), np.uint8)
    
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, kernel)
    return mask

def display_random_images_with_masks(directory_path, num_images=4):
    """Muestra cuatro imágenes aleatorias del directorio y sus máscaras binarias en una figura de 2x4."""
    image_files = [f for f in os.listdir(directory_path) if f.endswith(".jpg") or f.endswith(".png")]
    
    selected_images = random.sample(image_files, num_images)
    
    plt.figure(figsize=(12, 8))
    
    for i, filename in enumerate(selected_images):
        image_path = os.path.join(directory_path, filename)
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

        if image is None:
            print(f"Error al cargar la imagen {filename}")
            continue
        
        binary_mask = generate_binary_mask(image)

        plt.subplot(2, num_images, i + 1)
        plt.imshow(image, cmap='gray')
        plt.title(f"Imagen Original - {i + 1}")
        plt.axis('off')

        plt.subplot(2, num_images, i + 1 + num_images)
        plt.imshow(binary_mask, cmap='gray')
        plt.title("Máscara Binaria")
        plt.axis('off')
    
    plt.tight_layout()
    plt.show()

directory_path = "data/IR-FLAME-IMAGES"
display_random_images_with_masks(directory_path)
