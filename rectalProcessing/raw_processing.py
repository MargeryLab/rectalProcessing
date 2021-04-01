import SimpleITK as itk
import os
import glob
import shutil
import dicom2nifti
import pydicom
"""
1、将文件内容拷贝到另一个文件中
shutil.copyfileobj(open('old.xml','r'), open('new.xml', 'w'))
2、拷贝文件
shutil.copyfile('f1.log', 'f2.log') #目标文件无需存在
3、仅拷贝权限。内容、组、用户均不变
shutil.copymode('f1.log', 'f2.log') #目标文件必须存在
4、拷贝文件和权限
shutil.copy('f1.log', 'f2.log')
5、递归的去拷贝文件夹
shutil.copytree('folder1', 'folder2', ignore=shutil.ignore_patterns('*.pyc', 'tmp*')) #目标目录不能存在，注意对folder2目录父级目录要有可写权限，ignore的意思是排除
"""

raw_path = '/home/margery/DeepLearnigDemo/NEW12Month/RectalCancerDataFull/dcmData'
raw_mask_path = r'D:\segTeam_20201028\segTeam1'
des_path = '/media/margery/4ABB9B07DF30B9DB/pythonDemo/medical_image_segmentation/Data/data_nii'

def getalltag(path): #提取所有tag
    file_reader = itk.ImageFileReader()
    file_reader.SetFileName(path)
    data = file_reader.Execute()
    for key in file_reader.GetMetaDataKeys():
        print(key, file_reader.GetMetaData(key))

def changeTransferSyntaxUID():
    uncompressed_types = ["1.2.840.10008.1.2",
                          "1.2.840.10008.1.2.1",
                          "1.2.840.10008.1.2.1.99",
                          "1.2.840.10008.1.2.2"]
    for ID in os.listdir(raw_path):
        ID_path = os.path.join(raw_path,ID,ID,'HRT2')
        series_reader = itk.ImageSeriesReader()
        fileNames = series_reader.GetGDCMSeriesFileNames(ID_path)
        for index in range(len(fileNames)):
            ds = pydicom.dcmread(fileNames[index])
            # if 'TransferSyntaxUID' in ds.file_meta and ds.file_meta.TransferSyntaxUID not in uncompressed_types:
            #     ds.file_meta[0x0002,0x0010].value = "1.2.840.10008.1.2"
                # ds.save_as(fileNames[index])


#将dcm和png压缩成nii
def dcm_to_nii():
    for ID in sorted(os.listdir(raw_path)):
        ID_path = os.path.join(raw_path,ID,ID,'HRT2')
        # mask_ls = glob.glob(os.path.join(ID_path, '*.nii'))
        # mask_nii = os.path.join(raw_mask_path, ID+'_HT.nii')
        if not os.path.exists(os.path.join(des_path,ID)):
            os.mkdir(os.path.join(des_path,ID))

        # dicom2nifti.dicom_series_to_nifti(original_dicom_directory, output_file, reorient_nifti=True)
        # try:
        #     dicom2nifti.dicom_series_to_nifti(ID_path, os.path.join(des_path, ID, ID), reorient_nifti=True)
        # except:
        #     print(ID)
        reader = itk.ImageSeriesReader()
        dicom_path = reader.GetGDCMSeriesFileNames(ID_path)
        reader.SetFileNames(dicom_path)
        imgs = reader.Execute()
        if not os.path.exists(os.path.join(des_path, ID)):
            os.mkdir(os.path.join(des_path, ID))
        itk.WriteImage(imgs, os.path.join(des_path, ID, ID + '.nii'))

        # shutil.move(mask_nii, os.path.join(des_path, ID, ID+'_HT.nii'))


def dcm_to_nii_itk():
    for ID in os.listdir(raw_path):
        ID_path = os.path.join(raw_path,ID,ID,'HRT2')
        reader = itk.ImageSeriesReader()
        dicom_path = reader.GetGDCMSeriesFileNames(ID_path)
        reader.SetFileNames(dicom_path)
        imgs = reader.Execute()

        if not os.path.exists(os.path.join(des_path,ID)):
            os.mkdir(os.path.join(des_path,ID))
        itk.WriteImage(imgs, os.path.join(des_path, ID, ID+'.nii'))

        mask_nii = os.path.join(raw_mask_path, ID+'_HT.nii')
        shutil.move(mask_nii, os.path.join(des_path, ID, ID+'_HT.nii'))

def data_update():
    new_nii = '/home/margery/DeepLearnigDemo/NEW12Month/segDataUpdated20201211'
    old_nii = '/media/margery/4ABB9B07DF30B9DB/pythonDemo/medical_image_segmentation/Data/data_nii'

    index = 0
    for ID in sorted(os.listdir(new_nii)):
        for OID in sorted(os.listdir(old_nii)):
            if int(ID[0:7]) == int(OID):
                if os.path.exists(os.path.join(old_nii,OID,OID+'_label.nii')):
                    sl.copy(os.path.join(new_nii,ID),os.path.join(old_nii,OID))
                    index += 1
                    os.remove(os.path.join(old_nii,OID,OID+'_label.nii'))
                    break
                else:
                    sl.copy(os.path.join(new_nii, ID), os.path.join(old_nii, OID, OID + '_HT.nii'))
                    index += 1
                    break
    print(index)

def extract_label():
    data_nii_path = '/media/margery/4ABB9B07DF30B9DB/pythonDemo/medical_image_segmentation/Data/data_nii'
    des_path = '/home/margery/DeepLearnigDemo/NEW12Month/RectalCancerDataFull/labelData'
    for ID in os.listdir(data_nii_path):
        ID_nii_path = os.path.join(data_nii_path,ID)
        data_ls = os.listdir(ID_nii_path)
        if len(data_ls) == 2:
            shutil.copy(os.path.join(ID_nii_path,ID+'_HT.nii'),os.path.join(des_path,ID+'_HT.nii'))


if __name__ == '__main__':
    for s in os.listdir(raw_path):
        if s:
            data_hrt2_path = os.path.join(raw_path,s,s,'HRT2')
            reader = itk.ImageSeriesReader()

            # dcm_ls = glob.glob(os.path.join(data_hrt2_path,'*.DCM'))
            # reader.SetFileNames(dcm_ls)
            # dcm = reader.Execute()
            # Spacing = dcm.GetSpacing()
            # Origin = dcm.GetOrigin()
            # Direction = dcm.GetDirection()
            # des_dcm_path = os.path.join(des_path,s,'.nii')
            # if not os.path.exists(des_dcm_path):
            #     itk.WriteImage(dcm,os.path.join(des_path,s+'.nii'))

            mask_ls = glob.glob(os.path.join(data_hrt2_path,'*.nii'))
            mask_nii_des = os.path.join(des_path,s+'_mask'+'.nii')
            mask = itk.ReadImage(mask_ls[0])
            # mask.SetSpacing(Spacing)
            # mask.SetOrigin(Origin)
            # mask.SetDirection(Direction)
            if not os.path.exists(mask_nii_des):
                # itk.WriteImage(mask,mask_nii_des)
                shutil.copyfile(mask, mask_nii_des)

    path = r'D:\pythonDemo\medical_image_segmentation\Data\data_raw\1000001\1000001\HRT2'
    mask_path = r'D:\pythonDemo\medical_image_segmentation\Data\data_nii\1000011_mask.nii'

    reader = itk.ImageSeriesReader()

    series_file_names = reader.GetGDCMSeriesFileNames(path)
    reader.SetFileNames(series_file_names)
    image = reader.Execute()
    mask = itk.ReadImage(mask_path)
    print('ok')

    changeTransferSyntaxUID()
    dcm_to_nii()
    extract_label()

