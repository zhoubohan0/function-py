# -*- coding: utf-8 -*-
import os
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

# 中文名显示
def zh_cn(string):
    return string.encode("gbk").decode(errors="ignore")

# 读取中文路径图片，窗口显示中文标题，保存中文路径图片
def read_show_save_zh_img(filename,isshow=True,issave=True):
    name, ext = os.path.splitext(filename)
    # np.fromfile读取二进制文件，cv2.imdecode转化为np数组
    img = cv2.imdecode(np.fromfile(filename, dtype=np.uint8), 1)  # 0:gray, 1:color
    # 窗口显示中文标题，缺点是有些中文无法正常显示，要调整编码格式
    if isshow:
        cv2.imshow(zh_cn('图片'), img)
        cv2.waitKey(0)
    # cv2.imencode对图像二进制编码，cv2.imwrite保存图像格式到文件
    if issave:
        cv2.imencode(ext, img)[1].tofile("保存" + filename)
    return img

# 在图片上显示中文
def cv2ImgAddText(img, text, left, top, textColor, textSize):
    if isinstance(img, np.ndarray):  # 判断是否OpenCV图片类型
        img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(img)
        fontText = ImageFont.truetype("simhei.ttf", textSize, encoding="utf-8")
        draw.text((left, top), text, textColor, font=fontText)
        return cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)



if __name__ == '__main__':
    img = read_show_save_zh_img('图片.png')
    img = cv2ImgAddText(img, "这是文字区域", left=140, top=60, textColor=(255, 0, 0), textSize=30)
    cv2.imshow("DrawChinese", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()