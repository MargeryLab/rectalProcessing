import math
import os
import random
import shutil

cell_path = '/media/margery/4ABB9B07DF30B9DB/MedicalImagingDataset/nucleiSeg/stage1_train'
des_path = '/media/margery/4ABB9B07DF30B9DB/MedicalImagingDataset/nucleiSeg/celliImg'
txt_des_path = '/media/margery/4ABB9B07DF30B9DB/MedicalImagingDataset/nucleiSeg'
cell_train_img = '/media/margery/4ABB9B07DF30B9DB/MedicalImagingDataset/nucleiSeg/cell_train_img'
cell_train_mask = '/media/margery/4ABB9B07DF30B9DB/MedicalImagingDataset/nucleiSeg/cell_train_mask'
cell_test_img = '/media/margery/4ABB9B07DF30B9DB/MedicalImagingDataset/nucleiSeg/cell_test_img'
cell_test_mask = '/media/margery/4ABB9B07DF30B9DB/MedicalImagingDataset/nucleiSeg/cell_test_mask'


def partition_data(dataset_dir, ouput_root):
    image_names = os.listdir(dataset_dir)
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
            f.write(image_names[i])
            f.write('\n')

    with open(os.path.join(ouput_root, 'train.txt'), 'w') as f:
        for i in train_indices:
            train_names.append(image_names[i])
            f.write(image_names[i])
            f.write('\n')
    train_names.sort(), val_names.sort()
    return train_names, val_names

def save_img_by_txt():
    # data_list = [l.strip('\n') for l in open(os.path.join(txt_des_path, 'train.txt')).readlines()]
    data_list = [l.strip('\n') for l in open(os.path.join(txt_des_path, 'val.txt')).readlines()]
    # count = 100001
    count = 100598
    for i in range(len(data_list)):
        img_dir_path = os.path.join(cell_path,data_list[i],'images')
        mask_dir_path = os.path.join(cell_path,data_list[i],'masks')
        kk = 0
        for img in os.listdir(img_dir_path):
            if kk > 0:
                print(kk)
            img_path = os.path.join(img_dir_path, img)
            # shutil.copy(img_path, os.path.join(cell_train_img, str(count) +'.png'))
            shutil.copy(img_path, os.path.join(cell_test_img, str(count) + '.png'))
            kk += 1

        j = 1
        for mask in os.listdir(mask_dir_path):
            mask_path = os.path.join(mask_dir_path, mask)
            if j<10:
                # shutil.copy(mask_path,os.path.join(cell_train_mask, str(count) + '-0'+str(j) + '.png'))
                shutil.copy(mask_path, os.path.join(cell_test_mask, str(count) + '-0' + str(j) + '.png'))
            else:
                # shutil.copy(mask_path, os.path.join(cell_train_mask, str(count) + '-'+str(j) + '.png'))
                shutil.copy(mask_path, os.path.join(cell_test_mask, str(count) + '-' + str(j) + '.png'))
            j += 1
        count += 1


if __name__ == '__main__':
    # partition_data(cell_path,txt_des_path)
    save_img_by_txt()
