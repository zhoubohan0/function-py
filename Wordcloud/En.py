import os
from os import path
import numpy as np
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from matplotlib import pyplot as plt


def wc_english(text_file, mask_file, outputpath='./output', bg_color='white'):  # #383838-灰色背景，blues-colormap
    # 获取文本text
    text = open(text_file).read()
    # 读取背景图片
    img = plt.imread(mask_file)
    background_Image = np.array(img * 255, dtype=np.uint8) if img.max() <= 1 else np.array(img, dtype=np.uint8)
    # 提取背景图片颜色
    img_colors = ImageColorGenerator(background_Image)
    # 设置英文停止词
    stopwords = set(STOPWORDS)
    wc = WordCloud(
        margin=2,  # 设置页面边缘
        mask=background_Image,
        scale=2,
        max_words=200,  # 最多词个数
        min_font_size=4,  # 最小字体大小
        stopwords=stopwords,
        random_state=42,
        background_color=bg_color,  # 背景颜色
        colormap=None,
        max_font_size=150,  # 最大字体大小
    )
    # 生成词云
    wc.generate_from_text(text)
    # 根据图片色设置背景色
    wc.recolor(color_func=img_colors)
    # 存储图像
    wc.to_file(os.path.join(outputpath, f'wordcloud{len(os.listdir(outputpath)) + 1}.png'))
    # 显示图像
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    d = path.dirname(__file__) if "__file__" in locals() else os.getcwd()
    text_file = path.join(d, 'input', 'test.txt')
    mask_file = path.join(d, 'input', "mask.png")
    wc_english(text_file, mask_file)
