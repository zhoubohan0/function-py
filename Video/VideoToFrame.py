import cv2
import os
import time
def show(img, winname='n'):
    cv2.namedWindow(winname, 0)
    # cv2.resizeWindow(winname, 600, 600)
    cv2.imshow(winname, img)
    cv2.waitKey(0)

def output(frame, show=None, tofile=None):
    if tofile is not None:
        cv2.imwrite(tofile, frame)
    if show:
        cv2.imshow('', frame)
        cv2.waitKey()


def vtf(srcpath, destpath):
    if not os.path.exists(destpath):
        os.mkdir(destpath)
    start = time.time()
    videoCapture = cv2.VideoCapture()
    videoCapture.open(srcpath)
    fps = videoCapture.get(cv2.CAP_PROP_FPS)
    frames = videoCapture.get(cv2.CAP_PROP_FRAME_COUNT)
    print("fps=", int(fps), "frames=", int(frames))
    for i in range(int(frames)):
        _, frame = videoCapture.read()
        frame = cv2.resize(frame[62:-58],(128,64))  # add process here
        output(frame, tofile=os.path.join(destpath, r"%d.jpg" % (i)))
    end = time.time()
    print('Successfully!')
    print(f'total:{round(end-start,2)}s')

if __name__ == '__main__':
    srcpath = r"C:\Users\ZhouBoHan\Desktop\MC_youtube.mp4"
    destpath = os.path.join(os.path.split(srcpath)[0],'dataset')
    if not os.path.exists(destpath): os.mkdir(destpath)
    vtf(srcpath,destpath)

