import cv2
from pyzbar import pyzbar

def decode(imgfile):
    return pyzbar.decode(cv2.imread(imgfile))[0].data.decode("utf-8")

if __name__ == '__main__':
    imgfile = "QR.png"
    print(decode(imgfile))