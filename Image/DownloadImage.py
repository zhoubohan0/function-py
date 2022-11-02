from bs4 import BeautifulSoup
import requests
import os
import re
def createuniquefilename(outputpath):
    i = 0
    filename = os.path.join(outputpath, f'{i}.jpg')
    while os.path.exists(filename):
        i+=1
        filename = os.path.join(outputpath, f'{i}.jpg')
    return filename
def DownloadImage(baseurl,search,outputpath):
    url = baseurl + search
    response = requests.get(url)
    html = response.text  # 可读类型
    # re.findall('img.*?src="(.*?)"', html)
    soup = BeautifulSoup(html, 'lxml')
    tag_img = soup.find_all('img')
    for each in tag_img:
        src = each['src']
        if str.find(src,'http')!=-1:
            response2 = requests.get(src)
            filename = createuniquefilename(outputpath)
            # 如果文件很小，read()一次性读取最方便；
            # 如果不能确定文件大小，反复调用read(size)比较保险；
            # 如果是配置文件，调用readlines()最方便
            with open(filename,'wb')as f: # encoding='gbk'和errors='ignore'参数只能在非二进制读写中使用
                f.write(response2.content)





if __name__ == '__main__':
    baseurl = r'https://cn.bing.com/images/search?q='
    search = 'FACE'
    outputpath = r'C:\Users\dell\Desktop\test_face'
    DownloadImage(baseurl,search,outputpath)