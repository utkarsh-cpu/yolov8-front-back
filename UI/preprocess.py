import cv2
import albumentations as A
from albumentations.core.composition import OneOf
import os

# ui_backend/preprocess.py

import cv2
import os

def preprocess_image(input_path, output_path, resize=None, grayscale=False, normalize=False):
    img = cv2.imread(input_path)
    if img is None:
        raise FileNotFoundError(f"Could not read input image: {input_path}")

    # 1. Resize
    if resize and len(resize) == 2:
        width, height = resize
        img = cv2.resize(img, (width, height), interpolation=cv2.INTER_AREA)

    # 2. Grayscale
    if grayscale:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 3. Normalize
    if normalize:
        img = img.astype('float32') / 255.0
        # If we want to actually save it in standard 8-bit format, revert:
        img = (img * 255).clip(0, 255).astype('uint8')

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Write
    cv2.imwrite(output_path, img)
    return output_path

# Augmentation of Image is Using Albumentations, got this idea using this link
# https://www.kaggle.com/code/parulpandey/overview-of-popular-image-augmentation-packages#5.-Data-Augmentation-using-Augmentor
# Augmentation pipeline
augmentation_pipeline = A.Compose([
    A.HorizontalFlip(p=0.5),
    A.VerticalFlip(p=0.5),
    A.RandomBrightnessContrast(p=0.5),
    A.ShiftScaleRotate(shift_limit=0.0625, scale_limit=0.1, rotate_limit=45, p=0.5),
    OneOf([
        A.MotionBlur(p=0.2),
        A.MedianBlur(blur_limit=3, p=0.1),
        A.GaussianBlur(blur_limit=3, p=0.1),
    ], p=0.5),
    A.RandomSizedCrop(min_max_height=(480, 640), height=640, width=640, p=0.5),
])


def augment_image(image):

    augmented = augmentation_pipeline(image=image)
    return augmented['image']



'''
# Example usage
if __name__ == "__main__":
    input_image = "Picture1.png"
    preprocess_image(image_path=input_dir)
'''