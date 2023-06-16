###################################
#Format:nift transform to tif using ITK 
###################################
import SimpleITK as sitk
import cv2
import numpy as np
import scipy.io as io
import matplotlib.pyplot as plt
import nibabel as nib

import os

def show(image):  
    cv2.namedWindow('show image',0)
    cv2.imshow('show image',image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
pathname = r'\Model\R04\train\ANTs_Norlinear'
savename = r'G:/硕士课题/Model/R04/train/ANTs_nor/'
files = os.listdir(pathname)
pathlist = files
for path in pathlist:
    print(path)
    if 'mat' not in path:
        pathin = pathname+ '/'+path
        itk_BF200 = sitk.ReadImage(pathin)
        BF200_img = sitk.GetArrayFromImage(itk_BF200)
        print(BF200_img.shape)
        origin =itk_BF200.GetOrigin()
        print(origin)
        direction =itk_BF200.GetDirection()
        print(direction)
        dimension = itk_BF200.GetDimension()
        print(dimension)
        name = os.path.split(path)[1].replace('.nii.gz','.png')
        s = savename+'/'+name
        BF200_img = np.uint8(BF200_img)
        print(BF200_img.shape)
        cv2.imwrite(s,BF200_img)
        print(s)

       #sitk.WriteImage(BF200_img,s)
