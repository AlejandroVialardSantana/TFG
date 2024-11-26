import os
from pathlib import Path

def create_empty_annotations(image_dir):
    annotations_dir = Path(image_dir).parent / "annotations-empty"
    annotations_dir.mkdir(exist_ok=True)

    for filename in os.listdir(image_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            name_without_ext = os.path.splitext(filename)[0]
            
            annotation_file = annotations_dir / f"{name_without_ext}.txt"
            annotation_file.touch()

    print(f"Se han creado archivos de anotación vacíos en {annotations_dir}")

image_directory = "data/pix2pix01/ir_frames"
create_empty_annotations(image_directory)