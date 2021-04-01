import SimpleITK as sitk
import os
import skimage.io as io
import cv2
from numpy import random

data_path = r'D:\pythonDemo\medical_image_segmentation\unet-master-copy-1\data\image'
label_path = r'D:\pythonDemo\medical_image_segmentation\unet-master-copy-1\data\label'
to_img_path = r'D:\pythonDemo\medical_image_segmentation\unet-master-copy-1\data\membrane\train\image'
to_label_path = r'D:\pythonDemo\medical_image_segmentation\unet-master-copy-1\data\membrane\train\label'
data = []
label = []
name = []

if __name__ == '__main__':
    for img in os.listdir(data_path):
        img_path = os.path.join(data_path,img)
        img_arr = io.imread(img_path, as_gray=False)
        data.append(img_arr)
        name.append(img)
    for l in os.listdir(label_path):
        lab_path = os.path.join(label_path,l)
        label_arr = io.imread(lab_path, as_gray=False)
        label.append(label_arr)

    index = [i for i in range(len(data))]
    for iter in range(16):
        random.shuffle(index)

    imgs = []
    labels = []
    names = []

    for i in range(len(index)):
        print(data[index[i]])
        imgs.append(data[index[i]])
        labels.append(label[index[i]])
        names.append(name[index[i]])

    for j in range(len(imgs)):
        cv2.imwrite(os.path.join(to_img_path,names[j]),imgs[j])

    for k in range(len(labels)):
        cv2.imwrite(os.path.join(to_label_path,names[k]),labels[k])
