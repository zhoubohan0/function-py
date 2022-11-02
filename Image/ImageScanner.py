import cv2
import numpy as np
import os
from skimage.filters import threshold_local
import imutils
from imutils import perspective
def show(img):
    winname = zh_cn("output")
    cv2.namedWindow(winname, cv2.WINDOW_NORMAL)
    cv2.imshow(winname, img)
    cv2.waitKey(0)

# 中文显示
def zh_cn(string):
    return string.encode("GBK").decode(errors="ignore")


def scan_(filename, issave=False): # 未测试函数
    def rectify(h):
        h = h.reshape((4, 2))  # 改变数组的形状，变成4*2形状的数组
        hnew = np.zeros((4, 2), dtype=np.float32)  # 创建一个4*2的零矩阵
        # 确定检测文档的四个顶点
        add = h.sum(1)
        hnew[0] = h[np.argmin(add)]  # argmin()函数是返回最大数的索引
        hnew[2] = h[np.argmax(add)]

        diff = np.diff(h, axis=1)  # 沿着制定轴计算第N维的离散差值
        hnew[1] = h[np.argmin(diff)]
        hnew[3] = h[np.argmax(diff)]

        return hnew

    image = cv2.imread(filename)
    # 重新设置图片的大小，以便对其进行处理:选择最佳维度，以便重要内容不会丢失
    image = cv2.resize(image, (1500, 880))
    # 创建原始图像的副本
    orig = image.copy()
    # 对图像进行灰度处理，并进而进行行高斯模糊处理
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    # 使用canny算法进行边缘检测
    edged = cv2.Canny(blurred, 0, 50)
    # 创建canny算法处理后的副本
    orig_edged = edged.copy()
    # 找到边缘图像中的轮廓，只保留最大的，并初始化屏幕轮廓
    # findContours()函数用于从二值图像中查找轮廓
    contours, hierarchy = cv2.findContours(edged, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    # 使用python中的sorted函数返回contours重新排序的结果（降序），排序规则（key）：根据计算的轮廓面积大小
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    # 得到近似轮廓
    for c in contours:
        p = cv2.arcLength(c, True)  # 计算封闭轮廓的周长或者曲线的长度
        approx = cv2.approxPolyDP(c, 0.02 * p, True)  # 指定0.02*p精度逼近多边形曲线，这种近似曲线为闭合曲线,因此参数closed为True

        if len(approx) == 4:  # 如果逼近的是四边形
            target = approx  # 则此轮廓为要找的轮廓
            break  # 找到即跳出循环

    # 将目标映射到800*800四边形
    approx = rectify(target)
    pts2 = np.float32([[0, 0], [800, 0], [800, 800], [0, 800]])

    # 透视变换
    # 使用gtePerspectiveTransform函数获得透视变换矩阵：approx是源图像中四边形的4个定点集合位置；pts2是目标图像的4个定点集合位置
    M = cv2.getPerspectiveTransform(approx, pts2)
    # 使用warpPerspective函数对源图像进行透视变换，输出图像dst大小为800*800
    dst = cv2.warpPerspective(orig, M, (800, 800))
    # 画出轮廓，-1表示所有的轮廓，画笔颜色为（0,255,0），粗细为2
    cv2.drawContours(image, [target], -1, (0, 255, 0), 2)
    # 对透视变换后的图像进行灰度处理
    dst = cv2.cvtColor(dst, cv2.COLOR_BGR2GRAY)

    # 对透视变换后的图像使用阈值进行约束获得扫描结果

    # 使用固定阈值操作：threshold()函数：有四个参数：第一个是原图像，第二个是进行分类的阈值，第三个是高于(低于)阈值时赋予的新值，
    # 第四个是一个方法选择参数：cv2.THRESH_BINARY(黑白二值)
    # 该函数返回值有两个参数，第一个是retVal(得到的阈值值(在OTSU会用到))，第二个是阈值化后的图像
    ret, th1 = cv2.threshold(dst, 127, 255, cv2.THRESH_BINARY)  # 进行固定阈值处理，得到二值图像
    # 使用Otsu's二值化，在最后一个参数加上cv2.THRESH_OTSU
    ret2, th2 = cv2.threshold(dst, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # 使用自适应阈值操作：adaptiveThreshold()函数
    # 第二个参数为领域内均值，第五个参数为规定正方形领域大小（11*11），第六个参数是常数C：阈值等于均值减去这个常数
    th3 = cv2.adaptiveThreshold(dst, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
    # 第二个参数为领域内像素点加权和，权重为一个高斯窗口，第五个参数为规定正方形领域大小（11*11），第六个参数是常数C：阈值等于加权值减去这个常数
    th4 = cv2.adaptiveThreshold(dst, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

    # 输出处理后的图像
    # cv2.imshow(zh_cn("原始图像"), orig)
    # cv2.imshow(zh_cn("原始图像经灰度变换"), gray)
    # cv2.imshow(zh_cn("原始图像经高斯模糊处理"), blurred)
    # cv2.imshow(zh_cn("原始图像经canny边缘检测后的结果"), orig_edged)
    # cv2.imshow(zh_cn("边界被标记的原图"), image)
    # cv2.imshow(zh_cn("warpPerspective"), dst) # 透视变换后的图像
    # cv2.imshow(zh_cn("fixed T"), th1)
    cv2.imshow(zh_cn("Otsu"), th2)
    # cv2.imshow(zh_cn("自适应阈值（领域内均值）3"), th3)
    # cv2.imshow(zh_cn("自适应阈值（领域内像素点加权和）4"), th4)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    if issave:
        cv2.imwrite('transformed_' + filename, th2)


def scan(filename,issave=False):
    name, ext = os.path.splitext(filename)
    img = cv2.imdecode(np.fromfile(filename, dtype=np.uint8), 1)  # 0:gray, 1:color，这样读取可以适应中文路径图片
    #转换大小 保存副本
    orig = img.copy()
    # img = imutils.resize(img,height = 500)

    #预处理 转灰度图->滤波->边缘检测
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray,(5,5),0)
    edge = cv2.Canny(gray,75,200)

    #寻找轮廓 按照面积排序
    cnt,_ = cv2.findContours(edge,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    cnt = sorted(cnt,key=cv2.contourArea,reverse = True)[:5]
    for c in cnt:
        #用vertex来记录每个轮廓的顶点
        peri = cv2.arcLength(c,True)
        vertex = cv2.approxPolyDP(c,0.02 * peri,True)
        #顶点个数是4 说明找到了四边形
        if len(vertex) == 4:
            break

    #透视变换
    transformed = perspective.four_point_transform(orig,vertex.reshape(4,2))
    transformed = cv2.cvtColor(transformed,cv2.COLOR_BGR2GRAY)

    # Otsu二值化
    T_OTSU,output1 = cv2.threshold(transformed, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    # 动态阈值,可调参决定效果
    T_adp = threshold_local(transformed,block_size=15,method='gaussian',offset = 15)
    output2 = (transformed > T_adp).astype('uint8') * 255

    # show(orig)
    show(transformed)
    show(output1)
    show(output2)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    if issave:
        # 中文路径名保存
        cv2.imencode(ext, transformed)[1].tofile("透视变换_" + filename)
        cv2.imencode(ext, output1)[1].tofile("扫描1_" + filename)
        cv2.imencode(ext, output2)[1].tofile("扫描2_" + filename)



if __name__ == '__main__':
    imgpath = '1.jpg'
    scan(imgpath, issave=True)
