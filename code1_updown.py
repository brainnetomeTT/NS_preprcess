###################################
#pathname: original path
#savename:output path
#downrate: down rate (up>1,down<1)
#example show fromx40 ->x200
##################################
import re
import os
import cv2
import glob
import numpy
pathname = 'E:/data/data40'
savename = 'E:/data/data200'
downrate = 5
files = os.listdir(pathname)

for path in files:
    pathin = pathname+'/'+path
    img =cv2.imread(pathin)
    #img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    img2 = cv2.resize(img,(0,0),fx=1/downrate,fy=1/downrate)
    save = savename+'/'+path
    cv2.imwrite(save,img2)