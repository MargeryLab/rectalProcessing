import os,io
import SimpleITK as sitk
import cv2
import numpy as np
import shutil as sl

raw_data_path = '/media/margery/4ABB9B07DF30B9DB/DARA-SIRRUNRUN/MengPing_20210303/dcmData'
png_path = '/media/margery/4ABB9B07DF30B9DB/DARA-SIRRUNRUN/MengPing_20210303/140PNG'
label_path = '/media/margery/b44160de-00cb-402a-ba45-d81240edf8a4/DeepLearningDemo/NEW12Month/RectalCancerDataFull/labelData'

"""
新数据处理流程：
/media/margery/b44160de-00cb-402a-ba45-d81240edf8a4/DeepLearningDemo/NEW12Month/RectalCancerDataFull/dcmData为源数据
/media/margery/b44160de-00cb-402a-ba45-d81240edf8a4/DeepLearningDemo/NEW12Month/RectalCancerDataFull/labelData
为标注数据，新的数据可以删除该文件下所有数据全部替换掉
1、删除/media/margery/4ABB9B07DF30B9DB/pythonDemo/medical_image_segmentation/Data/data_png_png三个文件夹下的图片
2、执行dcm_to_png将dcm转png
3、执行niinii_to_pngpng下的nii_to_png
4、执行repartion_dataset.py下的partition_data随机划分训练集和测试集，存为train.txt\val.txt
5、根据txt存储png

png转json
1、删除/media/margery/4ABB9B07DF30B9DB/pythonDemo/tools/prepare_detection_dataset下几个文件夹的图片
2、执行nii_to_png_forjson.py下的方法png_to_png
3、project /media/margery/4ABB9B07DF30B9DB/pythonDemo/tools/prepare_detection_dataset下执行extract_box.py
"""
# 终版
def dcm_to_png():
    # id_ls = [id[:-7] for id in os.listdir(label_path)]
    # print(len(id_ls))
    for ID in os.listdir(raw_data_path):
        # if ID not in id_ls:
        #     continue
        data_path = os.path.join(raw_data_path, ID, ID, 'HRT2')
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
                cv2.imwrite(os.path.join(png_path,ID+'-'+index+'.png'), imgs_arr[i])


# def dcm_to_png():
#     for ID in os.listdir(train_path):
#         i = 0
#         data_path = os.path.join(train_path,ID,ID,'HRT2')
#         mask_nii = ID+'.nii'
#         if os.path.exists(data_path):
#             for s in os.listdir(data_path):
#                 if s != mask_nii:
#                     i += 1
#                     image = sitk.ReadImage(data_path + '/' + s) #w,h,d
#                     image_array = sitk.GetArrayFromImage(image) #d,h,w
#
#                     # image_array = np.fliplr(np.flipud(image_array))
#                     ddd = image_array[0,:,:]
#                     ddd = ddd / (np.max(ddd).astype(np.uint16))
#                     # ddd /= np.max(ddd).astype(np.uint16)
#                     ddd = ddd * 255
#
#                     png_path = os.path.join(r'D:\pythonDemo\medical_image_segmentation\unet-master\data\membrane\train\image')
#                     cv2.imwrite(os.path.join(png_path,ID+"-"+str(i)+".png"),ddd)


def IDname_to_num():
    data_path = r'D:\pythonDemo\medical_image_segmentation\unet-master\data\membrane\test\image-ID'
    i = -1
    print(len(os.listdir(data_path)))
    for img in os.listdir(data_path):
        # ID = int(img.split('-')[0])
        # if ID >= 1000426:
        i += 1
        png_path = os.path.join(data_path,img)
        sl.copyfile(png_path, os.path.join(r'D:\pythonDemo\medical_image_segmentation\unet-master\data\membrane\test\image',str(i)+".png"))

def mask_to_list():
    for ID in os.listdir(raw_data_path):
        data_path = os.path.join(raw_data_path, ID, 'mask')
        if os.path.exists(data_path):
            for s in os.listdir(data_path):
                mask_path = os.path.join(data_path,s)
                sl.copyfile(mask_path, os.path.join('D:\pythonDemo\medical_image_segmentation\Data\data_png_png\masks',ID+"-"+s[6:10]+".png"))

def niimask_to_list():
    for ID in os.listdir(raw_data_path):
        num = 1
        data_path = os.path.join(raw_data_path, ID, ID, 'HRT2')
        mask_path = os.path.join(data_path,ID+'.nii')
        mask_slices = sitk.ReadImage(mask_path)
        mask_arr = sitk.GetArrayFromImage(mask_slices)
        # print(np.max(mask_arr))
        # mask_arr = mask_arr / np.max(mask_arr)
        # print(np.max(mask_arr))
        mask_arr[mask_arr > 1] = 0
        ddd = (mask_arr * 255).astype(np.uint8)

        for arr in range(ddd.shape[0]):
            cv2.imwrite(os.path.join(r'D:\pythonDemo\medical_image_segmentation\unet-master\data\membrane\train\label',ID+"-"+str(num)+".png"),ddd[arr])
            num += 1


def del_no_cell():
    # data_png_path = r'D:\pythonDemo\medical_image_segmentation\unet-master\data\membrane\train\image'
    # mask_png_path = r'D:\pythonDemo\medical_image_segmentation\unet-master\data\membrane\train\label'
    # for i in os.listdir(mask_png_path):
    #     img = cv2.imread(os.path.join(mask_png_path,i))
    #     print(img)
    mask_png_path = r'C:\Users\Administrator\Desktop\-0008-0013-0013-W1497L748_mask.png'
    img = cv2.imread(mask_png_path)
    print(img)



if __name__ == '__main__':
    dcm_to_png()

    # mask_to_list()
    # niimask_to_list()
    # IDname_to_num()
    # del_no_cell()
