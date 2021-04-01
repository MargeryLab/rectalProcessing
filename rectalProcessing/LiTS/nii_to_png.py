import os
import SimpleITK as itk
import numpy as np
import cv2
import nibabel as nib
import imageio

nii_path = '/media/margery/4ABB9B07DF30B9DB/MedicalImagingDataset/LITS/train/seg'
imgs_png_path = '/media/margery/4ABB9B07DF30B9DB/pythonDemo/medical_image_segmentation/CE-Net/dataset/DRIVE/test/images'
train_tumor_gt_path = '/media/margery/4ABB9B07DF30B9DB/MedicalImagingDataset/LITS/MICCAI-LITS2017-master/data_prepare/train/seg/lesion'
train_liver_gt_path = '/media/margery/4ABB9B07DF30B9DB/MedicalImagingDataset/LITS/MICCAI-LITS2017-master/data_prepare/train/seg/liver'
test_tumor_gt_path = '/media/margery/4ABB9B07DF30B9DB/MedicalImagingDataset/LITS/MICCAI-LITS2017-master/data_prepare/test/seg/lesion'
test_wall_gt_path = '/media/margery/4ABB9B07DF30B9DB/MedicalImagingDataset/LITS/MICCAI-LITS2017-master/data_prepare/test/seg/liver'


def nii_to_png():
    for ID in os.listdir(nii_path):
        index = '00'
        patient_path = os.path.join(nii_path,ID)
        data = itk.ReadImage(patient_path)  #（512,19,512）

        data_arr = itk.GetArrayFromImage(data)  #(512,19,512）
        data_arr[data_arr == 1] = 0
        data_arr[data_arr == 2] = 1
        data_arr[data_arr > 1] = 0
        # data_arr[data_arr > 1] = 0
        data_arr = (data_arr / np.max(data_arr) * 255).astype(np.uint8)

        num = 1
        for i in range(data_arr.shape[0]):
            img = data_arr[i]

            if (index[0] == '0') and (index != '09'):
                index = '0' + str(int(index[-1]) + 1)
            elif index == '09':
                index = '10'
            else:
                index = str(int(index) + 1)
            cv2.imwrite(os.path.join(train_tumor_gt_path, ID[:-4] + '-' + index + '.png'), img)
            num += 1

def png_to_png():
    # data_list = [l.strip('\n') for l in open(os.path.join(DATA_DIR, 'val.txt')).readlines()]
    mask_train_vis = '/media/margery/4ABB9B07DF30B9DB/DARA-SIRRUNRUN/NEW12Month/RectalCancerDataFull/labelRepartion/mask_vis_train'
    mask_test_vis = '/media/margery/4ABB9B07DF30B9DB/DARA-SIRRUNRUN/NEW12Month/RectalCancerDataFull/labelRepartion/mask_vis_test'
    gt_path = mask_test_vis
    data_list = os.listdir(gt_path)
    for i in range(len(data_list)):
        gt_arr = cv2.imread(os.path.join(gt_path, data_list[i]),flags=0)
        tumor_gt = np.copy(gt_arr)
        wall_gt = np.copy(gt_arr)
        tumor_gt[tumor_gt==255] = 0
        tumor_gt[tumor_gt>120] = 255
        wall_gt[wall_gt<128] = 0
        cv2.imwrite(os.path.join(test_tumor_gt_path,data_list[i]),tumor_gt)
        cv2.imwrite(os.path.join(test_wall_gt_path,data_list[i]), wall_gt)
        # cv2.imwrite(os.path.join(test_tumor_gt_path,data_list[i]), tumor_gt)
        # cv2.imwrite(os.path.join(test_wall_gt_path,data_list[i]), wall_gt)

if __name__ == '__main__':
    nii_to_png()
    # png_to_png()