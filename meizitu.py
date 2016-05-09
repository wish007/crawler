import requests
import os
from bs4 import BeautifulSoup

# 创建需要下载图片的URL
def collect_url():
    print('开始创建需要下载图片的URL')
    url_list = []
    # 起始网页
    start = 5200
    # 结束网页
    end = 5200
    while start <= end:
        url = 'http://www.meizitu.com/a/' + str(start) + '.html'
        url_list.append(url)
        start = start + 1
    return url_list

# 使用find_all()方法过滤
# for link in soup.find_all('img'):
#     print(link.name, link.get('alt'), link.get('src'))

# 搜集图片链接
def collect_picture_link(soup):
    print('BeautifulSoup匹配，搜集图片链接')
    picture_link_list = []
    for link_node in soup.find_all(id='picture'):
        for link in link_node.find_all('img'):
            picture_link_list.append(link.get('src'))
    return picture_link_list

# 获取网页标题，创建以标题为名的文件夹
def create_directory(url, soup):
    print('创建文件夹用来保存图片')
    title = soup.title.string[:-6]
    url_cut = len(url) - 5
    url_id = url[25:url_cut]
    # 目录/Users/love/Desktop/暂时替换为/Users/Administrator/Desktop/spider/
    if os.path.exists('/Users/love/Desktop/xx/' + url_id + ' ' + title):
        None
    else:
        os.mkdir('/Users/love/Desktop/xx/' + url_id + ' ' + title)
    dir = '/Users/love/Desktop/xx/' + url_id + ' ' + title + '/'
    return dir

# 开始下载图片
def download_picture(links, dir, header):
    print('开始下载图片')
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

        # 显示现在的网页编码
        # print(response.encoding)
        # 显示响应状态码
        # print(response.status_code)
        # 以文本方式显示网页响应
        # print(response.text)

        # BeautifulSoup的第2个参数是解析器，解析器主要有：自带的Python标准库解析器html.parser、lxml、html5lib
        soup = BeautifulSoup(response.text, "html.parser")
        links = collect_picture_link(soup)
        dir = create_directory(url, soup)
        download_picture(links, dir, header)

if __name__ == '__main__':
    run()
