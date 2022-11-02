import os
import cv2
import numpy as np
# 对每一种对象,获得随机的颜色
def get_random_color(object_id): # 用每一种不同的对象 设置对应随机种子以每次获得相同的颜色
    np.random.seed(object_id)
    random_color = np.random.randint(0,255,3)
    return (int(random_color[0]),int(random_color[1]),int(random_color[2]))
# 整理输入txt文件，以每一帧整理对应的bounding box集合
def sort_tracklets(gts):
    sorted_gts = {}

    for line in gts:
        line = line.strip().split(" ")
        object_id = int(line[0])
        #if object != "car":  #这里可以通过这样的方式进行筛选 diy
        #    continue
        # 以下格式根据 自己文档格式的不同进行修改
        frame = int(line[2])
        left = int(float(line[3])) # [left top] of bounding box
        top = int(float(line[4]))
        right = left +int(float(line[5])) # [right bot] of bounding box
        bot = top+int(float(line[6]))
        conf = float(line[1])

        if frame not in list(sorted_gts.keys()):
            sorted_gts[frame] = []
        sorted_gts[frame].append([object_id,left,top,right,bot,conf]) #

    return sorted_gts #按照帧进行排列 包含每一帧的bounding box 和对应的置信度
# 对视频的每一帧，绘制一个box
def plot_bbx(frame, left, top, right, bot, conf, object_id,save=False):  # frame 为一张图片 left top right bot 为x1y1x2y2坐标 conf为左上角绘字

    ptLeftTop = np.array([left, top])
    ptRightBottom = np.array([right, bot])
    textleftTop = []

    point_color = get_random_color(object_id)  # 根据不同的object_id获得随机的颜色
    # point_color = (0, 0, 255) #指定颜色 GBR格式
    thickness = 2
    lineType = 4

    frame_np = np.array(frame)  # 输入frame为opencv截取视频获得每一帧图像
    # 绘制bounding box
    cv2.rectangle(frame_np, tuple(ptLeftTop), tuple(ptRightBottom), point_color, thickness, lineType)
    # 绘制conf左上角标
    t_size = cv2.getTextSize(conf_name, 1, cv2.FONT_HERSHEY_PLAIN, 1)[0]
    textlbottom = ptLeftTop + np.array(list(t_size))
    cv2.rectangle(frame_np, tuple(ptLeftTop), tuple(textlbottom), point_color, -1)
    ptLeftTop[1] = ptLeftTop[1] + (t_size[1] / 2 + 4)

    # 绘字
    cv2.putText(frame_np, conf_name, tuple(ptLeftTop), cv2.FONT_HERSHEY_PLAIN, 1.0, (255, 0, 0), 1)
    # 实现对每个图片中的目标截取并保存
    if save:
        cropped_img = frame[top:bot,left,right]
        cv2.imwrite("out_img_path",cropped_img) #此处可以对剪裁之后的图片进行保存
    return frame_np
# 处理视频，绘制多个box
def add_bbx_for_video(video_path, det_path, out_video_path):
    cap = cv2.VideoCapture(video_path)  # 开始读取视频
    state, im = cap.read()
    im_shape = im.shape  # 根据输入视频的尺寸确定输出视频的尺寸
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')  # 通过更改这里以修改不同的视频编码方式
    out = cv2.VideoWriter(out_video_path, fourcc, 10.0, (im_shape[1], im_shape[0]))

    with open(det_path, "r") as f:

        gts = f.readlines()  # gts[0][0]第几帧 gts[0][2 3 4 5]为xywh [6]为conf
        sorted_gts = sort_tracklets(gts, camera_id)
        fr_id = 0

        frames = list(sorted_gts.keys())

        while (state):
            if fr_id not in frames or im is None:
                out.write(im)
                state, im = cap.read()
                fr_id += 1
            else:
                tracks = sorted_gts[fr_id]  # tracks 为每一帧
                for track in tracks:
                    left, top, right, bot, conf, object_id = track
                    im = plot_bbx(im, left, top, right, bot, conf, object_id)

                # cv2.wtrite(im) 利用cv2 可以对绘制box后的图片进行额外的保存
                out.write(im)
                state, im = cap.read()
                fr_id += 1

        cap.release()
        out.release()
    print(out_video_path, "is done")

if __name__ == '__main__':
    '''
    输入：视频，格式通过改文件名字确定
    ground truth / target标签格式：一个txt文档，其中包含若干行lines, 每一行为[object_id conf frame_index x y w h]
    （如果格式不对应只需要修改读取文档的代码部分即可）
    '''
    det_path = "../detections.txt"  # 根据使用情况修改
    video_path = "../video.avi"  # 根据使用情况修改
    out_video_path = "../video_out.mp4"  # 输出文件路径 当前代码支持格式为mp4 如需修改格式 需修改下文编码方式
    add_bbx_for_video(video_path, det_path, out_video_path, camera_id)
