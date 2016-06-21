"""
    本模块分为3部分：
    1、collect_url()函数创建需要下载图片的网页URL
    2、collect_picture_link()将网页URL中的图片URL抓取出来
    3、database()将网页URL、网页标题、网页中的图片URL 3项保存到SQLite数据库
"""
import requests
from bs4 import BeautifulSoup
import sqlite3

def collect_url():
    """创建需要下载图片的网页URL"""

    url_list = []
    # 起始网页
    start = 5223
    # 结束网页
    end = 5230
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

def database(url,title,link):
    """将网页URL、网页标题、网页中的图片URL保存到SQLite数据库"""

    # 连接数据库
    conn = sqlite3.connect('picture_url.db')
    cur = conn.cursor()
    # 创建一个表
    cur.execute('CREATE TABLE IF NOT EXISTS picture (page TEXT, title TEXT, url TEXT)')
    # 插入数据
    cur.execute("INSERT INTO picture VALUES ('%s','%s','%s')" % (url,title,link))
    cur.close()
    conn.commit()
    conn.close()

def run():
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36',
              }
    url_list = collect_url()
    for url in url_list:
        response = requests.get(url, headers=header, timeout=30)
        response.encoding = 'gb2312'

        soup = BeautifulSoup(response.text, "html.parser")
        links = collect_picture_link(soup)

        title = soup.title.string[:-6]
        for link in links:
            database(url,title,link)

if __name__ == '__main__':
    run()