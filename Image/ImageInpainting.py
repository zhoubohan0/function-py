import numpy as np
from skimage.restoration import inpaint_biharmonic
import cv2
import os
def show(img,filename=None):
    if filename is not None:
        cv2.imwrite(filename,img*255)
    cv2.imshow('n', img)
    cv2.waitKey()

def on_EVENT_LBUTTONDOWN(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        img,path = param
        global points, img_draw  # 这些可以写到param里
        points.append((y,x))  # 图像坐标和np坐标不一样
        print(len(points))
        if len(points) >= 2:
            cv2.destroyWindow('n')
            print('开始修复...')
            # 形成掩膜,周围0中间1
            ul = min(points[0][0],points[1][0]),min(points[0][1],points[1][1])
            dr = max(points[0][0],points[1][0]),max(points[0][1],points[1][1])
            mask = np.zeros(img.shape[:-1])
            mask[ul[0]:dr[0]+1,ul[1]:dr[1]+1]=np.ones((dr[0]+1-ul[0],dr[1]+1-ul[1]))
            # 修复
            inpainted_image = inpaint_biharmonic(img, mask, True)  # 修复的图是归一化的
            # 输出结果图片
            path, filename = os.path.split(path)
            name, ext = os.path.splitext(filename)
            show(inpainted_image,os.path.join(path, name + '_' + ext))
        else:
            img_draw = cv2.circle(img_draw, (x, y), 1, (0, 0, 255), thickness=-1)
            show(img_draw)


if __name__ == '__main__':
    # 读取显示
    imgpath = r'C:\Users\zhoubohan\Desktop\1.jpg'
    img = cv2.imread(imgpath)
    # 准备
    img_draw = img.copy()
    points = []
    # 进入消息循环
    cv2.namedWindow('n', 0)
    cv2.setMouseCallback("n", on_EVENT_LBUTTONDOWN, param=[img,imgpath])
    cv2.imshow('n', img)
    cv2.waitKey()


