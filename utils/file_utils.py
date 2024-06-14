import os
import cv2

def create_folder_if_not_exists(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

def process_images(source_folder, target_folder, process_function, process_function_args=None, file_suffix=''):
    create_folder_if_not_exists(target_folder)

    for filename in os.listdir(source_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(source_folder, filename)
            save_path = os.path.join(target_folder, f'{file_suffix}{filename}')
            
            image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            if image is not None:
                processed_image = process_function(image, *process_function_args) if process_function_args else process_function(image)
                if processed_image is not None:
                    cv2.imwrite(save_path, processed_image)
                    print(f'Archivo procesado guardado en: {save_path}')
