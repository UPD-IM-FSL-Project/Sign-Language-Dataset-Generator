
import numpy as np
import cv2
import os
from image_feed import ImageFeed

# ====================================================== #
# Settings
output_format = "png" # Supports square outputs for now
# ------------------------ #
# Properties you can add randomness to
random_brightness = True # brightness
random_hflip = True # horizontal flip
random_rotation = True # rotation
# ------------------------ #
# Magnitude of the randomness
brightness_magnitude = 30 # for brightness
rotation_magnitude = 10 # for rotation in degrees
# ====================================================== #
# Call process_all() if you want to process all the folders in the output_images folder
# Call process(folder_name) if you want to process a specific folder in the output_images folder
# ====================================================== #

folder_path = "output_images"

image_folders = [f for f in os.listdir(folder_path)]

def randomize(folder: str):
    output_dir = f"randomized_images\{folder}"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    cap = ImageFeed("output_images/"+folder, loop=False)
    frame_count = 0
    while True:
        frame_count += 1
        ret, frame = cap.read()
        if not ret:
            break
        (h, w) = frame.shape[:2]
        randomize = np.random.randint(-30, 30) if random_brightness or random_hflip else 0
        frame = np.clip(frame + randomize, 0, 255).astype(np.uint8)
        frame = cv2.flip(frame,1) if randomize % 2 == 0 else frame
        angle = 0
        center = (w // 2, h // 2)
        rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
        frame = cv2.warpAffine(frame, rotation_matrix, (w, h))
        cv2.imwrite(f"{output_dir}\{frame_count}.{output_format}", frame)

def randomize_all():
    for folder in image_folders:
        randomize(folder)

randomize_all()

