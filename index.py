import re
import sys
import urllib
import os
import requests
import hashlib

def get_pic_urls(onepageurl):
    try:
        html = requests.get(onepageurl).text
        reg = r'http[s]{0,}://[^\s]*.jpg|http[s]{0,}://[^\s]*.png' 
        imgre = re.compile(reg)  
        return re.findall(imgre, html)
    except Exception as e:
        print('出错了 ❌ ', e)
        pic_urls = []
        return pic_urls

def down_pic(imageFloder, pic_urls):
    """给出图片链接列表, 下载所有图片"""
    path = os.getcwd() + '/' + imageFloder
    folder = os.path.exists(path)
    if not folder:
        os.makedirs(path)
        print('图片存储路径：{} ，总共{}张图片'.format(path,len(pic_urls)))
    else:
        print('文件夹已存在，之前下载的图片将被覆盖')
    for i, pic_url in enumerate(pic_urls):
        try:
            fileName = pic_url.split('/')[-1]
            pic = requests.get(pic_url, timeout=15)
            string = path + '/' + fileName
            with open(string, 'wb') as f:
                f.write(pic.content)
                print('成功下载第%s张图片: %s' % (str(i + 1), str(pic_url)))
        except Exception as e:
            print('下载第%s张图片时失败: %s' % (str(i + 1), str(pic_url)))
            print(e)
            continue

if __name__ == '__main__':
    argvLen = len(sys.argv)
    if argvLen > 1 :
        all_pic_urls = []
        url = sys.argv[1]
        preHeaders = url.split('/')
        floderName = ""
        floderNameMD5 = hashlib.md5(url.encode('utf-8')).hexdigest()
        if len(preHeaders) > 3 :
            floderName = preHeaders[2] + '-' + floderNameMD5
        else:
            floderName = floderNameMD5
        print(floderName)
        pic_urls = get_pic_urls(url)
        if len(pic_urls) > 0 :
            all_pic_urls.extend(pic_urls)
            down_pic(floderName, list(set(all_pic_urls)))
        else:
            print('❌ 没有检测到图片')
    else:
        print('❌ 缺少参数：web url')
        exit(1)
    
