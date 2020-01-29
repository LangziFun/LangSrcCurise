#coding:utf-8
import requests,os,re,time
import requests
requests.packages.urllib3.disable_warnings()
import re
import random
import time
import re
from urllib.parse import urlparse
import socket
from concurrent.futures import ThreadPoolExecutor
import difflib
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

    def get_host(self):
        url = self.url.split('//')[1]
        if ':' in url:
            url = url.split(':')[0]
        try:
            s = socket.gethostbyname(url)
            return str(s)
        except Exception as e:
            time.sleep(2)
            try:
                s = socket.gethostbyname(url)
                return str(s)
            except Exception as e:
                return '获取失败'

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
            'status':status,
            'ip':str(self.get_host())
        }
        #print(self.result)
        return self.result
def Return_Content_Difflib(original, compare):
    '''
    对比传入字符串相似度
    :param original: 要判断的字符串1
    :param compare: 要判断的字符串1
    :return: 返回结果是相似度判断结果
        如果相似度非常大则返回True
        否则返回False
    '''
    res = int(str(difflib.SequenceMatcher(None,original, compare).quick_ratio()*10000).split('.')[0])
    if res>8500:
        return True
    else:
        return False
    # return 4 integer like 1293 or 9218

def GetDomainsInfos(domain):
    '''
    2020-01-14
    该函数用来过滤泛解析
    原理如下：
        - 访问一个不存在的网址，获取【标题，ip，网页内容】
        - 首先第一步对比 标题 是否一样

        - 如果标题不一样则判定为 非泛解析
                保存到域名资产+网络资产
        - 如果标题一样
            - 则进一步判断ip和网页内容
            - 如果网页内容相似度非常高
            - 认定为泛解析，保存到 排除资产数据表
    '''
    ORICOM = {domain:{'title': 'None', 'ip': 'None', 'content': 'None'}}
    DD = Get_Url_Info('http://shanghai.{}'.format(domain)).get_info()
    ORICOM[domain]['title'],ORICOM[domain]['ip'],ORICOM[domain]['content'], = DD['title'],DD['ip'],DD['content']
    return ORICOM

def DomainsInfos(domains):
    # 接受数据为一个列表的子域名-->['qq.com','yy.com','iqiyi.com']
    '''
    接受的参数如下
    ['qq.com','yy.com','iqiyi.com']
    返回的数据格式如下
    {'qq.com': {'title': '获取失败', 'ip': '220.250.64.225', 'content': 'Error'}, 'yy.com': {'title': '403 Forbidden', 'ip': '125.39.99.224', 'content': '<html>\r\n<head><title>403 Forbidden</title></head>\r\n<body bgcolor="white">\r\n<center><h1>403 Forbidden</h1></center>\r\n<hr><center>nginx</center>\r\n</body>\r\n</html>\r\n<!-- a padding to disable MSIE and Chrome friendly error page -->\r\n<!-- a padding to disable MSIE and Chrome friendly error page -->\r\n<!-- a padding to disable MSIE and Chrome friendly error page -->\r\n<!-- a padding to disable MSIE and Chrome friendly error page -->\r\n<!-- a padding to disable MSIE and Chrome friendly error page -->\r\n<!-- a padding to disable MSIE and Chrome friendly error page -->\r\n'}, 'iqiyi.com': {'title': '获取失败', 'ip': '220.250.64.225', 'content': 'Error'}}
    '''
    try:
        if os.path.exists('DomainsInfos.txt'):
            with open('DomainsInfos.txt', 'r', encoding='utf-8')as a:
                DOMAINSINFOS = eval(a.read())
            if len(list(DOMAINSINFOS.keys())) != len(domains) or list(set(DOMAINSINFOS.keys()).difference(set(domains))) != []:
                os.remove('DomainsInfos.txt')
                with ThreadPoolExecutor() as pool:
                    res = pool.map(GetDomainsInfos, domains)
                r = {}
                for d in res:
                    r.update(d)
                with open('DomainsInfos.txt', 'a+', encoding='utf-8')as a:
                    a.write(str(r))
                return r
            else:
                return DOMAINSINFOS
        else:
            with ThreadPoolExecutor() as pool:
                res = pool.map(GetDomainsInfos, domains)
            r = {}
            for d in res:
                r.update(d)
            with open('DomainsInfos.txt', 'a+', encoding='utf-8')as a:
                a.write(str(r))
            return r
    except Exception as e:
        if os.path.exists('DomainsInfos.txt'):
            os.remove('DomainsInfos.txt')
        with ThreadPoolExecutor() as pool:
            res = pool.map(GetDomainsInfos, domains)
        r = {}
        for d in res:
            r.update(d)
        with open('DomainsInfos.txt', 'a+', encoding='utf-8')as a:
            a.write(str(r))
        return r


if __name__ == '__main__':
    #print(Get_Url_Info('https://dxiyi.taobao.com/').Requests()[0].decode())
    # 如下是获取泛解析数据信息
    #Domains = ['qq.com','yy.com','iqiyi.com']
    #print(DomainsInfos(Domains))

    # ORICOM = eval(str(dict.fromkeys(Domains,{'title':'None','ip':'None','content':'None'})))
    # print(ORICOM)
    # for dom in Domains:
    #     DD = Get_Url_Info('http://asyyyyyyyyyyyyyy.{}'.format(dom)).get_info()
    #     print(DD)
    #     ORICOM[dom]['title'],ORICOM[dom]['ip'],ORICOM[dom]['content'], = DD['title'],DD['ip'],DD['content']
    # print(ORICOM)
    #

    a = Get_Url_Info('http://www.a.yy.com')
    print(a.get_info())
    #
    b = Get_Url_Info('http://ssssssssssssss.yy.com')
    print(b.get_info())
    # print('------------------------')
    print(Return_Content_Difflib(a.get_info()['content'],b.get_info()['content']))
