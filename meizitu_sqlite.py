"""
    本模块分为2部分：
    1、urls()函数返回需要下载图片的网页URL
    2、collect_picture_link()将网页URL中的图片URL抓取出来
"""
import requests
from bs4 import BeautifulSoup
import sqlite3

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

def run():
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36',
              }
    # 连接数据库
    conn = sqlite3.connect('picture_url.db')
    cur = conn.cursor()
    # 创建一个表，将网页URL、网页标题、网页中的图片URL保存到SQLite数据库
    cur.execute('CREATE TABLE IF NOT EXISTS picture (page TEXT, title TEXT, url TEXT)')
    try:
        for url in urls():
        # 加入异常处理，防止网页无效导致抓取异常
            response = requests.get(url, headers=header, timeout=30)
            response.encoding = 'gb2312'
            soup = BeautifulSoup(response.text, "html.parser")
            try:
                title = soup.title.string[:-6]
                links = collect_picture_link(soup)
                for link in links:
                    # 将图片链接插入数据库
                    cur.execute("INSERT INTO picture VALUES ('%s','%s','%s')" % (url,title,link))
                    print(url + ' 已写入数据库')
            except TypeError:
                title = 'Empty'
                link = 'Empty'
                # 将无图片的URL插入数据库
                cur.execute("INSERT INTO picture VALUES ('%s','%s','%s')" % (url,title,link))
                print(url + ' 没有图片')
    except KeyboardInterrupt:
        cur.close()
        conn.commit()
        conn.close()
    else:
        cur.close()
        conn.commit()
        conn.close()

if __name__ == '__main__':
    run()
