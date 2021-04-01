import os
import SimpleITK as sitk
import numpy as np


data_path = r'D:\pythonDemo\medical_image_segmentation\Unet-1\RectalCancerU2\1000450\1000450'
mask_path = r'D:\pythonDemo\medical_image_segmentation\Unet-1\RectalCancerU2\1000450\mask'

# image_slices = [sitk.ReadImage(data_path + '/' + s) for s in os.listdir(data_path)]
for data in os.listdir(data_path):
    print(os.path.join(data_path,data))
    data_arr = sitk.ReadImage(os.path.join(data_path,data))


def getRangImageDepth(image):
    firstflag = True
    startposition = 0
    endposition = 0
    for z in range(image.shape[0]):
        notzeroflag = np.max(image[z])
        if notzeroflag and firstflag:
            startposition = z
            firstflag = False
        if notzeroflag:
            endposition = z
    return startposition, endposition


