import os
import shutil
import cv2

test_mask_path = r'D:\pythonDemo\medical_image_segmentation\CE-Net\dataset\DRIVE\test\masks'
test_img_path = r'D:\pythonDemo\medical_image_segmentation\CE-Net\dataset\DRIVE\test\images'
train_imgs_path = r'D:\pythonDemo\medical_image_segmentation\CE-Net\dataset\DRIVE\training\images'


lowresult_img_path = r'D:\pythonDemo\medical_image_segmentation\CE-Net\dataset\DRIVE\error_img'
lowresult_mask_path = r'D:\pythonDemo\medical_image_segmentation\CE-Net\dataset\DRIVE\error_mask'

if __name__ == '__main__':
    png_name = []
    for name in os.listdir(lowresult_img_path):
        # png_name.append(name)
        train_img_path = os.path.join(test_mask_path, name)
        shutil.move(train_img_path, os.path.join(lowresult_mask_path, name))
