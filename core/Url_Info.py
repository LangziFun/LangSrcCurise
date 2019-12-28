# -*- encoding: utf-8 -*- 
"""
@author: LangziFun
@Blog: www.langzi.fun
@time: 2019/8/5 21:46
@file: 获取网址信息.py
"""
import requests
requests.packages.urllib3.disable_warnings()
import re
import random
import time
import re
from urllib.parse import urlparse

_Headers = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"]


'''
2019-12-28
新增获取网址标题
'''
Alive_Status = range(1000)
def get_title(r):
    title = '获取失败'
    try:
        title_pattern = b'<title>(.*?)</title>'
        title = re.search(title_pattern, r, re.S | re.I).group(1)
        try:
            title = title.decode().replace('\n', '').strip()
            return title
        except:
            try:
                title = title.decode('gbk').replace('\n', '').strip()
                return title
            except:
                return title
    except:
        return title
    finally:
        return title
def RequestsTitle(url):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
    title = '获取失败'
    title1 = '获取失败'
    title2 = '获取失败'
    content1 = None
    content2 = None
    try:
        r = requests.get(url=url,headers=headers,verify=False,timeout=20)
        if b'text/html' in r.content or b'<title>' in r.content or b'</html>' in r.content:
            content1 = r.content
        if int(r.status_code) in Alive_Status:
            u = urlparse(str(r.url))
            title1 = get_title(r.content)
            url1 = u.scheme + '://' + u.netloc
    except Exception as e:
        pass
    try:
        r = requests.get(url=url,headers=headers,verify=False,timeout=20)
        if b'text/html' in r.content or b'<title>' in r.content or b'</html>' in r.content:
            content2 = r.content
        if int(r.status_code) in Alive_Status:
            u = urlparse(str(r.url))
            title2 = get_title(r.content)
            url2 = u.scheme + '://' + u.netloc
    except Exception as e:
        pass
    if title1 != '获取失败':
        return title1
    if title2 != '获取失败':
        return title2
    if content1 != None:
        return title
    if content2 != None:
        return title
    return title

class Get_Url_Info:
    def __init__(self,url):
        self.url = url
        self.timeout = 10
        self.title = '获取失败'
        self.power = '获取失败'
        self.server = '获取失败'
        self.content = 'Error'
        self.headers = '获取失败'
        self.status = '1'
        self.result = {}

    def Requests(self):
        try:
            r = requests.get(url=self.url,headers={'User-Agent':random.choice(_Headers)},verify=False,timeout=self.timeout)
            return (r.content,r.headers,r.status_code)
        except Exception as e:
            try:
                r = requests.get(url=self.url, headers={'User-Agent': random.choice(_Headers)}, verify=False,timeout=self.timeout)
                return (r.content, r.headers, r.status_code)
            except:
                return (self.content,self.headers,self.status)
        #     try:
        #         encoding = requests.utils.get_encodings_from_content(r.text)[0]
        #         #print(encoding)
        #         content = r.content.decode(encoding,'replace')
        #         #print(content)
        #         return (content, r.headers, r.status_code)
        #     except:
        #         return (self.content, r.headers, r.status_code)
        # except Exception as e:
        #     #print(e)
        #     return (self.content,self.headers,self.status)

    def get_title(self,content):
        if content == 'Error':
            return self.title
        try:
            title_pattern = b'<title>(.*?)</title>'
            title = re.search(title_pattern, content, re.S | re.I).group(1)
            try:
                title = title.decode().replace('\n', '').strip()
                return title
            except:
                try:
                    title = title.decode('gbk').replace('\n', '').strip()
                    return title
                except:
                    return self.title
        except:
            return self.title

    def get_headers(self,headers):
        if headers == '获取失败':
            return (self.power,self.server)
        power,server=headers.get('Server'), headers.get('X-Powered-By')
        power = [power if power is not None else self.power][0]
        server = [server if server is not None else self.power][0]
        return (power,server)

    def get_info(self):
        req = self.Requests()
        if req[0] == 'Error':
            req = self.Requests()
        content = req[0]
        headers = req[1]
        status = req[2]
        title = self.get_title(content)
        power,server = self.get_headers(headers)

        try:
            content = content.decode().replace(r'\r','').replace(r'\n','')
        except:
            try:
                content = content.decode('gbk').replace(r'\r','').replace(r'\n','')
            except:
                content = self.content

        self.result = {
            'url':self.url,
            'title':title,
            'power':power,
            'server':server,
            'content':content,
            'status':status
        }
        #print(self.result)
        return self.result

if __name__ == '__main__':
    #print(Get_Url_Info('https://dxiyi.taobao.com/').Requests()[0].decode())
    a = Get_Url_Info('https://170.taobao.com')
    print(a.get_info()['content'])
    # '''
    # 传入数据为 网址https://dxiyi.taobao.com/
    # 返回数据为
    # {
    # url 网址
    # title 标题
    # power WEB容器
    # server 服务器
    # content 网页内容
    # status 状态码
    # }
    # '''