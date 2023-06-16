###################################
#get norlinear transformer file from ANTs in low resolution
#apply the transformer file on high resolution
#in reality,this funciton useless,beacuse it introduce a lot of information(it doesn't exist) 
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
def show(image):   
    cv2.namedWindow('show image',0)
    cv2.imshow('show image',image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
pathname = 'D:\MASTDATA\R03\patch'
matname = 'G:\voxelmorph\split_morph\data\ANTs\mat'
savename = 'G:\voxelmorph\split_morph\data\ANTs\save'

uptimes = 10 
files = os.listdir(pathname)
pathlist = files
for path in pathlist:
    name = os.path.splitext(path)[0]
    #rname= name
    list_index = [i.start() for i in re.finditer("_",name)]
    name = name[:16]
    print(name)
#field process
    pathin = matname + '/'+name+'1Warp.nii.gz'
    print(pathin)
    nii_img = nib.load(pathin)
    newdata = nii_img.get_fdata()
    print(newdata.shape)
    img = np.squeeze(newdata)
    print(img.shape)
    #变形场要采样T倍数后采样，原来移动x到A点，现在要移动x*T倍才能到A点
    img = img *uptimes 
    img = cv2.resize(img,(0,0),fx=uptimes,fy=uptimes)
    #测试显示要转换类型才可以用于antsApplytransforms
    img = np.array(img).astype(np.float16)
    img = img[:,:,np.newaxis,np.newaxis,:]
    print(img.shape)
    affine = nii_img.affine.copy()
    hdr = nii_img.header.copy()
    #维度改变后，要改变头文件中的维度，别的不变
    hdr['dim'] = [5,hdr['dim'][1]*uptimes,hdr['dim'][2]*uptimes,1,1,2,1,1]
    #print(hdr)
    new_nii = nib.Nifti1Image(img,affine,hdr)
    s = savename+'/'+name+'1Warp.nii.gz'
    nib.save(new_nii,s)

    #code2
    #非线性affine.mat文件的变换 
    #主要是改变移动距离，和中心
    matin = matname + '/'+name+'0GenericAffine.mat'
    read_result = sitk.ReadTransform(matin)
    basic_transform = read_result

    center = read_result.GetFixedParameters()
    translation =read_result.GetParameters()

    newcenter = []
    for path in center:
        newcenter.append(path * uptimes)
    newtranslation = []
    for i in range(6):
        if (i<4):
            newtranslation.append(translation[i])
        else:
            newtranslation.append(translation[i]*uptimes)
    print(newcenter)
    print(newtranslation)
    read_result.SetFixedParameters(newcenter)
    read_result.SetParameters(newtranslation)
    s = savename+'/'+name+'0GenericAffine.mat'
    sitk.WriteTransform(read_result,s)
    print(read_result)


