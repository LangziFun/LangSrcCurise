# -*- encoding: utf-8 -*- 
import socket
import django
import os
import sys
pathname = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,pathname)
sys.path.insert(0,os.path.abspath(os.path.join(pathname,'..')))
os.environ.setdefault("DJANGO_SETTINGS_MODULE","LangSrcCurise.settings")
django.setup()
from app.models import Domains
from core.main import Add_Data_To_Url,close_old_connections
from concurrent.futures import ThreadPoolExecutor
from core.Url_Info import DomainsInfos
BA = Domains.objects.filter(curise='yes')
ALL_DOMAINS = [x.get('url') for x in BA.values()]
import requests,re
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}

class BeiAn:
    def __init__(self,keyword):
        self.keyword=keyword
        self.title_parrten = '<div class="_chinaz-seo-t2l">(.*?) <i class="iconfo'  # group(1) 正常
        self.ip_parrten = '>IP：.*?\?ip=(.*?)" target'  # group(1) 正常
        self.ages = '" target="_blank">(.*?)</a></div></div>'  # group(1)
        self.whois_id = '<a href="//icp.chinaz.com/.*?" target="_blank">(.*?)</a></i></span>'  # 需group(1)
        self.whois_type = '性质：.*?">(.*?)</i>'  # 需group(1)
        self.whois_name = '名称：.*?style=.*?">(.*?)</a>'  # 需group(1)
        self.whois_time = '审核时间.*?">(.*?)</i></span>'  # 需group(1)
        self.include_baidu = '<div class="Ma01LiRow w12-1 ">(.*?)</div>'  # group(1)
        self.infos = '<div class="MaLi03Row w180">(.*?)</div>'  # 要findall 0，1，2，3
        self.result={}

    def get_info_from_pattren(self,pattren, result):
        try:
            res = re.search(pattren, result,re.S|re.I).group(1)
            return res
        # return str(res.encode('utf-8'))
        except:
            return '暂无信息'

    def scan_seo(self):
        r = 0
        urls = 'http://seo.chinaz.com/' + self.keyword
        # url,title,weights,ip,ages,whois_id,whois_type,whois_name,whois_time
        # 网址，标题，百度权重，ip信息，年龄，备案号，备案性质，备案名称，备案时间
        # include_baidu,request,text,service,language
        # 百度收录，，协议类型，页面类型，服务器类型，程序语言
        try:
            req = requests.get(urls, headers, verify=False, timeout=10)
            encoding = requests.utils.get_encodings_from_content(req.text)[0]
            r = req.content.decode(encoding, 'replace')
        except Exception as e:
            print('第1次请求失败....')
            try:
                req = requests.get(urls, headers, verify=False, timeout=20)
                encoding = requests.utils.get_encodings_from_content(req.text)[0]
                r = req.content.decode(encoding, 'replace')
            except Exception as e:
                print('第2次请求失败....')
                try:
                    req = requests.get(urls, headers, verify=False, timeout=20)
                    encoding = requests.utils.get_encodings_from_content(req.text)[0]
                    r = req.content.decode(encoding, 'replace')
                except Exception as e:
                    print('第3次请求失败....')
                    try:
                        req = requests.get(urls, headers, verify=False, timeout=20)
                        encoding = requests.utils.get_encodings_from_content(req.text)[0]
                        r = req.content.decode(encoding, 'replace')
                    except Exception as e:
                        print('第4次请求失败....')
        if r == 0:
            self.result['备案编号'] = '暂无数据'
            self.result['备案性质'] = '暂无数据'
            self.result['备案名称'] = '暂无数据'
        else:
            self.result['备案编号'] = self.get_info_from_pattren(self.whois_id, r)
            self.result['备案性质'] = self.get_info_from_pattren(self.whois_type, r)
            self.result['备案名称'] = self.get_info_from_pattren(self.whois_name, r)

        return self.result

def initialdomains():
    Dicts = os.path.join('initialize', 'domains.list')
    tasks = list(set([x.strip() for x in open(Dicts,'r').readlines()]))
    for task in tasks:
        try:
            print('\n初始化子域名 : {}'.format(task))
            res = BeiAn(task).scan_seo()
            bid = str(res.get('备案编号'))
            bsex = str(res.get('备案性质'))
            bname = str(res.get('备案名称'))
            print(bid,bname,bsex)
            close_old_connections()
            BA = Domains()
            BA.url = task.lower()
            BA.BA_sex = bsex
            BA.BA_name = bname
            BA.BA_id = bid
            BA.save()
        except Exception as e:
            print(e)
            close_old_connections()
            print('\n初始化子域名 : {}'.format(task))
            res = BeiAn(task).scan_seo()
            bid = str(res.get('备案编号'))
            bsex = str(res.get('备案性质'))
            bname = str(res.get('备案名称'))
            print(bid,bname,bsex)
            close_old_connections()
            try:
                BA = Domains()
                BA.url = task.lower()
                BA.BA_sex = bsex
                BA.BA_name = bname
                BA.BA_id = bid
                BA.save()
            except:
                pass
def InsertUrls(filetxt):
    print('\n[加载] 开始获取泛解析对比数据 请耐心等待 获取目标总数为 : {}\n\n'.format(len(ALL_DOMAINS)))
    DomainsInfos(ALL_DOMAINS)
    print('[成功] 泛解析对比数据获取成功 请耐心等待数据持续收集整理\n\n')
    try:
        urls = set([x.strip()  if   x.startswith('http') else 'http://'+x.strip()  for x in open(filetxt,'r',encoding='utf-8').readlines() ])
        with ThreadPoolExecutor() as pool:
            pool.map(Add_Data_To_Url,urls)
    except Exception as e:
        print('读取导入域名文本失败:{}'.find(str(e)))

if __name__ == '__main__':
    res = BeiAn('qq.com').scan_seo()
    print(res)
