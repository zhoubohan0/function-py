import matplotlib.pyplot as plt
import cv2
import os
from glob import glob
def plotgrid(imgpath,nrows,ncols,figsize,labellist,labelsize,outputfile):
    fig, ax = plt.subplots(nrows=nrows, ncols=ncols,figsize=figsize)
    imgfilels = glob(os.path.join(imgpath,'*.*'))  # 默认排序
    for i in range(nrows*ncols):
        ax[i//ncols][i%ncols].imshow(cv2.imread(imgfilels[i]))
        ax[i // ncols][i % ncols].set_title(labellist[i],fontsize=labelsize)
        ax[i // ncols][i % ncols].axis('off')
    fig.show()
    fig.savefig(outputfile)

if __name__ == '__main__':
    imgpath = './dataset/test/PNEUMONIA/'
    nrows, ncols = 2,4
    figsize = (24,12)
    labellist = [f'Label: Pneumonia\nPrediction: Pneumonia']*(nrows*ncols)
    labelsize = 25
    outputfile = f'./visulize/test_Pneumonia.png'
    plotgrid(imgpath,nrows, ncols,figsize,labellist,labelsize,outputfile)