import os

dir_imagenes = 'imagenes-ir-v2'
dir_anotaciones = 'yolo-annotations'

imagenes = set(os.path.splitext(f)[0] for f in os.listdir(dir_imagenes) if f.lower().endswith(('.png', '.jpg', '.jpeg')))

for archivo in os.listdir(dir_anotaciones):
    if archivo.endswith('.txt'):
        nombre_base = os.path.splitext(archivo)[0]
        
        if nombre_base not in imagenes:
            ruta_completa = os.path.join(dir_anotaciones, archivo)
            os.remove(ruta_completa)
            print(f"Archivo borrado: {archivo}")

print("Proceso completado.")