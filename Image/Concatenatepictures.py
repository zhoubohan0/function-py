import PIL.Image as Image
import os
def concatenatepictures():
    IMAGES_PATH = r'.\face_fig\compare\collect'  # 图片集地址
    IMAGES_FORMAT = ['.jpg', '.JPG']  # 图片格式
    IMAGE_SIZE = 256  # 每张小图片的大小
    IMAGE_COLUMN = 4  # 图片间隔，也就是合并成一张图后，一共有几列
    # IMAGE_ROW = 4  # 图片间隔，也就是合并成一张图后，一共有几行
    IMAGE_SAVE_PATH = r'.\face_fig\compare\save'+ '\\mix.jpg'  # 图片转换后的地址
    # 获取图片集地址下的所有图片名称
    image_names = [name for name in os.listdir(IMAGES_PATH) for item in IMAGES_FORMAT if
                   os.path.splitext(name)[1] == item]

    IMAGE_ROW = len(image_names) // IMAGE_COLUMN
    if len(image_names) % IMAGE_COLUMN : IMAGE_ROW +=1


    # 定义图像拼接函数
    to_image = Image.new('RGB', (IMAGE_COLUMN * IMAGE_SIZE, IMAGE_ROW * IMAGE_SIZE))  # 创建一个新图
    # 循环遍历，把每张图片按顺序粘贴到对应位置上
    total_num = 0
    for y in range(0, IMAGE_ROW ):
        for x in range(0, IMAGE_COLUMN ):
            from_image = Image.open(IMAGES_PATH + '\\' + image_names[IMAGE_COLUMN * y + x ]).resize(
                (IMAGE_SIZE, IMAGE_SIZE), Image.ANTIALIAS)
            to_image.paste(from_image, (x * IMAGE_SIZE, y * IMAGE_SIZE))
            total_num += 1
            if total_num == len(image_names):
                break
    to_image.save(IMAGE_SAVE_PATH)  # 保存新图