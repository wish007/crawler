import requests
from bs4 import BeautifulSoup
import sqlite3

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36'
          }

class Meizitu():

    def __init__(self, start, end):
        self.start = start
        self.end = end

    def url(self):
        while self.start < self.end:
            yield 'http://www.meizitu.com/a/%s.html' % self.start
            self.start +=1

    def picture(self, url):
        r = requests.get(url, headers=header, timeout=30)
        r.encoding = 'gb2312'
        soup = BeautifulSoup(r.text, "html.parser")
        try:
            title = soup.title.string[:-6]
            for links in soup.find_all(class_='postContent'):
                for l in links.find_all('img'):
                    link = l.get('src')
                    yield title, link
        except TypeError:
            title = 'Empty'
            link = 'Empty'
            return title, link

    def save(self, url, title, link):
        cur.execute("INSERT INTO meizitu VALUES ('%s','%s','%s')" % (url,title,link))
        print(url + ' 已写入数据库')

if __name__ == '__main__':
    mzt = Meizitu(500, 502)
    conn = sqlite3.connect('meizitu.db')
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS meizitu (page TEXT, title TEXT, url TEXT)')
    try:
        for url in mzt.url():
            for title, link in mzt.picture(url):
                mzt.save(url, title, link)
    except KeyboardInterrupt:
        cur.close()
        conn.commit()
        conn.close()
    cur.close()
    conn.commit()
    conn.close()
