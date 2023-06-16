###################################
#upsample rotated file
#for example: we get best angle in resolution 22um
#we can apply the angle on resolution 2.2um 
###################################
import nibabel as nib
import numpy as np
import os
import cv2
import glob
import matplotlib.pyplot as plt
import re 
pathname1 = 'E:/data/upsample/x200'
pathname2 = 'E:/data/upsample/x40'
save = 'E:/data/Registration'
files = os.listdir(pathname1)
pathlist = files



for path in pathlist:
    name = os.path.splitext(path)[0]
    print(name)
    list_index = [i.start() for i in re.finditer("_",name)]
    angle = int(name[list_index[-1]+1:])
    print(angle)
    r_po = name.find('r')
    name = name[:16]
    print(name)
    
    pathin2 = pathname2 + '/' + name + '.tif'
    img2 = cv2.imread(pathin2)
    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    
    height, width = img2.shape
    center = (width // 2, height // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(img2, M, (width, height))
    plt.figure()
    plt.subplot(2,2,1)
    plt.imshow(img2)
    plt.subplot(2,2,2)
    plt.imshow(rotated)
    plt.show()
    s = '{}/{}rotated_{}.tif'.format(save,name,angle)
    print(s)
    cv2.imwrite(s,rotated)
