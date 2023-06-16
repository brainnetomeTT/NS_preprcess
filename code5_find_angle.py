###################################
#将图像完成旋转粗配准，并且转为nii格式，使用15度，3个误配准，10度1个误配准，这里采用5度
#输出的为niss，BF，rotated, tif文件
#only using rotation transformation to search to find image pairs have max MI's angle,
###################################
import nibabel as nib
import numpy as np
import os
import cv2
import glob
import matplotlib.pyplot as plt
import sklearn.metrics as skm


pathname1 = r'D:\data\r04x100_preprocess\BF\CropC2'
pathname2 = r'D:\data\r04x100_preprocess\NS\CropC2'

save = r'D:\data\r04x100_preprocess\NS\RotatedC2'
files = os.listdir(pathname1)
pathlist = files

coarsesearch = 5
step = 72


def hxx_forward(img1, img2):
    x = np.reshape(img1, -1)
    y = np.reshape(img2, -1)
    return skm.mutual_info_score(x, y)


def findangle(img1, img2, step):
    i = 0
    hxx_max = hxx_forward(img1, img2)
    maxi = 0
    rotated1 = img2
    maxrotated = img2
    while (i <= step):
        i = i + 1
        hxx = hxx_forward(img1, rotated1)
        M1 = cv2.getRotationMatrix2D(center, i * coarsesearch, 1.0)
        rotated1 = cv2.warpAffine(img2, M1, (width, height))
        h1 = hxx_forward(img1, rotated1)
        if (h1 > hxx_max):
            hxx_max = h1
            maxi = i
            maxrotated = rotated1
    # print("maxi={},MI={}".format(maxi*coarsesearch,hxx_max))
    M1 = cv2.getRotationMatrix2D(center, -maxi * coarsesearch, 1.0)
    return maxi * coarsesearch, M1


for path in pathlist:
    name = os.path.splitext(path)[0]
    print(name)
    pathin1 = pathname1 + '/' + name + '.tif'
    pathin2 = pathname2 + '/' + name + '.tif'
    img1 = cv2.imread(pathin1)
    img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img2 = cv2.imread(pathin2)
    print(pathin2)
    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    height, width = img1.shape
    center = (width // 2, height // 2)
    angle, M = findangle(img2, img1, step)
    print(angle,M)
    rotated = cv2.warpAffine(img2, M, (width, height))
    plt.figure()
    plt.subplot(2,2,1)
    plt.imshow(img1)
    plt.subplot(2,2,2)
    plt.imshow(img2)
    plt.subplot(2,2,3)
    plt.imshow(rotated)
    plt.show()
    s = '{}/{}rotated_{}.tif'.format(save,name,angle)
    print(s)
    cv2.imwrite(s,rotated)