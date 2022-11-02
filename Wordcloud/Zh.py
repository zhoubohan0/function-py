import matplotlib.pyplot as plt
import numpy as np
from wordcloud import WordCloud, ImageColorGenerator
from jieba import analyse
from PDFreader import read_pdf
import os


def generate_wordcloud(text_file, mask_file, font_file, outputpath='./output', bg_color='white'):
    mk = plt.imread(mask_file)  # 获得作为遮罩的图片
    mk = np.array(mk * 255, dtype=np.uint8) if mk.max() <= 1 else np.array(mk, dtype=np.uint8)
    text = read_pdf(text_file)  # 读取生成词云的文本
    wc = WordCloud(font_path=font_file, width=400, height=200, mask=mk, background_color=bg_color,
                   mode='RGBA')  # 生成词云对象bg_color
    ls = analyse.extract_tags(text, topK=200)  # jieba统计并提取权值topK的词语
    wc.generate(" ".join(ls))  # 将list转换为空格分隔的字符串，创建词云
    img_colors = ImageColorGenerator(mk)
    wc.recolor(color_func=img_colors)  # 将词云颜色设置为图片颜色
    # plt展示
    plt.figure()
    plt.imshow(wc.to_array(), interpolation='bilinear')
    plt.axis("off")
    plt.show()
    wc.to_file(os.path.join(outputpath, f'wordcloud{len(os.listdir(outputpath)) + 1}.png'))  # 保存图片


if __name__ == '__main__':
    inputpath = './input/'
    text_file = os.path.join(inputpath, 'test.pdf')
    mask_file = os.path.join(inputpath, 'cloud.jpg')
    font_file = "./ttf/xingkai.ttf"
    generate_wordcloud(text_file, mask_file, font_file)
