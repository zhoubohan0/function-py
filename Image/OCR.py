# 中文文字要大而清楚，噪声少，平直
from cnocr import CnOcr
import cv2
ocr = CnOcr()
img = cv2.imread('./test.jpg')
res = ocr.ocr(img)
for line in res:
    print("".join(line[0]))

