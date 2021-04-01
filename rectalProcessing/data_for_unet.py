import os
import glob
import nibabel as nib
import SimpleITK as itk
import shutil


data_dir_raw = 'D:\pythonDemo\medical_image_segmentation\RectalCancer'
data_dir_new = 'D:\pythonDemo\medical_image_segmentation\RectalCanceData'
filenames = os.listdir(data_dir_raw)


def makedir():
    for ID in filenames:
        path = os.path.join(data_dir_new,ID)
        isExists = os.path.exists(path)
        if not isExists:
            os.makedirs(path)
        HRT2_path = os.path.join(path,ID)



def data_processing():
    for ID in filenames:
        HRT2_path = os.path.join(data_dir_raw, ID, ID, 'HRT2')
        data_path = HRT2_path

        file_type = 'gz'
        hdr_path = os.path.join(HRT2_path,'*.hdr.'+file_type)
        img_path = os.path.join(HRT2_path,'*.img.'+file_type)

        _,hdr_used_name = os.path.split(hdr_path)
        _,img_used_name = os.path.split(img_path)
        hdr_new_name = ID + '.hdr.'+ file_type
        img_new_name = ID + '.img.'+ file_type

        os.rename(os.path.join(HRT2_path,hdr_used_name),os.path.join(HRT2_path,hdr_new_name))
        os.rename(os.path.join(HRT2_path,img_used_name),os.path.join(HRT2_path,img_new_name))


if __name__ == '__main__':
    data_processing()
    makedir()
