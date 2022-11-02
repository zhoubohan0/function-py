import unicodedata
import re
import pickle
import numpy as np
import matplotlib.pyplot as plt
# unicodedata.numeric(s)  # 可以查找中文数字


def draw_loss(loss_list, save=False):
    # 定义画布大小
    fig = plt.figure(figsize=(6, 6))

    # style
    params = {
        "font.size": 14,  # 全局字号
        'font.family': 'STIXGeneral',  # 全局字体，微软雅黑(Microsoft YaHei)可显示中文
        "figure.subplot.wspace": 0.2,  # 图-子图-宽度百分比
        "figure.subplot.hspace": 0.4,  # 图-子图-高度百分比
        "axes.spines.right": True,  # 坐标系-右侧线
        "axes.spines.top": True,  # 坐标系-上侧线
        "axes.titlesize": 14,  # 坐标系-标题-字号
        "axes.labelsize": 14,  # 坐标系-标签-字号
        "legend.fontsize": 14,  # 图例-字号
        "xtick.labelsize": 12,  # 刻度-标签-字号
        "ytick.labelsize": 12,  # 刻度-标签-字号
        "xtick.direction": 'in',  # 刻度-方向
        "ytick.direction": 'in'  # 刻度-方向
    }
    '''
    plt.style.available                      # 查看所有可用样式列表
    plt.style.use('seaborn-colorblind')      # 使用样式
    '''
    plt.rcParams.update(params)

    # original_episode_reward
    epoch_list = range(len(loss_list[0]))
    for l in loss_list:
        plt.plot(epoch_list, l)
    plt.xlabel('Epoches')
    plt.ylabel('Loss')
    plt.grid(color='grey', linestyle='--', linewidth=0.5)
    plt.title('Training Loss')

    if save:  # 保存数据
        fig.savefig(f'training-loss.jpg')
    plt.show()

def extract(s,n_col):
    res = re.findall(r'-?\d+\.?\d*', s)
    table = np.float_(res).reshape(-1,n_col)
    return table

d = pickle.load(open('adversary.pkl','rb'))
# table = extract(s,4)
draw_loss([d['G'],d['D'][::5][:-1]])
pickle.dump(table[:,1].tolist(),open('.pkl','wb'))
print()
