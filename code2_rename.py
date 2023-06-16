###################################
#rename noralization name  R04{}_P{:02d}_N{:02d}_{}
###################################
import re
import os
import cv2
import glob
import numpy
pathname = r'G:\data\R03\x10'
savename1 = r'D:\data\R03\original'
savename2 = r'D:\data\R03\renam'

#将文件夹分为两个分别为单张染色的片子和多个染色的片子
files = os.listdir(pathname)
for path in files:

    pathin = pathname+'/'+path
    img =cv2.imread(pathin)
    list_index = [i.start() for i in re.finditer("_",path)]

    #3 or 4
    if(list_index[2]-list_index[1] > 4):
        save = savename1+'/'+path
        cv2.imwrite(save,img)
    else:
        Pindex = path.index('P')
        Nindex = path.index('N')
        index = path[Pindex+1:list_index[2]]
        layer = path[Nindex+1:list_index[3]]
        print(index,layer)
        name = "R04{}_P{:02d}_N{:02d}_{}".format(path[list_index[0]+1:list_index[1]],int(index),int(layer),path[list_index[-1]:])
        print(name)
        save = savename2+'/'+name
        cv2.imwrite(save,img)