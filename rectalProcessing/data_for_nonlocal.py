import os
import glob
import SimpleITK as sitk
import shutil
"""
import dicom2nifti
# 多个dicom文件转化为3D nii文件
# 'E:/COVID-19CTimageAnal/data'为存放dcm2d切片文件的目录
original_dicom_directory = 'E:/COVID-19CTimageAnal/data'
# '0007686236.nii'为要生成的nii文件名
output_file = '0007686236.nii'
dicom2nifti.dicom_series_to_nifti(original_dicom_directory, output_file, reorient_nifti=True)
"""

data_dir_raw = r'D:\RectalCancer'
output_path = r'D:\pythonDemo\medical_image_segmentation\Non-local-U-Nets\data\zhengyang\InfantBrain\RawData'


def raw_to_img():
    i = 1
    for ID in os.listdir(data_dir_raw):
        HRT2_path = os.path.join(data_dir_raw,ID,ID,'HRT2')
        reader = sitk.ImageSeriesReader()
        # GetGDCMSeriesFileNames读取序列号相同dcm文件的路径，series[0]代表第一个序列号对应的文件
        dicom_path = reader.GetGDCMSeriesFileNames(HRT2_path)
        if not dicom_path:
            i += 1
            continue
        # # GetGDCMSeriesIDs读取序列号相同的dcm文件
        # series_id = sitk.ImageSeriesReader.GetGDCMSeriesIDs(path_read)
        reader.SetFileNames(dicom_path)
        image2 = reader.Execute()

        # image_array = sitk.GetArrayFromImage(image2) #z,y,x
        # origin = image2.GetOrigin() #x,y,z
        # spacing = image2.GetSpacing() #x,y,z
        # image3 = sitk.GetImageFromArray(image_array)
        # sitk.WriteImage(image2,'subject-%d-'%ID+'HRT2.img.gz')
        if os.path.isfile(os.path.join(output_path,'subject-%s-'% i+'HRT2.nii')):
            i += 1
            continue
        sitk.WriteImage(image2,os.path.join(output_path,'subject-%s-'%i+'HRT2.nii'))
        i += 1

def rename_label():
    label_type = '.nii'

    i = 1
    for ID in os.listdir(data_dir_raw):
        label_path = glob.glob(os.path.join(data_dir_raw,ID,ID,'HRT2\*'+label_type))

        new_img_name = 'subject-%d-label'% i + label_type
        for file in label_path:
            if os.path.isfile(os.path.join(output_path,new_img_name)):
                break
            # _,used_img_name = os.path.split(file)
            # os.rename(file, os.path.join(output_path,new_img_name))
            shutil.copy(file, os.path.join(output_path,new_img_name))
        i += 1


if __name__ == '__main__':
    raw_to_img()
    rename_label()
