import cv2
import numpy as np
from pathlib import Path

def dhash(image, hash_size = 8):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    resized = cv2.resize(gray, (hash_size + 1, hash_size))
    diff = resized[:, 1:] > resized[:, :-1]
    return sum([2 ** i for (i, v) in enumerate(diff.flatten()) if v])

def are_images_similar(img1, img2, threshold=0.85):
    hash1 = dhash(img1)
    hash2 = dhash(img2)
    similarity = 1 - (bin(hash1 ^ hash2).count("1") / 64)
    return similarity > threshold

def process_images(input_dir, output_dir):
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    image_files = list(input_path.glob('*.jpg')) + list(input_path.glob('*.png'))
    unique_images = []

    for i, img_file in enumerate(image_files):
        print(f"Processing image {i+1}/{len(image_files)}")
        img = cv2.imread(str(img_file))
        
        is_unique = True
        for unique_img in unique_images:
            if are_images_similar(img, unique_img):
                is_unique = False
                break
        
        if is_unique:
            unique_images.append(img)
            cv2.imwrite(str(output_path / img_file.name), img)

    print(f"Processed {len(image_files)} images. {len(unique_images)} unique images saved.")

input_directory = "data/imagenes-ir-procesar"
output_directory = "data/unique-images"
process_images(input_directory, output_directory)