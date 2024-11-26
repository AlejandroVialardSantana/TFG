import os
from PIL import Image

def combine_images(a_dir, b_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    a_images = sorted(os.listdir(a_dir))
    b_images = sorted(os.listdir(b_dir))
    
    for a_img, b_img in zip(a_images, b_images):
        img_a = Image.open(os.path.join(a_dir, a_img))
        img_b = Image.open(os.path.join(b_dir, b_img))
        
        width = img_a.width + img_b.width
        height = max(img_a.height, img_b.height)
        
        combined = Image.new('RGB', (width, height))
        combined.paste(img_a, (0, 0))
        combined.paste(img_b, (img_a.width, 0))
        
        combined.save(os.path.join(output_dir, f"{a_img.split('.')[0]}_combined.jpg"))

combine_images('data-rgbt/train/A', 'data-rgbt/train/B', 'rgb2ir/train')
combine_images('data-rgbt/test/A', 'data-rgbt/test/B', 'rgb2ir/test')