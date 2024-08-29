import os
import shutil
import random

def split_dataset(images_dir, labels_dir, output_dir, split_ratio=(0.7, 0.15, 0.15)):
    yolo_ir_dir = os.path.join(output_dir, 'yolo-ir-v2')
    train_images_dir = os.path.join(yolo_ir_dir, 'train', 'images')
    train_labels_dir = os.path.join(yolo_ir_dir, 'train', 'labels')
    val_images_dir = os.path.join(yolo_ir_dir, 'valid', 'images')
    val_labels_dir = os.path.join(yolo_ir_dir, 'valid', 'labels')
    test_images_dir = os.path.join(yolo_ir_dir, 'test', 'images')
    test_labels_dir = os.path.join(yolo_ir_dir, 'test', 'labels')

    for dir in [train_images_dir, train_labels_dir, val_images_dir, val_labels_dir, test_images_dir, test_labels_dir]:
        os.makedirs(dir, exist_ok=True)

    image_files = [f for f in os.listdir(images_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    print(f"Found {len(image_files)} image files.")

    valid_image_files = [f for f in image_files if os.path.exists(os.path.join(labels_dir, os.path.splitext(f)[0] + '.txt'))]
    print(f"Found {len(valid_image_files)} images with corresponding labels.")

    random.shuffle(valid_image_files)

    total_files = len(valid_image_files)
    train_count = int(total_files * split_ratio[0])
    val_count = int(total_files * split_ratio[1])
    test_count = total_files - train_count - val_count

    train_files = valid_image_files[:train_count]
    val_files = valid_image_files[train_count:train_count+val_count]
    test_files = valid_image_files[train_count+val_count:]

    def move_files(files, src_img_dir, src_lbl_dir, dst_img_dir, dst_lbl_dir):
        for file_name in files:
            base_name = os.path.splitext(file_name)[0]
            img_src_path = os.path.join(src_img_dir, file_name)
            lbl_src_path = os.path.join(src_lbl_dir, base_name + '.txt')
            img_dst_path = os.path.join(dst_img_dir, file_name)
            lbl_dst_path = os.path.join(dst_lbl_dir, base_name + '.txt')

            if os.path.exists(img_src_path) and os.path.exists(lbl_src_path):
                shutil.copy(img_src_path, img_dst_path)
                shutil.copy(lbl_src_path, lbl_dst_path)
            else:
                print(f"Warning: Missing file for {file_name}")

    move_files(train_files, images_dir, labels_dir, train_images_dir, train_labels_dir)
    move_files(val_files, images_dir, labels_dir, val_images_dir, val_labels_dir)
    move_files(test_files, images_dir, labels_dir, test_images_dir, test_labels_dir)

    print(f"Dataset split completed. Train: {len(train_files)} files, Validation: {len(val_files)} files, Test: {len(test_files)} files.")

images_dir = 'imagenes-ir-v2'
labels_dir = 'yolo-annotations'
output_dir = 'data-v3'
split_ratio = (0.7, 0.2, 0.1)

split_dataset(images_dir, labels_dir, output_dir, split_ratio)