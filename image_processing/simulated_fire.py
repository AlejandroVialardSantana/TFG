import cv2
import numpy as np
import random
from PIL import Image, ImageDraw
from image_processing.perlin_noise import generate_perlin_noise_2d
from image_processing.image_processor import measure_blur

# Funciones comunes

def calculate_threshold_value(image):
    mean_brightness = np.mean(image)
    return max(200, min(255, mean_brightness + 50))

def generate_fire_area(fire_size):
    fire_area = generate_perlin_noise_2d((fire_size, fire_size), (4, 4))
    fire_area = (fire_area - fire_area.min()) / (fire_area.max() - fire_area.min())
    fire_area = (fire_area * 255).astype(np.uint8)
    _, fire_area = cv2.threshold(fire_area, 128, 255, cv2.THRESH_BINARY)
    return fire_area

def find_largest_contours(image, threshold_value, min_contour_area=100, max_contour_area=5000):
    _, thresholded = cv2.threshold(image, threshold_value, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Filtrar contornos por tamaño
    filtered_contours = [contour for contour in contours if min_contour_area <= cv2.contourArea(contour) <= max_contour_area]
    
    filtered_contours = sorted(filtered_contours, key=cv2.contourArea, reverse=True)
    return filtered_contours, thresholded

def add_fire_to_region(output_image, contour, min_fire_size, max_fire_size, thresholded, blur_kernel_size):
    x, y, w, h = cv2.boundingRect(contour)
    if w < min_fire_size or h < min_fire_size:
        print(f"Región demasiado pequeña: w={w}, h={h}")
        return False
    
    fire_size = random.randint(min_fire_size, min(max_fire_size, w, h))
    x_fire = random.randint(x, x + w - fire_size)
    y_fire = random.randint(y, y + h - fire_size)

    fire_area = generate_fire_area(fire_size)
    fire_area = cv2.GaussianBlur(fire_area, (blur_kernel_size, blur_kernel_size), 0)

    fire_size = min(fire_area.shape[0], fire_area.shape[1])
    fire_area = fire_area[:fire_size, :fire_size]

    fire_mask = fire_area > 128
    if np.any(thresholded[y_fire:y_fire + fire_size, x_fire:x_fire + fire_size][fire_mask]):
        output_image[y_fire:y_fire + fire_size, x_fire:x_fire + fire_size][fire_mask] = fire_area[fire_mask]
        return True
    else:
        print(f"No se puede agregar fuego en la región seleccionada: ({x_fire}, {y_fire}) de tamaño {fire_size}")
        return False

def add_fire(image, num_fire_areas=3, min_fire_size=30, max_fire_size=150):
    output_image = image.copy()
    threshold_value = calculate_threshold_value(image)
    blur_amount = measure_blur(image)
    blur_kernel_size = max(5, int(30 / (blur_amount + 1e-6)))
    contours, thresholded = find_largest_contours(image, threshold_value)

    fire_added = False
    for _ in range(num_fire_areas * 2):
        if not contours:
            print("No se encontraron contornos.")
            break
        contour = random.choice(contours)
        if add_fire_to_region(output_image, contour, min_fire_size, max_fire_size, thresholded, blur_kernel_size):
            fire_added = True
            break

    if not fire_added:
        print("No se pudo agregar fuego en la imagen.")
        return None

    return output_image

# Funciones específicas para el patrón definido con PIL

FIRE_VALUE = 235  # Valor medio entre 230 y 239
BORDER_VALUES = [135, 190]

def expand_fire(image, position, fire_radius, border_radius, intensity=0.8):
    draw = ImageDraw.Draw(image)
    x, y = position
    for i in range(-border_radius, border_radius):
        for j in range(-border_radius, border_radius):
            distance = np.sqrt(i**2 + j**2)
            if distance < fire_radius:
                if random.random() < intensity:
                    alpha = int(255 * (1 - distance / fire_radius))
                    draw.point((x + i, y + j), fill=(FIRE_VALUE, FIRE_VALUE, FIRE_VALUE, alpha))
            elif distance < border_radius:
                if random.random() < intensity * (1 - (distance - fire_radius) / (border_radius - fire_radius)):
                    alpha = int(255 * (1 - (distance - fire_radius) / (border_radius - fire_radius)))
                    border_value = BORDER_VALUES[0] + (BORDER_VALUES[1] - BORDER_VALUES[0]) * (1 - (distance - fire_radius) / (border_radius - fire_radius))
                    draw.point((x + i, y + j), fill=(int(border_value), int(border_value), int(border_value), alpha))

def add_fire_pattern(image_path, num_fires=3):
    target_image = Image.open(image_path)
    target_image_with_fire = Image.new('RGBA', target_image.size)
    target_image_with_fire.paste(target_image)

    # Convertir la imagen a escala de grises y detectar áreas blancas
    grayscale_image = target_image.convert('L')
    threshold_value = 250  # Establecer un valor de umbral alto para detectar áreas blancas
    contours, _ = find_largest_contours(np.array(grayscale_image), threshold_value, min_contour_area=500, max_contour_area=5000)

    for _ in range(num_fires):
        if not contours:
            print("No se encontraron contornos.")
            break
        contour = random.choice(contours)
        x, y, w, h = cv2.boundingRect(contour)
        pos = (random.randint(x, x + w), random.randint(y, y + h))
        fire_radius = random.randint(10, 30)
        border_radius = fire_radius + random.randint(10, 20)
        expand_fire(target_image_with_fire, pos, fire_radius, border_radius)

    return target_image_with_fire.convert('RGB')

def create_fire_mask(image, fire_threshold=(230, 239)):
    grayscale_image = image.convert('L')
    mask = np.array(grayscale_image)
    fire_mask = np.where((mask >= fire_threshold[0]) & (mask <= fire_threshold[1]), 255, 0)
    return Image.fromarray(fire_mask.astype(np.uint8))
