"""

获取可用于训练网络的训练数据集
需要四十分钟左右,产生的训练数据大小3G左右
"""

import os
import sys

import cv2

sys.path.append(os.path.split(sys.path[0])[0])
import shutil
from time import time

import numpy as np
from tqdm import tqdm
import SimpleITK as sitk
import scipy.ndimage as ndimage

raw_path = '/media/margery/4ABB9B07DF30B9DB/MedicalImagingDataset/Pancreas-CT/manifest-1599750808610/Pancreas-CT'
label_path = '/media/margery/4ABB9B07DF30B9DB/MedicalImagingDataset/Pancreas-CT/TCIA_pancreas_labels-02-05-2017'

if os.path.exists('./train'):
    shutil.rmtree('./train')

new_ct_path = os.path.join('./train', 'ct')
new_seg_dir = os.path.join('./train', 'seg')

os.mkdir('./train')
os.mkdir(new_ct_path)
os.mkdir(new_seg_dir)

start = time()
num = 0
reader = sitk.ImageSeriesReader()
writer = sitk.ImageSeriesWriter()
for case in tqdm(os.listdir(raw_path)):
    num += 1
    fist_path = os.path.join(raw_path,case)
    for f in os.listdir(fist_path):
        sec_path = os.path.join(fist_path,f)
        for ff in os.listdir(sec_path):
            thir_path = os.path.join(sec_path, ff)
            # 将CT和金标准入读内存
            dcm_path = reader.GetGDCMSeriesFileNames(thir_path)
            reader.SetFileNames(dcm_path)
            imgs = reader.Execute()
            ct_array = sitk.GetArrayFromImage(imgs)

            if num == 25 or num==70:
                num+=1
            if num <10:
                seg = sitk.ReadImage(os.path.join(label_path, 'label000'+str(num)+'.nii.gz'), sitk.sitkUInt8)
            else:
                seg = sitk.ReadImage(os.path.join(label_path, 'label00' + str(num) + '.nii.gz'), sitk.sitkUInt8)
            seg_array = sitk.GetArrayFromImage(seg)

            # 将金标准中肝脏和肝肿瘤的标签融合为一个
            # seg_array[seg_array > 0] = 1

            # 将灰度值在阈值之外的截断掉
            ct_array[ct_array > 200] = 200
            ct_array[ct_array < -200] = -200

            # 对CT数据在横断面上进行降采样,并进行重采样,将所有数据的z轴的spacing调整到1mm
            ct_array = ndimage.zoom(ct_array, (imgs.GetSpacing()[-1] / 1, 1, 1), order=3)
            seg_array = ndimage.zoom(seg_array, (imgs.GetSpacing()[-1] / 1, 1, 1), order=0)

            # 找到肝脏区域开始和结束的slice
            z = np.any(seg_array, axis=(1, 2))
            start_slice, end_slice = np.where(z)[0][[0, -1]]
            print(start_slice, end_slice)

            # 两个方向上各扩张slice
            # start_slice = max(0, start_slice - para.expand_slice)
            # end_slice = min(seg_array.shape[0] - 1, end_slice + para.expand_slice)

            # 如果这时候剩下的slice数量不足size，直接放弃该数据，这样的数据很少,所以不用担心
            # if end_slice - start_slice + 1 < para.size:
            #     print('!!!!!!!!!!!!!!!!')
            #     print(file, 'have too little slice', ct_array.shape[0])
            #     print('!!!!!!!!!!!!!!!!')
            #     continue

            ct_array = ct_array[start_slice:end_slice + 1, :, :]
            seg_array = seg_array[start_slice:end_slice + 1, :, :]

            # 最终将数据保存为nii
            new_ct = sitk.GetImageFromArray(ct_array)

            new_ct.SetDirection(imgs.GetDirection())
            new_ct.SetOrigin(imgs.GetOrigin())
            new_ct.SetSpacing((imgs.GetSpacing()[0] * int(1 / 1), imgs.GetSpacing()[1] * int(1 / 1), 1))

            new_ct_arr = sitk.GetArrayFromImage(new_ct)
            # new_ct_arr = (new_ct_arr / np.max(new_ct_arr) * 255).astype(np.int16)

            new_seg = sitk.GetImageFromArray(seg_array)

            new_seg.SetDirection(imgs.GetDirection())
            new_seg.SetOrigin(imgs.GetOrigin())
            new_seg.SetSpacing((imgs.GetSpacing()[0], imgs.GetSpacing()[1], 1))

            new_seg_arr = sitk.GetArrayFromImage(new_seg)
            new_seg_arr = (new_seg_arr / np.max(new_seg_arr) * 255).astype(np.uint8)

            if num < 10:
                index = 0
                for i in range(new_ct_arr.shape[0]):
                    index+=1
                    if index <10:
                        cv2.imwrite(os.path.join(new_ct_path, 'PANCREAS0' + str(num)+'-00'+str(index) + '.png'), new_ct_arr[i])
                        cv2.imwrite(os.path.join(new_seg_dir, 'PANCREAS0' + str(num)+'-00' + str(index) + '.png'),
                                    new_seg_arr[i])
                    elif (index >=10 and index<100):
                        cv2.imwrite(os.path.join(new_ct_path, 'PANCREAS0' + str(num)+'-0' + str(index) + '.png'),
                                    new_ct_arr[i])
                        cv2.imwrite(os.path.join(new_seg_dir, 'PANCREAS0' + str(num)+'-0' + str(index) + '.png'),
                                    new_seg_arr[i])
                    else:
                        cv2.imwrite(os.path.join(new_ct_path, 'PANCREAS0' + str(num)+'-' + str(index) + '.png'),
                                    new_ct_arr[i])
                        cv2.imwrite(os.path.join(new_seg_dir, 'PANCREAS0' + str(num)+'-' + str(index) + '.png'),
                                    new_seg_arr[i])
                # sitk.WriteImage(new_ct, os.path.join(new_seg_dir, 'PANCREAS_000' + str(num) + '.nii'))
                # sitk.WriteImage(new_seg, os.path.join(new_ct_path, 'PANCREAS_000' + str(num) + '.nii'))
            else:
                index = 0
                for i in range(new_ct_arr.shape[0]):
                    index += 1
                    if index < 10:
                        cv2.imwrite(os.path.join(new_ct_path, 'PANCREAS' + str(num)+'-00' + str(index) + '.png'),
                                    new_ct_arr[i])
                        cv2.imwrite(os.path.join(new_seg_dir, 'PANCREAS' + str(num)+'-00' + str(index) + '.png'),
                                    new_seg_arr[i])
                    elif (index >= 10 and index < 100):
                        cv2.imwrite(os.path.join(new_ct_path, 'PANCREAS' + str(num)+'-0' + str(index) + '.png'),
                                    new_ct_arr[i])
                        cv2.imwrite(os.path.join(new_seg_dir, 'PANCREAS' + str(num)+'-0' + str(index) + '.png'),
                                    new_seg_arr[i])
                    else:
                        cv2.imwrite(os.path.join(new_ct_path, 'PANCREAS_0' + str(num)+'-' + str(index) + '.png'),
                                    new_ct_arr[i])
                        cv2.imwrite(os.path.join(new_seg_dir, 'PANCREAS_0' + str(num)+'-' + str(index) + '.png'),
                                    new_seg_arr[i])