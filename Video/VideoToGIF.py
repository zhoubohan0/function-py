import imageio
import os
import cv2.cv2 as cv
def videoToGIF(videofile_path,savefile_path,timelasting,fps):
    cap = cv.VideoCapture(videofile_path)
    gif = []
    total_frames=int(timelasting*fps)
    while cap.isOpened() and total_frames:
        ret,frame = cap.read()
        if ret == False:
            break
        frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        gif.append(frame)
        total_frames-=1
    imageio.mimsave(savefile_path, gif, format='GIF', fps=fps)

if __name__ == '__main__':
    videofile_path = r'video.mp4'
    savefile_path = videofile_path[:-3]+'gif'
    timelasting = 12  # gif动图持续时间
    fps = 15          # gif动图帧率
    videoToGIF(videofile_path,'here.gif',timelasting=timelasting,fps=fps)