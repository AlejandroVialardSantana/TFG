import cv2
import os
import numpy as np
import matplotlib.pyplot as plt
from utils.file_utils import create_folder_if_not_exists, process_images

def generate_fire_mask(image):
    _, mask = cv2.threshold(image, 230, 255, cv2.THRESH_BINARY)
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, kernel)

    laplacian = cv2.Laplacian(image, cv2.CV_64F)
    texture_mask = cv2.convertScaleAbs(laplacian)
    _, texture_mask = cv2.threshold(texture_mask, 30, 1, cv2.THRESH_BINARY)

    combined_mask = cv2.bitwise_and(mask, texture_mask)
    return combined_mask

def process_folder(source_folder, target_folder):
    process_images(source_folder, target_folder, generate_fire_mask, file_suffix='mask_')

def check_mask(mask_path):
    mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)
    if mask is None:
        print(f"Error al cargar la máscara: {mask_path}")
        return
    fire_pixels = cv2.countNonZero(mask)
    if fire_pixels > 0:
        print('¡Fuego detectado!')
    else:
        print('No se detectó fuego')

def visualize_fire(mask_path):
    mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)
    if mask is None:
        print(f"Error al cargar la máscara: {mask_path}")
        return
    colored_mask = cv2.applyColorMap(mask * 255, cv2.COLORMAP_INFERNO)
    plt.figure(figsize=(12, 6))
    plt.subplot(121)
    plt.imshow(mask, cmap='gray')
    plt.title('Máscara Original')
    plt.axis('off')
    plt.subplot(122)
    plt.imshow(colored_mask)
    plt.title('Visualización Mejorada')
    plt.axis('off')
    plt.show()
    fire_pixels = cv2.countNonZero(mask)
    print(f'Número de píxeles de fuego detectados: {fire_pixels}') 

def analyze_mask_values(mask_path):
    mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)
    if mask is None:
        print(f"Error al cargar la máscara: {mask_path}")
        return
    hist = cv2.calcHist([mask], [0], None, [256], [0, 256])
    plt.figure()
    plt.title("Histograma de Valores de Píxeles")
    plt.xlabel("Intensidad de Píxel")
    plt.ylabel("Cantidad de Píxeles")
    plt.plot(hist)
    plt.xlim([0, 256])
    plt.show()
    min_val, max_val, _, _ = cv2.minMaxLoc(mask)
    mean_val = cv2.mean(mask)[0]
    print(f"Valor mínimo en la máscara: {min_val}")
    print(f"Valor máximo en la máscara: {max_val}")
    print(f"Valor medio de la máscara: {mean_val}")
