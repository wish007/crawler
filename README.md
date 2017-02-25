# 爬虫



## 爬取目标：

http://www.meizitu.com/



## 用到的库

- requests
- BeautifulSoup
- aiohttp
- asyncio（标准库）



## 实现功能

- 使用 requests 库模拟 HTTP 请求获取页面响应
- 使用 BeautifulSoup 解析出页面图片的 URL 、获取页面标题，将图片保存到以页面标题为名的文件夹
- 将页面 URL 、页面标题、图片 URL 保存到 SQLite 数据库
- 实现爬取过程中异常情况的处理



# 更新

aiohttp 是基于 asyncio 实现的 HTTP 框架，能实现异步高并发，使用后相比原程序有相当大的提升，测试中下载速度能几乎跑满带宽

未使用 aiohttp：meizitu.py

使用 aiohttp：meizitu_asynchronous.py

有兴趣的可以下载测试 :)

我的博客中关于 asyncio 和 aiohttp 的介绍：[使用asyncio和aiohttp实现异步IO](http://wish007.github.io/2017/02/25/%E4%BD%BF%E7%94%A8asyncio%E5%92%8Caiohttp%E5%AE%9E%E7%8E%B0%E5%BC%82%E6%AD%A5IO/)