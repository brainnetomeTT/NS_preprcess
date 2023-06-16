###################################
#get linear transformer file from ANTs in low resolution
#apply the transformer file on high resolution
###################################
import nibabel as nib
import numpy as np
import os
import cv2
import glob
import matplotlib.pyplot as plt
import re 
import scipy.io as io 
import SimpleITK as sitk

pathname1 = r'G:\data\aa\out'
matpath = r'G:\data\aa\mat'
size = 10
save = r'G:\data\aa'


files = os.listdir(pathname1)
pathlist = files
for path in pathlist[35:]:
    name = os.path.splitext(path)[0]
    rname= name
    list_index = [i.start() for i in re.finditer("_",name)]
    name = name[:15]
    print(name)
    matname = matpath+'/'+name+'0GenericAffine.mat'
    print(matname) 
    read_result = sitk.ReadTransform(matname)
    basic_transform = read_result
    center = read_result.GetFixedParameters()
    translation =read_result.GetParameters()
    newcenter = []
    for path in center:
        newcenter.append(path * size)
    newtranslation = []
    for i in range(6):
        if (i<4):
            newtranslation.append(translation[i])
        else:
            newtranslation.append(translation[i]*size)
    read_result.SetFixedParameters(newcenter)
    read_result.SetParameters(newtranslation)

    
    itkpath = pathname1+'/'+rname+'.tif'
    itk_img = sitk.ReadImage(itkpath)
    img = sitk.GetArrayFromImage(itk_img)
    print(img.shape)

    origin =itk_img.GetOrigin()
    print(origin)
    direction = itk_img.GetDirection()
    print(direction)
    dimension = itk_img.GetDimension()
    print(dimension)


    basic_transform  = read_result

    resampler = sitk.ResampleImageFilter()
    resampler.SetReferenceImage(itk_img);
    resampler.SetInterpolator(sitk.sitkLinear)
    resampler.SetTransform(basic_transform)
    out = resampler.Execute(itk_img)
    img2 = sitk.GetArrayFromImage(out)
    s =save+'/'+name+'AFFINE.tif'
    
    img2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)   
    cv2.imwrite(s,img2)
    

    
    
  