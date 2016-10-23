"""
    本模块分为4部分：
    1、urls()函数返回需要下载图片的网页URL
    2、collect_picture_link()函数将网页URL中的图片URL抓取出来
    3、create_directory()函数创建以网页标题为名称的文件夹
    4、download_picture()函数下载并保存图片到本地文件夹
"""
import requests
import os
from bs4 import BeautifulSoup


def urls():
    """返回需要下载图片的网页URL"""
    start_url = int(input('请输入开始页面编号：'))
    end_url = int(input('请输入结束页面编号：'))
    while start_url < end_url:
        yield 'http://www.meizitu.com/a/%s.html' % start_url
        start_url += 1

def collect_picture_link(soup):
    """将网页URL中的图片URL抓取出来"""

    picture_link_list = []
    for link_node in soup.find_all(class_='postContent'):
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
            i = i + 1
        else:
            picture = requests.get(picture_link, headers=header, timeout=50)
            with open(dir + picture_name, 'wb') as file:
                file.write(picture.content)
                print('第 %s 张完成' % i)
                i = i + 1

def run():
    # 加入headers模拟浏览器请求
    header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36',
              'content-encoding':'gzip'
              }
    for url in urls():
        print('开始下载：' + url)
        # 加入timeout超时时间
        response = requests.get(url, headers=header, timeout=30)
        # 将返回的网页编码强制设定为‘gb2312’，防止request将返回解析为其他编码
        response.encoding = 'gb2312'
        # BeautifulSoup的第2个参数是解析器，解析器主要有：自带的Python标准库解析器html.parser、lxml、html5lib
        soup = BeautifulSoup(response.text, "html.parser")
        # 加入异常处理，防止网页无效导致抓取异常，未完成编写
        try:
            links = collect_picture_link(soup)
            dir = create_directory(url, soup)
            download_picture(links, dir, header)
        except TypeError:
            print(url + ' 没有图片')

if __name__ == '__main__':
    run()
