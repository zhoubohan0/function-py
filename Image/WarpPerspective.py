import cv2
import numpy as np
import os
# 备注：一定按照左上、右上、左下、右下选择四个点

class WarpPerspective:
    def __init__(self, img, points):
        self.img = img
        self.points = points

    # 计算透视变换参数矩阵
    def cal_perspective_params(self, offset=(0, 0)):
        offset_x, offset_y = offset  # 设置偏移点。如果设置为(0,0),表示透视结果只显示变换的部分（也就是画框的部分）
        img_size = (self.img.shape[1], self.img.shape[0])
        src = np.float32(self.points)
        # 透视变换的四个点
        dst = np.float32([[offset_x, offset_y], [img_size[0] - offset_x, offset_y],
                          [offset_x, img_size[1] - offset_y], [img_size[0] - offset_x, img_size[1] - offset_y]])
        # 透视矩阵
        M = cv2.getPerspectiveTransform(src, dst)
        # 透视逆矩阵
        M_inverse = cv2.getPerspectiveTransform(dst, src)
        return M, M_inverse

    # 透视变换
    def img_perspect_transform(self):
        M, M_inverse = self.cal_perspective_params()
        img_size = (self.img.shape[1], self.img.shape[0])
        return cv2.warpPerspective(self.img, M, img_size)


def draw_line(image, points):
    img = image.copy()
    p1, p2, p3, p4 = points[0], points[1], points[2], points[3]
    # 画线
    img = cv2.line(img, p1, p2, (0, 0, 255), 3)
    img = cv2.line(img, p2, p4, (0, 0, 255), 3)
    img = cv2.line(img, p4, p3, (0, 0, 255), 3)
    img = cv2.line(img, p3, p1, (0, 0, 255), 3)
    return img


def on_EVENT_LBUTTONDOWN(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        global cnt, points, img, img_draw, src, ratio
        print((x, y))
        points.append((x, y))
        img_draw = cv2.circle(img_draw, (x, y), 10, (0, 0, 255), thickness=-1)
        cv2.imshow("window", img_draw)
        cnt += 1
        if cnt == 4:  # 选取四个点，必须保证左上、右上、左下、右下
            cv2.destroyWindow('window')
            # 透视变换
            transformer = WarpPerspective(img, points)
            trasform_img = transformer.img_perspect_transform()
            dsize = ( int(img.shape[1] * ratio[1]),int(img.shape[0] * ratio[0]),)
            result_img = cv2.resize(trasform_img, dsize=dsize)
            # 输出结果图片
            path, filename = os.path.split(src)
            name, ext = os.path.splitext(filename)
            cv2.imwrite(os.path.join(path, name + '_' + ext), result_img)
            labeled_img = draw_line(img, points)
            # 展示结果
            labeled_img = cv2.resize(labeled_img, dsize=dsize)
            show('selected region', dsize, (200, 200), labeled_img)
            show('warpPerspective', dsize, (600, 200), result_img)


def show(winname, dsize, pos, img):
    cv2.namedWindow(winname, cv2.WINDOW_AUTOSIZE)
    cv2.resizeWindow(winname, dsize)
    cv2.moveWindow(winname, *pos)
    cv2.imshow(winname, img)


if __name__ == '__main__':
    # 输入：图片路径和输出图片缩放比例
    src = r'C:\Users\zhoubohan\Desktop\test.jpg'
    ratio = (0.9,0.9)

    # 传入回调函数的变量
    cnt = 0
    points = []
    img = cv2.imread(src)
    img_draw = img.copy()
    # 显示窗口
    cv2.namedWindow('window', 0)
    cv2.setMouseCallback("window", on_EVENT_LBUTTONDOWN)  # 回调函数
    cv2.imshow('window', img)
    cv2.waitKey()
