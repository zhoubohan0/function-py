from argparse import ArgumentParser
from os import listdir,path,rename
from random import sample


def renamefile(dir,newname,shuffle = False):  # 默认变成1,2……+扩展名形式
    filelist = listdir(dir)
    if shuffle:
        filelist = sample(filelist,len(filelist))
    for i,file in enumerate(filelist):
        filename,extension = path.splitext(file)
        rename(path.join(dir,file),path.join(dir,newname+str(i+1)+extension))

def Rename(dir,newname,shuffle=True):
    # 修改时出现重名，newname = '$'执行一次，newname = ''再执行一次
    renamefile(dir,newname='#$@',shuffle=shuffle)
    renamefile(dir, newname=newname,shuffle=shuffle)

if __name__ == '__main__':
    parser = ArgumentParser(description="Rename each file in order(for .txt/.jpg ……) ")
    parser.add_argument('--dir',required=True,type=str,help='需重命名文件所在文件夹目录(双引号)')
    parser.add_argument('--name',default='',help='需要被统一修改的名字')
    parser.add_argument('--shuffle', default='True',type=bool,help='是否需要打乱')
    args = parser.parse_args()
    # print(args)
    dir = args.dir
    name = args.name
    Rename(dir,name,shuffle)
    print('Rename successfully!')
# 警告！一定会被打乱！
