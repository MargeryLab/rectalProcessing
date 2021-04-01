import math
import random
import os
import SimpleITK as sitk
import cv2
import numpy as np


dcm_path = '/media/margery/4ABB9B07DF30B9DB/DARA-SIRRUNRUN/NEW12Month/RectalCancerDataFull/dcmData'
nii_path = '/media/margery/4ABB9B07DF30B9DB/DARA-SIRRUNRUN/NEW12Month/RectalCancerDataFull/labelData'
output_dir = '/media/margery/4ABB9B07DF30B9DB/DARA-SIRRUNRUN/NEW12Month/RectalCancerDataFull'

train_des_path = '/media/margery/4ABB9B07DF30B9DB/DARA-SIRRUNRUN/NEW12Month/RectalCancerDataFull/datasets/rectalTumor/rectal_tumor_train'
test_des_path = '/media/margery/4ABB9B07DF30B9DB/DARA-SIRRUNRUN/NEW12Month/RectalCancerDataFull/datasets/rectalTumor/rectal_tumor_val'



def dcm_to_png(ID, raw_data_path):
    data_path = os.path.join(raw_data_path,'HRT2')
    if os.path.exists(data_path):
        reader = sitk.ImageSeriesReader()
        dcm_path = reader.GetGDCMSeriesFileNames(data_path)
        reader.SetFileNames(dcm_path)
        imgs = reader.Execute()

        imgs_arr = sitk.GetArrayFromImage(imgs)
        imgs_arr = (imgs_arr / np.max(imgs_arr) * 255).astype(np.uint8)

        index = '00'
        for i in range(imgs_arr.shape[0]):
            if (index[0] == '0') and (index != '09'):
                index = '0' + str(int(index[-1]) + 1)
            elif index == '09':
                index = '10'
            else:
                index = str(int(index) + 1)
            cv2.imwrite(os.path.join(train_des_path,ID+'-'+index+'.png'), imgs_arr[i])
            # cv2.imwrite(os.path.join(test_des_path, ID + '-' + index + '.png'), imgs_arr[i])

def partition_data(dataset_dir, ouput_root):
    """
    Divide the raw data into training sets and validation sets
    :param dataset_dir: path root of dataset
    :param ouput_root: the root path to the output file
    :return:
    """
    image_names = os.listdir(dataset_dir)
    mask_names = []
    val_size = 0.11
    train_names = []
    val_names = []

    rawdata_size = len(os.listdir(dataset_dir))
    random.seed(361)
    val_indices = random.sample(range(0, rawdata_size), math.floor(rawdata_size * val_size))
    train_indices = []
    for i in range(0, rawdata_size):
        if i not in val_indices:
            train_indices.append(i)

    with open(os.path.join(ouput_root, 'val.txt'), 'w') as f:
        for i in val_indices:
            val_names.append(image_names[i])
            f.write(image_names[i][:-7])
            f.write('\n')

    with open(os.path.join(ouput_root, 'train.txt'), 'w') as f:
        for i in train_indices:
            train_names.append(image_names[i])
            f.write(image_names[i][:-7])
            f.write('\n')
    train_names.sort(), val_names.sort()
    return train_names, val_names

def save_img_by_txt(dataset_dir):
    data_list = [l.strip('\n') for l in open(os.path.join(dataset_dir, 'train.txt')).readlines()]
    # data_list = [l.strip('\n') for l in open(os.path.join(dataset_dir, 'val.txt')).readlines()]
    for i in range(len(data_list)):
        slice_path = os.path.join(dataset_dir,'dcmData',data_list[i],data_list[i])
        dcm_to_png(data_list[i], slice_path)

def nii_to_png(patient_path,ID):
    index = '00'
    data = sitk.ReadImage(patient_path)  #（512,19,512）

    data_arr_ = sitk.GetArrayFromImage(data)  #(512,19,512）
    data_arr_[data_arr_ == 4] = 1   #黄色交界处定义为肿瘤
    data_arr_[data_arr_ > 2] = 0
    data_arr = (data_arr_ / np.max(data_arr_) * 255).astype(np.uint8)
    if data_arr.shape[0] > 100 and data_arr.shape[1] < 100:
        data_arr = data_arr.transpose(1, 2, 0)
    elif data_arr.shape[2] < 100:
        data_arr = data_arr.transpose(2, 0, 1)
        print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")

    num = 1
    masks_train_path ='/media/margery/4ABB9B07DF30B9DB/DARA-SIRRUNRUN/NEW12Month/RectalCancerDataFull/labelRepartion/mask_vis_train'
    masks_test_path = '/media/margery/4ABB9B07DF30B9DB/DARA-SIRRUNRUN/NEW12Month/RectalCancerDataFull/labelRepartion/mask_vis_test'
    for i in range(data_arr.shape[0]):
        if (index[0] == '0') and (index != '09'):
            index = '0' + str(int(index[-1]) + 1)
        elif index == '09':
            index = '10'
        else:
            index = str(int(index) + 1)
        # cv2.imwrite(os.path.join(masks_png_path,ID[:-7]+'-'+index+'.png'),img)
        # cv2.imwrite(os.path.join(masks_png_path,ID+'-'+str(num)+'.png'),label_arr[index])
        # cv2.imwrite(os.path.join(masks_train_path,ID+'-'+index+'.png'),data_arr[i])
        cv2.imwrite(os.path.join(masks_test_path, ID + '-' + index + '.png'), data_arr[i])
        num += 1

def save_mask_by_txt():
    dataset_dir = '/media/margery/4ABB9B07DF30B9DB/DARA-SIRRUNRUN/NEW12Month/RectalCancerDataFull'

    # data_list = [l.strip('\n') for l in open(os.path.join(dataset_dir, 'train.txt')).readlines()]
    data_list = [l.strip('\n') for l in open(os.path.join(dataset_dir, 'val.txt')).readlines()]
    for i in range(len(data_list)):
        patient_mask_path = os.path.join(dataset_dir,'labelData',data_list[i]+'_HT.nii')
        nii_to_png(patient_mask_path,data_list[i])


if __name__ == '__main__':
    partition_data(nii_path,output_dir)
    dataset_dir = '/media/margery/4ABB9B07DF30B9DB/DARA-SIRRUNRUN/NEW12Month/RectalCancerDataFull'
    # save_img_by_txt(dataset_dir)
    save_mask_by_txt()