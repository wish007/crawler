"""
    本模块分为4部分：
    1、collect_url()函数创建需要下载图片的网页URL
    2、collect_picture_link()函数将网页URL中的图片URL抓取出来
    3、create_directory()函数创建以网页标题为名称的文件夹
    4、download_picture()函数下载并保存图片到本地文件夹
"""
import requests
import os
from bs4 import BeautifulSoup


def collect_url():
    """创建需要下载图片的网页URL"""

    url_list = []
    # 起始网页
    start = 5200
    # 结束网页
    end = 5201
    while start <= end:
        url = 'http://www.meizitu.com/a/' + str(start) + '.html'
        url_list.append(url)
        start = start + 1
    return url_list

def collect_picture_link(soup):
    """将网页URL中的图片URL抓取出来"""

    picture_link_list = []
    for link_node in soup.find_all(id='picture'):
        for link in link_node.find_all('img'):
            picture_link_list.append(link.get('src'))
    return picture_link_list

def create_directory(url, soup):
    """创建以标题为名的文件夹"""

    title = soup.title.string[:-6]
    url_cut = len(url) - 5
    url_id = url[25:url_cut]
    # Python文件的绝对路径
    path = os.path.dirname(os.path.realpath(__file__))
    if os.path.exists(path + '/' + url_id + ' ' + title):
        None
    else:
        os.mkdir(path + '/' + url_id + ' ' + title)
    dir = path + '/' + url_id + ' ' + title + '/'
    return dir

def download_picture(links, dir, header):
    """下载并保存图片"""

    i = 1
    for picture_link in links:
        picture_name = picture_link[-18:].replace('/','-')
        if os.path.exists(dir + picture_name):
            None
        else:
            picture = requests.get(picture_link, headers=header, timeout=50)
            with open(dir + picture_name, 'wb') as file:
                file.write(picture.content)
                print('第 ' + str(i) + ' 张完成')
                i = i + 1

def run():
    # 加入headers模拟浏览器请求
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36',
              }
    url_list = collect_url()
    for url in url_list:
        # 加入timeout超时时间
        response = requests.get(url, headers=header, timeout=30)
        # 将返回的网页编码强制设定为‘gb2312’，防止request将返回解析为其他编码
        response.encoding = 'gb2312'
        # BeautifulSoup的第2个参数是解析器，解析器主要有：自带的Python标准库解析器html.parser、lxml、html5lib
        soup = BeautifulSoup(response.text, "html.parser")
        links = collect_picture_link(soup)
        dir = create_directory(url, soup)
        download_picture(links, dir, header)

if __name__ == '__main__':
    run()
