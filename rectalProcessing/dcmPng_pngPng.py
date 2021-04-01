import SimpleITK as sitk
import os,shutil

root = r'D:\pythonDemo\medical_image_segmentation\Data\data_dcm_png'

def dcm_to_png():
    for ID in os.listdir(root):
        data_path = os.path.join(root,ID,ID)
        mask_path = os.path.join(root,ID,'mask')
        reader = sitk.ImageSeriesReader()
        series_file_name = reader.GetGDCMSeriesFileNames(data_path)
        reader.SetFileNames(series_file_name)
        imgs = reader.Execute()
        imgs_array = sitk.GetArrayFromImage(imgs)

        print('ok')


if __name__ == '__main__':
    dcm_to_png()