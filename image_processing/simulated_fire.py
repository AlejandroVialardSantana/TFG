import cv2
import numpy as np
import random
from image_processing.perlin_noise import generate_perlin_noise_2d
from image_processing.image_processor import measure_blur

def calculate_threshold_value(image):
    mean_brightness = np.mean(image)
    return max(200, min(255, mean_brightness + 50))

def generate_fire_area(fire_size):
    fire_area = generate_perlin_noise_2d((fire_size, fire_size), (4, 4))
    fire_area = (fire_area - fire_area.min()) / (fire_area.max() - fire_area.min())
    fire_area = (fire_area * 255).astype(np.uint8)
    _, fire_area = cv2.threshold(fire_area, 128, 255, cv2.THRESH_BINARY)
    return fire_area

def find_largest_contours(image, threshold_value, num_contours=5):
    _, thresholded = cv2.threshold(image, threshold_value, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresholded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    return contours, thresholded

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