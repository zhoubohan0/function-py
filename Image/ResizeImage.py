import os
import cv2
import numpy as np

def Resizeimg(inputpath,outputpath,shape = None,scale = None,defaultname = 'resize_'):
    for imgfile in os.listdir(inputpath):
        img = cv2.imread(os.path.join(inputpath, imgfile))
        if shape is not None:
            resizeimg = cv2.resize(img,dsize=shape).astype(np.uint8)
        if scale is not None:
            resizeimg = cv2.resize(img, dsize=None,fx=scale[0],fy=scale[1])
        cv2.imwrite(os.path.join(outputpath, defaultname+imgfile),resizeimg)
if __name__ == '__main__':
    inputpath = '.'#r'E:\学习\大3上\实验室\image\imageset'
    outputpath = inputpath
    Resizeimg(inputpath, outputpath,(1920,1080))