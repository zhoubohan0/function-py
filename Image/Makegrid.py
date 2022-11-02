import torch
import numpy as np
import glob
import cv2
import os
from torchvision.utils import make_grid


def show(img, filename):
    img = np.transpose(img.numpy(), (1, 2, 0))  # 转回ndarry显示
    if filename is not None:
        cv2.imwrite(filename, img)
    cv2.namedWindow('n', 0)
    cv2.imshow('n', img)
    cv2.waitKey()


def stackimg(imagepath, nrow, outputfile=None, pattern=None):
    if pattern is None:
        pattern = '*.*'
    imgpath = glob.glob(os.path.join(imagepath, pattern))  # 直接获得拼接好的路径
    dsize = np.int_(np.array([cv2.imread(each).shape[:-1] for each in imgpath]).mean(axis=0)[::-1])  # 自动获取resize尺寸
    print(f'width-{dsize[0]},height-{dsize[1]}')
    imglist = []
    for each in imgpath:
        img = cv2.resize(cv2.imread(each), dsize=dsize)
        imglist.append(torch.from_numpy(img).permute(2, 0, 1))
    show(make_grid(imglist, nrow=nrow, padding=10), outputfile)  # 可以传入tensor/List(tensor)


if __name__ == '__main__':
    imagepath = '.'
    outputfile = './output/stack_image.jpg'
    stackimg(imagepath, nrow=5, outputfile=outputfile, pattern='*.jpg')
