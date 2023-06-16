###################################
#pathname :pathname
#save :savename
#path: newfile name 
###################################
#code3:去白边
import re
import os
import cv2
import glob
import numpy  as np
import os
import cv2
import glob
import numpy as np


def maskedge(pathname, pathlist, save):
    index = 0.0
    sum = len(pathlist)
    for path in pathlist:
        index = index + 1
        print("#####{:.2%}   {:.0f}/{:d}#####".format(index / sum, index, sum))
        print(path)
        name = path
        path = pathname + '/' + path
        print(path)
        img = cv2.imread(path)
        # transfer to gray
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        print(np.max(img),np.min(img))
        # show the hsitogram
        hist = cv2.calcHist([img], [0], None, [256], [0, 256])
        # find maxpostion but not too dark
        hist = hist[20:]

        # find wihte edge postion range [max+-7]
        #maxpo = np.where(hist == np.max(hist))
        #maxpo = int(maxpo[0])
        maxpo = 168
        noisyrange = list(range(256))
        noisyrange = noisyrange[maxpo - 8:maxpo + 8]

        # Extraction prospects
        propost = img
        for i in noisyrange:
            propost = np.where(propost == (i + 20), 0, propost)

        lbimg = cv2.medianBlur(propost, 11)
        # show(lbimg)
        mask = np.where(lbimg == 0, 0, 255)

        cach = save + '/' + 'cach.tif'
        cv2.imwrite(cach, mask)
        path = cach
        mask = cv2.imread(path)
        mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
        masklbimg = cv2.medianBlur(mask, 7)
        # show(masklbimg)
        cv2.imwrite(cach, mask)
        img = np.where(img > 200,0,img)
        maskimg = np.where(masklbimg == 0, 0,img)
        #maskimg = np.where(maskimg > 200,0,maskimg)
        # show(maskimg)

        path = save + '/R04' + name[3:-10]+'.tif'
        print(path)
        cv2.imwrite(path, maskimg)
pathname = r'D:\data\r04x100\A'
files = os.listdir(pathname)
pathlist = files
save = r'D:\data\r04x100_preprocess\A'
maskedge(pathname,pathlist,save)
    