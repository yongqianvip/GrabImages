import re
import sys
import urllib
import os
import requests


def getPage(keyword, page, n):
    page = page * n
    keyword = urllib.parse.quote(keyword, safe='/')
    url_begin = "http://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word="
    url = url_begin + keyword + "&pn=" + str(page) + "&gsm=" + str(hex(page)) + "&ct=&ic=0&lm=-1&width=0&height=0"
    return url

def get_onepage_urls(onepageurl):
    try:
        html = requests.get(onepageurl).text
    except Exception as e:
        print(e)
        pic_urls = []
        return pic_urls
    pic_urls = re.findall('"objURL":"(.*?)",', html, re.S)
    return pic_urls


def down_pic(floderName, pic_urls):
    """给出图片链接列表, 下载所有图片"""
    path = os.getcwd() + '/' + floderName
    folder = os.path.exists(path)
    if not folder:
        os.makedirs(path)
        print('图片存储路径：{} ，总共{}张图片'.format(path,len(pic_urls)))
    else:
        print('文件夹已存在，之前下载的图片将被覆盖')
    for i, pic_url in enumerate(pic_urls):
        try:
            pic = requests.get(pic_url, timeout=15)
            string = path + '/' + str(i + 1) + '.jpg'
            with open(string, 'wb') as f:
                f.write(pic.content)
                print('成功下载第%s张图片: %s' % (str(i + 1), str(pic_url)))
        except Exception as e:
            print('下载第%s张图片时失败: %s' % (str(i + 1), str(pic_url)))
            print(e)
            continue


if __name__ == '__main__':
    keyword = '狗'  # 关键词, 改为你想输入的词即可, 相当于在百度图片里搜索一样
    page_begin = 0
    page_number = 30
    image_number = 10
    all_pic_urls = []
    while 1:
        if page_begin > image_number:
            break
        print("第{}次请求数据".format(page_begin))
        url = getPage(keyword, page_begin, page_number)
        onepage_urls = get_onepage_urls(url)
        page_begin += 1

        all_pic_urls.extend(onepage_urls)
        # set 过滤重复项
    down_pic(keyword, list(set(all_pic_urls)))
