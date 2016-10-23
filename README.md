# 爬虫

## 爬取目标：

http://www.meizitu.com/

## 用到的库

- requests
- BeautifulSoup

## 实现功能

- 使用 requests 库模拟 HTTP 请求获取页面响应
- 使用 BeautifulSoup 解析出页面图片的 URL 、获取页面标题，将图片保存到以页面标题为名的文件夹
- 将页面 URL 、页面标题、图片 URL 保存到 SQLite 数据库
- 实现爬取过程中异常情况的处理