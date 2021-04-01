import os
import SimpleITK as itk
import numpy as np
import cv2
import nibabel as nib
import imageio


nii_path = '/media/margery/b44160de-00cb-402a-ba45-d81240edf8a4/DeepLearningDemo/NEW12Month/RectalCancerDataFull/labelData'
imgs_png_path = '/media/margery/4ABB9B07DF30B9DB/pythonDemo/medical_image_segmentation/CE-Net/dataset/DRIVE/test/images'
masks_png_path = '/media/margery/4ABB9B07DF30B9DB/pythonDemo/medical_image_segmentation/Data/data_png_png/masks'
masks_png_path_vis = '/media/margery/4ABB9B07DF30B9DB/pythonDemo/medical_image_segmentation/Data/data_png_png/masks_vis'

#终版
def nii_to_png():
    print(len(os.listdir(nii_path)))
    for ID in os.listdir(nii_path):
        # if int(ID) >= 1000067:
            index = '00'
            patient_path = os.path.join(nii_path,ID)
            data = itk.ReadImage(patient_path)  #（512,19,512）
            # if not os.path.exists(os.path.join(patient_path,ID+'_HT.nii')):
            #     continue
            # label = itk.ReadImage(patient_path)  #（512，512，19)

            data_arr_ = itk.GetArrayFromImage(data)  #(512,19,512）
            data_arr_[data_arr_ == 4] = 1   #黄色交界处定义为肿瘤
            data_arr_[data_arr_ > 2] = 0
            data_arr = (data_arr_ / np.max(data_arr_) * 255).astype(np.uint8)
            if data_arr.shape[0] > 100 and data_arr.shape[1] < 100:
                data_arr = data_arr.transpose(1, 2, 0)
            elif data_arr.shape[2] < 100:
                data_arr = data_arr.transpose(2, 0, 1)
                print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")

            # label_arr = itk.GetArrayFromImage(label)    #（19，512，512)
            # label_arr[label_arr > 2] = 0
            # label_arr_vis = (label_arr / np.max(label_arr) * 255).astype(np.uint8)

            num = 1
            for i in range(data_arr.shape[0]):
                img = data_arr_[i]
                if data_arr_.shape[0] > 100 and data_arr_.shape[1] < 100:
                    img = np.rot90(img, -1, (1,0))

                if (index[0] == '0') and (index != '09'):
                    index = '0' + str(int(index[-1]) + 1)
                elif index == '09':
                    index = '10'
                else:
                    index = str(int(index) + 1)
                cv2.imwrite(os.path.join(masks_png_path,ID[:-7]+'-'+index+'.png'),img)
                # cv2.imwrite(os.path.join(masks_png_path,ID+'-'+str(num)+'.png'),label_arr[index])
                cv2.imwrite(os.path.join(masks_png_path_vis,ID[:-7]+'-'+index+'.png'),data_arr[i])
                num += 1


def nii_to_png_nibabel():
    # filenames = [os.listdir(os.path.join(nii_path,id))[0]for id in os.listdir(nii_path)]
    # data_nii = []
    # mask_nii = []
    # for id in os.listdir(nii_path):
    #     nii_ls = os.listdir(os.path.join(nii_path, id))
    #     # if len(nii_ls) == 1:
    #     #     continue
    #     data_nii.append(nii_ls[0])
    #     # mask_nii.append(nii_ls[1])

    for d in os.listdir(nii_path):
        index = '00'
        # fname = d.replace('.nii','')
        fname = d[:--7]
        niiID_path = os.path.join(nii_path, d)
        # niiMask_path = os.path.join(nii_path, fname, m)
        imgs = nib.load(niiID_path) #(512, 19, 512)
        # masks = nib.load(niiMask_path)
        img_fdata = imgs.get_fdata()
        # mask_fdata = masks.get_fdata()
        if not os.path.exists(imgs_png_path):
            os.mkdir(imgs_png_path)
            # os.mkdir(masks_png_path)
        # masks.shape = [2,1,1]
        # if imgs.shape is not masks.shape:
        #     print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
        #     print('shape error')
        if imgs.shape[2] < 100:
            (x, y, z) = imgs.shape
        elif imgs.shape[0] < 100:
            (z, x, y) = imgs.shape
        else:
            (x,z,y) = imgs.shape

        for i in range(z):
            if imgs.shape[2] < 100:
                slice = img_fdata[:,:,i]
            elif imgs.shape[0]<100:
                slice = img_fdata[i, :, :]
            else:
                slice = img_fdata[:, i, :]
            slice = np.rot90(slice,-1,(1,0))
            slice[slice > 2] = 0
            slice_vis = (slice / np.max(slice) * 255).astype(np.uint8)
            if (index[0] =='0') and (index != '09'):
                index = '0'+str(int(index[-1]) + 1)
            elif index == '09':
                index = '10'
            else:
                index = str(int(index) + 1)
            cv2.imwrite(os.path.join(masks_png_path,fname+'-'+index+'.png'),slice)
            cv2.imwrite(os.path.join(masks_png_path_vis,fname+'-'+index+'.png'),slice_vis)




if __name__ == '__main__':
    nii_to_png()
    # nii_to_png_nibabel()