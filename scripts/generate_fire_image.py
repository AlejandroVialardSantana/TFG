import cv2
import numpy as np
import random
import os
from PIL import Image, ImageDraw

# Coordenadas para evitar la barra lateral (ajustar según sea necesario)
BAR_X_START = 600  # Ajusta según la posición de la barra lateral en la imagen

# Función para expandir el fuego en un área específica con ruido controlado en los bordes
def expand_fire(image, position, fire_radius, border_radius, intensity=0.8, border_noise_level=0.5):
    draw = ImageDraw.Draw(image)
    x, y = position
    for i in range(-border_radius, border_radius):
        for j in range(-border_radius, border_radius):
            if x + i < BAR_X_START:  # Evitar la zona de la barra lateral
                distance = np.sqrt(i**2 + j**2)
                if distance < fire_radius:
                    alpha = int(255 * (1 - distance / fire_radius))
                    draw.point((x + i, y + j), fill=(235, 235, 235, alpha))
                elif distance < border_radius:
                    if random.random() < intensity * (1 - (distance - fire_radius) / (border_radius - fire_radius)):
                        alpha = int(255 * (1 - (distance - fire_radius) / (border_radius - fire_radius)))
                        noise = random.uniform(-border_noise_level, border_noise_level) * 20
                        border_value = 190 + (240 - 190) * (1 - (distance - fire_radius) / (border_radius - fire_radius)) + noise
                        draw.point((x + i, y + j), fill=(int(border_value), int(border_value), int(border_value), alpha))

# Función para añadir un patrón de fuego a la imagen
def add_fire_pattern(image_path, border_noise_level=0.5):
    target_image = Image.open(image_path).convert('RGBA')
    target_image_with_fire = Image.new('RGBA', target_image.size)
    target_image_with_fire.paste(target_image)

    # Convertir la imagen a escala de grises y detectar áreas blancas
    grayscale_image = target_image.convert('L')
    threshold_value = 250 
    _, thresholded = cv2.threshold(np.array(grayscale_image), threshold_value, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    num_fires = random.randint(1, 5)
    for _ in range(num_fires):
        if not contours:
            print("No se encontraron contornos.")
            break
        contour = random.choice(contours)
        x, y, w, h = cv2.boundingRect(contour)
        if x + w < BAR_X_START:  # Evitar contornos en la barra lateral
            pos = (random.randint(x, x + w), random.randint(y, y + h))
            fire_radius = random.randint(5, 15)
            border_radius = fire_radius + random.randint(5, 10)
            expand_fire(target_image_with_fire, pos, fire_radius, border_radius, border_noise_level=border_noise_level)

    return target_image_with_fire.convert('RGB')

# Función para crear una máscara de fuego basada en umbrales
def create_fire_mask(image, fire_threshold=(230, 239), bar_x_start=600):
    grayscale_image = image.convert('L')
    mask = np.array(grayscale_image)

    # Aplicar umbral fijo
    fire_mask = cv2.inRange(mask, fire_threshold[0], fire_threshold[1])

    # Aplicar operaciones morfológicas para mejorar la máscara
    kernel = np.ones((3, 3), np.uint8)
    fire_mask = cv2.morphologyEx(fire_mask, cv2.MORPH_CLOSE, kernel)
    fire_mask = cv2.morphologyEx(fire_mask, cv2.MORPH_OPEN, kernel)

    # Filtrar por tamaño de contorno, forma y propiedades geométricas
    contours, _ = cv2.findContours(fire_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    fire_mask_filtered = np.zeros_like(fire_mask)

    for contour in contours:
        if is_fire_contour(contour, bar_x_start):
            cv2.drawContours(fire_mask_filtered, [contour], -1, 255, -1)

    return Image.fromarray(fire_mask_filtered)

def is_fire_contour(contour, bar_x_start, area_range=(100, 1000), aspect_ratio_range=(0.5, 2), circularity_threshold=0.1, solidity_threshold=0.5):
    x, y, w, h = cv2.boundingRect(contour)
    if x + w >= bar_x_start:
        return False

    area = cv2.contourArea(contour)
    if not (area_range[0] < area < area_range[1]):
        return False

    aspect_ratio = float(w) / h
    if not (aspect_ratio_range[0] < aspect_ratio < aspect_ratio_range[1]):
        return False

    perimeter = cv2.arcLength(contour, True)
    if perimeter == 0:
        return False

    circularity = 4 * np.pi * (area / (perimeter * perimeter))
    if circularity <= circularity_threshold:
        return False

    hull = cv2.convexHull(contour)
    hull_area = cv2.contourArea(hull)
    solidity = float(area) / hull_area
    if solidity <= solidity_threshold:
        return False

    return True

# Crear directorios si no existen
os.makedirs('data/simulated_fire', exist_ok=True)
os.makedirs('data/masks', exist_ok=True)

# Directorio de las imágenes originales
image_dir = 'data/images'

# Procesar todas las imágenes en el directorio
for i, image_filename in enumerate(os.listdir(image_dir)):
    image_path = os.path.join(image_dir, image_filename)
    
    # Añadir el patrón de fuego a la imagen
    fire_image = add_fire_pattern(image_path, border_noise_level=0.5)
    
    # Crear la máscara de fuego
    fire_mask = create_fire_mask(fire_image, fire_threshold=(230, 239))
    
    # Convertir la máscara a array de numpy y comprobar si contiene píxeles detectados
    fire_mask_np = np.array(fire_mask)
    if np.any(fire_mask_np > 0):  # Si contiene píxeles detectados
        # Guardar la imagen con el patrón de fuego
        fire_image_path = f'data/simulated_fire/frame{i}.jpg'
        fire_image.save(fire_image_path)
        print(f"Imagen de fuego simulado guardada: {fire_image_path}")

        # Guardar la máscara de fuego
        fire_mask_path = f'data/masks/mask_frame{i}.jpg'
        fire_mask.save(fire_mask_path)
        print(f"Máscara de fuego guardada: {fire_mask_path}")
    else:
        print(f"No se detectaron píxeles de fuego en la máscara para la imagen: {image_filename}")

print("Imágenes de fuego simulado y máscaras generadas con éxito.")
