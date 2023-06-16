###################################
#blockface和niss在x200倍上，剪裁到1500x1500进行配准
#code4 将图像中心化
#extracted center image size must less than 'size' size
###################################

import os
import cv2
import glob
import numpy as np


pathname = r'D:\data\R03\filter'
save =r'D:\data\R03\Crop'
size = 1536
files = os.listdir(pathname)
pathlist = files

for path in pathlist:
    pathin = pathname+'/'+path
    img = cv2.imread(pathin)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    new_img  = cv2.resize(img,(0,0),fx=1,fy=1)
    arran = np.where(img>0)
    xmin =  arran[0].min()
    xmax = arran[0].max()
    ymin =  arran[1].min()
    ymax = arran[1].max()
    #print(xmin,xmax,ymin,ymax)
    img = img[xmin:xmax,ymin:ymax]
    x= xmax-xmin
    y = ymax-ymin
    xpre = int((size - x)/2) 
    xbe = size - (xpre+x)
    ypre = int((size - y)/2)
    ybe = size-(ypre+y)
    img = np.pad(img,((xpre,xbe),(ypre,ybe)),'constant', constant_values=(0,0))
    print(img.shape)
    pathin = save+'/'+path
    cv2.imwrite(pathin,img)
    