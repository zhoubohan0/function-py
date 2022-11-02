import cv2
from time import sleep
from argparse import ArgumentParser
def show(img):
    cv2.imshow('', img)
    cv2.waitKey()

def Video(Four_Character_Codes,videoname):
    # [备注]：视频输出在.py目录下，一定要按'q'退出才能正常保存视频
    cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
    fourcc = cv2.VideoWriter_fourcc(*Four_Character_Codes)  # 不同编码格式，上网搜
    fps = 30  # int(cap.get(cv2.CAP_PROP_FPS))
    size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    video = cv2.VideoWriter(videoname, fourcc, fps, size)
    cnt = 0
    try:
        while cap.isOpened():
            success, frame = cap.read()
            if success:
                image = cv2.flip(frame,1)
                video.write(image)
                sleep(1 / fps)
                cnt+=1
                cv2.imshow('Recording',image)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    except KeyboardInterrupt:
        print(f'Stopped! {cnt} frames captured!')  # 提前停止捕获
    cap.release()
    video.release()
    print('Save video successfully!')

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('--fourcc',default='mp4v',type=str)
    parser.add_argument('--filename',default='video.mp4',type=str)
    args = parser.parse_args()
    fourcc = args.fourcc
    filename = args.filename
    Video(fourcc,filename)