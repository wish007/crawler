import os
from bs4 import BeautifulSoup
import asyncio
import aiohttp


header = {'User-Agent': 'Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko) \
          Chrome/49.0.2623.110 Safari/537.36', 'content-encoding': 'gzip'
          }


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

    try:
        title = soup.title.string[:-6]
        url_cut = len(url) - 5
        url_id = url[25:url_cut]
        # Python文件的绝对路径
        path = os.path.dirname(os.path.realpath(__file__))
        if not os.path.exists(path + '/' + url_id + ' ' + title):
            os.mkdir(path + '/' + url_id + ' ' + title)
        dir = path + '/' + url_id + ' ' + title + '/'
        return dir
    except TypeError:
        print('页面无图片! %s' % url)


@asyncio.coroutine
def download_picture(picture_link, dir, header):
    """下载并保存图片"""

    picture_name = picture_link[-18:].replace('/', '-')
    try:
        with aiohttp.Timeout(20):
            if not os.path.exists(dir + picture_name):
                print('开始下载图片 %s' % picture_link)
                r = yield from aiohttp.request('GET',
                                               picture_link, headers=header)
                picture = yield from r.read()
                with open(dir + picture_name, 'wb') as file:
                    file.write(picture)
                    print('图片下载成功 %s' % picture_name)
    except asyncio.TimeoutError:
        print('下载图片超时 %s' % picture_name)
    except Exception as e:
        raise e


@asyncio.coroutine
def get_html(url):
    """获取页面 html 文件并用 BeautifulSoup 解析出图片链接"""

    try:
        with aiohttp.Timeout(40):
            print('正在获取页面 %s' % url)
            r = yield from aiohttp.request('GET', url, headers=header)
            print('获取页面成功 %s' % url)
            t = yield from r.text(encoding='gbk')
            soup = BeautifulSoup(t, "html.parser")
            dir = create_directory(url, soup)
            links = collect_picture_link(soup)
            for picture_link in links:
                yield from download_picture(picture_link, dir, header)
    except asyncio.TimeoutError:
        print('获取页面超时 %s' % url)
    except Exception as e:
        raise e


def run():
    tasks = []
    for url in urls():
        tasks.append(get_html(url))
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
    print('所有图片下载完成!')


if __name__ == '__main__':
    run()
