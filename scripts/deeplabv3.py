import torch
import numpy as np
import cv2
from torchvision import models, transforms
from PIL import Image

# Load the images
background = cv2.imread('data/images/frame0.jpg')
fire_ship_image = Image.open('data/oil-rig-explosion-618704_1920_real_A.png')

# Check if images are loaded correctly
if background is None:
    raise FileNotFoundError("Background image not loaded correctly.")
if fire_ship_image is None:
    raise FileNotFoundError("Fire ship image not loaded correctly.")

# Convert the fire ship image to a NumPy array
fire_ship_image_rgb = np.array(fire_ship_image)

# Keep a copy of the original fire ship image for blending
original_fire_ship_image = fire_ship_image_rgb.copy()

# Configure the segmentation model
weights = models.segmentation.DeepLabV3_ResNet101_Weights.COCO_WITH_VOC_LABELS_V1
model = models.segmentation.deeplabv3_resnet101(weights=weights).eval()

# Preprocess the fire ship image for segmentation
preprocess = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

input_tensor = preprocess(fire_ship_image)
input_batch = input_tensor.unsqueeze(0)

# Perform segmentation
with torch.no_grad():
    output = model(input_batch)['out'][0]
output_predictions = output.argmax(0)

# Create a binary mask for the 'boat' class (index 4)
boat_mask = output_predictions == 4
boat_mask = boat_mask.byte().cpu().numpy()

# Resize the mask and segmented image to match the background size
boat_mask_resized = cv2.resize(boat_mask, (background.shape[1], background.shape[0]), interpolation=cv2.INTER_NEAREST)
fire_ship_resized = cv2.resize(original_fire_ship_image, (background.shape[1], background.shape[0]))

# Create an image with the fire ship and a black background
fire_ship_segmented = cv2.bitwise_and(fire_ship_resized, fire_ship_resized, mask=boat_mask_resized.astype(np.uint8))

# Create the alpha mask for blending
alpha_mask = boat_mask_resized.astype(float)

# Create a copy of the background image for blending
blended_image = background.copy()

# Apply alpha blending
for c in range(0, 3):
    blended_image[:, :, c] = (alpha_mask * fire_ship_segmented[:, :, c] +
                              (1 - alpha_mask) * background[:, :, c])

# Display and save the resulting image
cv2.imshow('Blended Image', blended_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Save the resulting image
cv2.imwrite('data/blended_image_segmented.jpg', blended_image)
