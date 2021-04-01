import os,io
import SimpleITK as sitk
import cv2
import numpy as np
import shutil as sl


test_path = r'D:\RC_DataUnlabelled_Small_Collection'
to_path_HRT2 = r'D:\pythonDemo\medical_image_segmentation\unet-master-copy\data\membrane\new_test\HRT2\image'
to_path_DWI = r'D:\pythonDemo\medical_image_segmentation\unet-master-copy\data\membrane\new_test\DWI\image'


def test_to_png():
    for ID in os.listdir(test_path):
        HRT2_path = os.path.join(test_path,ID,ID,'HRT2')
        DWI_path = os.path.join(test_path,ID,ID,'DWI')

        for dcm in os.listdir(HRT2_path):
            img_hrt2 = sitk.ReadImage(HRT2_path + '/' + dcm)
            img_h_arr = sitk.GetArrayFromImage(img_hrt2)
            img_h_arr = img_h_arr[0, :, :]
            img_h_arr = img_h_arr / (np.max(img_h_arr).astype(np.int16))
            img_h_arr = img_h_arr * 255

            cv2.imwrite(os.path.join(to_path_HRT2, ID + "-" + dcm[0:-4] + ".png"), img_h_arr)

        for dcm in os.listdir(DWI_path):
            img_dwi = sitk.ReadImage(DWI_path + '/' + dcm)
            img_d_arr = sitk.GetArrayFromImage(img_dwi)  # d,h,w
            img_d_arr = img_d_arr[0, :, :]
            img_d_arr = img_d_arr / (np.max(img_d_arr).astype(np.int16))
            img_d_arr = img_d_arr * 255

            cv2.imwrite(os.path.join(to_path_DWI, ID + "-" + dcm[0:-4] + ".png"), img_d_arr)

if __name__ == '__main__':
    shengyi_path = r'D:\pythonDemo\medical_image_segmentation\unet-master-copy\data\membrane\new_test\HRT2\RC_DATA_Pred_2020-09-10\RC_DATA_Pred_only_2020-09-10'
    for case in os.listdir(shengyi_path):
        imgs = sitk.ReadImage(os.path.join(shengyi_path,case))
        imgs_arr = sitk.GetArrayFromImage(imgs)
        for i in range(imgs_arr.shape[0]):
            img = imgs_arr[imgs_arr.shape[0]-i-1, :, :]
            # img = img_arr / (np.max(img_arr).astype(np.int16))
            img = img * 255

            cv2.imwrite(os.path.join(r'D:\pythonDemo\medical_image_segmentation\unet-master-copy\data\membrane\new_test\HRT2\shengyi_png', case[0:-8] + "-" + str(i+1) + ".png"), img)
