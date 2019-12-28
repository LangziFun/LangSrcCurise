# -*- encoding: utf-8 -*- 
"""
@author: LangziFun
@Blog: www.langzi.fun
@time: 2019/8/5 22:47
@file: 获取IP信息.py
"""
import IPy
import nmap
import socket
socket.setdefaulttimeout(25)
from urllib.parse import urlparse
import requests
requests.packages.urllib3.disable_warnings()
import time
from concurrent.futures import ProcessPoolExecutor,ThreadPoolExecutor
from qqwry import QQwry
from scapy.all import *
q = QQwry()
import os
q.load_file(os.path.join('Auxiliary','IP_ADDRESS.dat'))

import django
import os
import sys
pathname = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,pathname)
sys.path.insert(0,os.path.abspath(os.path.join(pathname,'..')))
os.environ.setdefault("DJANGO_SETTINGS_MODULE","LangSrcCurise.settings")
django.setup()
from app.models import Setting,Error_Log


Set = Setting.objects.all()[0]
pool_count = int(Set.Pool)
Alive_Status = eval(Set.Alive_Code)

# 判断存活验证码·机制，实际清空会写在配置文件中

#Banner = {b'http': [b'^HTTP/.*\nServer: Apache/2',b'HTTP'], b'ssh': [b'^SSH-.*openssh'], b'netbios': [b'\xc2\x83\x00\x00\x01\xc2\x8f'], b'backdoor-fxsvc': [b'^500 Not Loged in'], b'backdoor-shell': [b'^sh[$#]'], b'bachdoor-shell': [b'[a-z]*sh: .* command not found'], b'backdoor-cmdshell': [b'^Microsoft Windows .* Copyright .*>'], b'db2': [b'.*SQLDB2RA'], b'db2jds': [b'^N\x00'], b'dell-openmanage': [b'^N\x00\r'], b'finger': [b'finger: GET: '], b'ftp': [b'^220 .* UserGate'], b'http-iis': [b'^<h1>Bad Request .Invalid URL.</h1>'], b'http-jserv': [b'^HTTP/.*Cookie.*JServSessionId'], b'http-tomcat': [b'.*Servlet-Engine'], b'http-weblogic': [b'^HTTP/.*Cookie.*WebLogicSession'], b'http-vnc': [b'^HTTP/.*RealVNC/'], b'ldap': [b'^0E'], b'smb': [b'^\x00\x00\x00.\xc3\xbfSMBr\x00\x00\x00\x00.*'], b'msrdp': [b'^\x03\x00\x00\x0b\x06\xc3\x90\x00\x004\x12\x00'], b'msrdp-proxy': [b'^nmproxy: Procotol byte is not 8\n$'], b'msrpc': [b'\x05\x00\r\x03\x10\x00\x00\x00\x18\x00\x00\x00....\x04\x00\x01\x05\x00\x00\x00\x00$'], b'mssql': [b';MSSQLSERVER;'], b'telnet': [b'^\xc3\xbf\xc3\xbe'], b'mysql': [b"whost '"], b'mysql-blocked': [b'^\\(\x00\x00'], b'mysql-secured': [b'this MySQL'], b'mongodb': [b'^.*version.....([\\.\\d]+)'], b'nagiosd': [b'Sorry, you \\(.*are not among the allowed hosts...'], b'nessus': [b'< NTP 1.2 >\nUser:'], b'oracle-tns-listener': [b'\\(ADDRESS=\\(PROTOCOL='], b'oracle-dbsnmp': [b'^\x00\x0c\x00\x00\x04\x00\x00\x00\x00'], b'oracle-https': [b'^220- ora'], b'oracle-rmi': [b'^N\x00\t'], b'postgres': [b'^EFATAL'], b'rlogin': [b'^\x01Permission denied.\n'], b'rpc-nfs': [b'^\x02\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x00'], b'rpc': [b'^\xc2\x80\x00\x00'], b'rsync': [b'^@RSYNCD:.*'], b'smux': [b'^A\x01\x02\x00'], b'snmp-public': [b'public\xc2\xa2'], b'snmp': [b'A\x01\x02'], b'socks': [b'^\x05[\x00-\x08]\x00'], b'ssl': [b'^\x16\x03\x00..\x02...\x03\x00'], b'sybase': [b'^\x04\x01\x00'], b'tftp': [b'^\x00[\x03\x05]\x00'], b'uucp': [b'^login: password: '], b'vnc': [b'^RFB.*'], b'webmin': [b'^0\\.0\\.0\\.0:.*:[0-9]'], b'websphere-javaw': [b'^\x15\x00\x00\x00\x02\x02\n']}


# 2019-12-27 更新，新增BANNER识别服务指纹
Banner = {b'http': [b'^HTTP/.*\nServer: Apache/2', b'HTTP', b'http/1.1', b'http/1.0'], b'ssh': [b'^SSH-.*openssh', b'^ssh-', b'connection refused by remote host.'], b'netbios': [b'\xc2\x83\x00\x00\x01\xc2\x8f', b'^y\x08.*browse', b'^y\x08.\x00\x00\x00\x00', b'^\x05\x00\r\x03', b'^\x82\x00\x00\x00', b'\x83\x00\x00\x01\x8f'], b'backdoor-fxsvc': [b'^500 Not Loged in'], b'backdoor-shell': [b'^sh[$#]'], b'bachdoor-shell': [b'[a-z]*sh: .* command not found'], b'backdoor-cmdshell': [b'^Microsoft Windows .* Copyright .*>'], b'db2': [b'.*SQLDB2RA', b'.*sqldb2ra'], b'db2jds': [b'^N\x00', b'^n\x00'], b'dell-openmanage': [b'^N\x00\r'], b'finger': [b'finger: GET: ', b'^\r\n\tline\t  user', b'line\t user', b'login name: ', b'login.*name.*tty.*idle', b'^no one logged on', b'^\r\nwelcome', b'^finger:', b'^must provide username', b'finger: get: '], b'ftp': [b'^220 .* UserGate', b'^220.*\n331', b'^220.*\n530', b'^220.*ftp', b'^220 .* microsoft .* ftp', b'^220 inactivity timer', b'^220 .* usergate', b'^220.*filezilla server', b'^220-', b'^220.*?ftp', b'^220.*?filezilla'], b'http-iis': [b'^<h1>Bad Request .Invalid URL.</h1>'], b'http-jserv': [b'^HTTP/.*Cookie.*JServSessionId'], b'http-tomcat': [b'.*Servlet-Engine'], b'http-weblogic': [b'^HTTP/.*Cookie.*WebLogicSession'], b'http-vnc': [b'^HTTP/.*RealVNC/'], b'ldap': [b'^0E', b'^0\x0c\x02\x01\x01a', b'^02\x02\x01', b'^03\x02\x01', b'^08\x02\x01', b'^0\x84', b'^0e'], b'smb': [b'^\x00\x00\x00.\xc3\xbfSMBr\x00\x00\x00\x00.*', b'^\x00\x00\x00.\xffsmbr\x00\x00\x00\x00.*', b'^\x83\x00\x00\x01\x8f'], b'msrdp': [b'^\x03\x00\x00\x0b\x06\xc3\x90\x00\x004\x12\x00'], b'msrdp-proxy': [b'^nmproxy: Procotol byte is not 8\n$'], b'msrpc': [b'\x05\x00\r\x03\x10\x00\x00\x00\x18\x00\x00\x00....\x04\x00\x01\x05\x00\x00\x00\x00$', b'^\x05\x00\r\x03\x10\x00\x00\x00\x18\x00\x00\x00\x00\x00', b'\x05\x00\r\x03\x10\x00\x00\x00\x18\x00\x00\x00....\x04\x00\x01\x05\x00\x00\x00\x00$'], b'mssql': [b';MSSQLSERVER;', b'^\x05n\x00', b'^\x04\x01', b';mssqlserver;', b'mssqlserver'], b'telnet': [b'^\xc3\xbf\xc3\xbe', b'telnet', b'^\xff[\xfa-\xff]', b'^\r\n%connection closed by remote host!\x00$'], b'mysql': [b"whost '", b'mysql_native_password', b'^\x19\x00\x00\x00\n', b'^,\x00\x00\x00\n', b"hhost '", b"khost '", b'mysqladmin', b"whost '", b'^[.*]\x00\x00\x00\n.*?\x00', b'this mysql server', b'mariadb server', b'\x00\x00\x00\xffj\x04host'], b'mysql-blocked': [b'^\\(\x00\x00'], b'mysql-secured': [b'this MySQL'], b'mongodb': [b'^.*version.....([\\.\\d]+)', b'mongodb'], b'nagiosd': [b'Sorry, you \\(.*are not among the allowed hosts...', b'sorry, you \\(.*are not among the allowed hosts...'], b'nessus': [b'< NTP 1.2 >\nUser:', b'< ntp 1.2 >\nuser:'], b'oracle-tns-listener': [b'\\(ADDRESS=\\(PROTOCOL=', b'\\(error_stack=\\(error=\\(code=', b'\\(address=\\(protocol='], b'oracle-dbsnmp': [b'^\x00\x0c\x00\x00\x04\x00\x00\x00\x00', b'^\x00\x0c\x00\x00\x04\x00\x00\x00\x00'], b'oracle-https': [b'^220- ora', b'^220- ora'], b'oracle-rmi': [b'^N\x00\t'], b'postgres': [b'^EFATAL'], b'rlogin': [b'^\x01Permission denied.\n', b'login: ', b'rlogind: ', b'^\x01permission denied.\n'], b'rpc-nfs': [b'^\x02\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x00', b'^\x02\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x00'], b'rpc': [b'^\xc2\x80\x00\x00', b'\x01\x86\xa0', b'\x03\x9beb\x00\x00\x00\x01', b'^\x80\x00\x00'], b'rsync': [b'^@RSYNCD:.*', b'^@rsyncd:', b'@rsyncd:'], b'smux': [b'^A\x01\x02\x00', b'^a\x01\x02\x00'], b'snmp-public': [b'public\xc2\xa2', b'public\xa2'], b'snmp': [b'A\x01\x02', b'a\x01\x02'], b'socks': [b'^\x05[\x00-\x08]\x00', b'^\x05[\x00-\x08]\x00'], b'ssl': [b'^\x16\x03\x00..\x02...\x03\x00', b'^..\x04\x00.\x00\x02', b'^\x16\x03\x01..\x02...\x03\x01', b'^\x16\x03\x00..\x02...\x03\x00', b'ssl.*get_client_hello', b'^-err .*tls_start_servertls', b'^\x16\x03\x00\x00j\x02\x00\x00f\x03\x00', b'^\x16\x03\x00..\x02\x00\x00f\x03\x00', b'^\x15\x03\x00\x00\x02\x02\\.*', b'^\x16\x03\x01..\x02...\x03\x01', b'^\x16\x03\x00..\x02...\x03\x00'], b'sybase': [b'^\x04\x01\x00', b'^\x04\x01\x00'], b'tftp': [b'^\x00[\x03\x05]\x00', b'^\x00[\x03\x05]\x00'], b'uucp': [b'^login: password: ', b'^login: password: '], b'vnc': [b'^RFB.*', b'^rfb'], b'webmin': [b'^0\\.0\\.0\\.0:.*:[0-9]', b'.*miniserv', b'^0\\.0\\.0\\.0:.*:[0-9]'], b'websphere-javaw': [b'^\x15\x00\x00\x00\x02\x02\n', b'^\x15\x00\x00\x00\x02\x02\n'], b'xmpp': [b"^\\<\\?xml version='1.0'\\?\\>"], b'backdoor': [b'^500 not loged in', b'get: command', b'sh: get:', b'^bash[$#]', b'^sh[$#]', b'^microsoft windows'], b'bachdoor': [b'*sh: .* command not found'], b'rdp': [b'^\x00\x01\x00.*?\r\n\r\n$', b'^\x03\x00\x00\x0b', b'^\x03\x00\x00\x11', b'^\x03\x00\x00\x0b\x06\xd0\x00\x00\x12.\x00$', b'^\x03\x00\x00\x17\x08\x02\x00\x00z~\x00\x0b\x05\x05@\x06\x00\x08\x91j\x00\x02x$', b'^\x03\x00\x00\x11\x08\x02..}\x08\x03\x00\x00\xdf\x14\x01\x01$', b'^\x03\x00\x00\x0b\x06\xd0\x00\x00\x03.\x00$', b'^\x03\x00\x00\x0b\x06\xd0\x00\x00\x00\x00\x00', b'^\x03\x00\x00\x0e\t\xd0\x00\x00\x00[\x02\xa1]\x00\xc0\x01\n$', b'^\x03\x00\x00\x0b\x06\xd0\x00\x004\x12\x00'], b'rdp-proxy': [b'^nmproxy: procotol byte is not 8\n$'], b'rmi': [b'\x00\x00\x00vinva', b'^n\x00\t'], b'postgresql': [b'invalid packet length', b'^efatal'], b'imap': [b'^\\* ok.*?imap'], b'pop': [b'^\\+ok.*?'], b'smtp': [b'^220.*?smtp', b'^554 smtp'], b'rtsp': [b'^rtsp/'], b'sip': [b'^sip/'], b'nntp': [b'^200 nntp'], b'sccp': [b'^\x01\x00\x00\x00$'], b'squid': [b'x-squid-error'], b'vmware': [b'vmware'], b'iscsi': [b'\x00\x02\x0b\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'], b'redis': [b'^-err unknown command', b'^-err wrong number of arguments', b'^-denied redis is running'], b'memcache': [b'^error\r\n'], b'websocket': [b'server: websocket'], b'https': [b'instead use the https scheme to accesshttps', b'http request to an https server', b'location: https'], b'svn': [b'^\\( success \\( 2 2 \\( \\) \\( edit-pipeline svndiff1'], b'dubbo': [b'^unsupported command'], b'elasticsearch': [b'cluster_name.*elasticsearch'], b'rabbitmq': [b'^amqp\x00\x00\t\x01'], b'zookeeper': [b'^zookeeper version: ']}

from tinydb import TinyDB, where
from tinydb.storages import JSONStorage
from tinydb.middlewares import CachingMiddleware
from collections import namedtuple
import os
Port = namedtuple("Port", ["name", "port", "protocol", "description"])

__BASE_PATH__ = os.path.dirname(os.path.abspath(__file__))
__DATABASE_PATH__ = os.path.join( 'Auxiliary','ports.json')
__DB__ = TinyDB(__DATABASE_PATH__, storage=CachingMiddleware(JSONStorage))

# pathname = os.path.dirname(os.path.abspath(__file__))
# sys.path.insert(0,pathname)
# sys.path.insert(0,os.path.abspath(os.path.join(pathname,'..')))


def GetPortInfo(port, like=False):
    """
    判断端口服务，传入参数为 字符串类型的数字
    返回服务名称  'http'，没有则返回  '检测失效'

    """
    where_field = "port" if port.isdigit() else "name"
    if like:
        ports = __DB__.search(where(where_field).search(port))
    else:
        ports = __DB__.search(where(where_field) == port)
    try:
        return ports[0]['name']  # flake8: noqa (F812)
    except:
        return '识别端口失败'



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

def Requests(url):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
    url1 = 'http://'+url
    url2 = 'https://'+url
    title = '获取失败'
    title1 = '获取失败'
    title2 = '获取失败'
    content1 = None
    content2 = None
    try:
        r = requests.get(url='http://'+url,headers=headers,verify=False,timeout=20)
        if b'text/html' in r.content or b'<title>' in r.content or b'</html>' in r.content:
            content1 = r.content
        if r.status_code in Alive_Status:
            u = urlparse(str(r.url))
            title1 = get_title(r.content)
            url1 = u.scheme + '://' + u.netloc
    except Exception as e:
        pass
    try:
        r = requests.get(url='https://'+url,headers=headers,verify=False,timeout=20)
        if b'text/html' in r.content or b'<title>' in r.content or b'</html>' in r.content:
            content2 = r.content
        if r.status_code in Alive_Status:
            u = urlparse(str(r.url))
            title2 = get_title(r.content)
            url2 = u.scheme + '://' + u.netloc
    except Exception as e:
        pass
    if title1 != '获取失败':
        return {url1: title1}
    if title2 != '获取失败':
        return {url2: title2}
    if content1 != None:
        return {url1:title}
    if content2 != None:
        return {url2:title}


def Get_Alive_Url(urls):
    '''
    如果想要获取 IP 段内存活web服务
        hosts = IPy.IP('118.24.1.0/24')
        urls = []
        for host in hosts:
            urls.append('http://{}:{}'.format(host,80))
            urls.append('https://{}:{}'.format(host,443))
        Get_Alive_Url(urls)
        返回结果是一个列表，列表内数据为字典 多个自带你 {网址：标题}
    '''
    with ThreadPoolExecutor(max_workers=pool_count) as p:
        future_tasks = [p.submit(Requests, i) for i in urls]
    result = [obj.result() for obj in future_tasks if obj.result() is not None]
    # print(result)
    return result

class Get_Ip_Info:
    '''
    要获取开放端口的服务
        r = Get_Ip_Info('118.24.11.235')
        print(r.get_server_from_banner('118.24.11.235',80))
        返回 mssql，没识别出则返回 ‘识别失败’
        用的非常少，因为这个本身就是在nmap识别不出来情况下使用

    要获取网段存活主机
            r = Get_Ip_Info('192.168.1.55')
            print(r.get_alive_host())
            返回列表，没有则是空列表

    要获取IP上面的端口与服务(nmap扫描存在误报)
            r = Get_Ip_Info('118.24.11.235')
            print(r.get_server_from_nmap('118.24.11.235'))
            返回字典，对应
            {80:'http'...}

    要获取 IP 归属地
        a = Get_Ip_Info('118.24.11.235')
        print(a.get_ip_address('118.24.11.235'))
        不存在返回None，存在返回
        ('四川省成都市', '腾讯云')

    要获取一个IP的主机类型
        a = Get_Ip_Info('118.24.11.235')
        print(a.get_host_type('118.24.11.235'))
        识别失败返回’识别失败‘，否则返回主机类型 Windows

    检查ip是否存活
        a = Get_Ip_Info('118.24.11.235')
        print(a.check_ip_alive('118.24.11.235'))
        存活返回true 否则返回false

    获取传入ip的C段名 以及C段ip
            a = Get_Ip_Info('118.24.11.235')
            print(a.cs_ips('118.24.11.235'))
            返回
            {'118.24.11.0/24',[118.24.11.1,118.24.11.2..........]}

    获取传入ip的C段名
                a = Get_Ip_Info('118.24.11.235')
                print(a.cs_name('118.24.11.235'))

    获取一个传入列表返回存货主机

    get_alive_hosts([xxx.xxx.xx.x,xx.x.xx])
    '''

    def __init__(self,ip):
        self.ip = ip

    def get_host_type(self,ip):
        try:
            r = sr1(IP(dst=ip) / ICMP(), timeout=20, verbose=0)
            if r == None:
                return ('获取失败')
            if r[IP].ttl <= 64:
                return ("Linux/Unix")
            if r[IP].ttl > 64 and r[IP].ttl <= 128:
                return ("Windows")
            else:
                return ("Unix")
        except:
            return '获取失败'
    def get_server_from_banner(self,ip,port):
        try:
            s = socket.socket()
            s.connect((ip,port))
            s.send(b'')
            res = s.recv(1024)
            s.close()
            for k,v in Banner.items():
                for b in v:
                    banner = re.search(b,res)
                    if banner:
                        return k.decode()
            return '获取失败'
        except Exception as e:
            # print(e)
            return '获取失败'
    def get_alive_host(self):
        ip = '.'.join(self.ip.split('.')[0:-1])+'.0/24'
        # hosts = list(IPy.IP(ip))
        # print(hosts)
        nma = nmap.PortScanner()
        result = nma.scan(hosts=ip, arguments='-n -sP -PE')
        alive_host = []
        try:
            alive_host = list(result['scan'].keys())
        except:
            pass
        return alive_host

    def get_cs_name(self,ip):
        return '.'.join(str(ip).split('.')[0:-1])+'.0/24'




    def get_cs_ips(self,ip):
        res = {}
        cs_name = '.'.join(str(ip).split('.')[0:-1])+'.0/24'
        cs_ip = list(IPy.IP(cs_name))
        res[cs_name] = cs_ip
        return res

    def check_ip_alive(self,ip):
        # 存活返回true 否则返回false
        alive = None
        try:
            nm = nmap.PortScanner()
            res = nm.scan(hosts=ip, arguments='-sn -PE -n')
            stat = int(res['nmap']['scanstats']['uphosts'])
            if stat == 1:
                alive = ip
        except Exception as e:
            pass
        return alive

    def get_alive_hosts(self,hosts):
        result = set()
        with ProcessPoolExecutor(max_workers=pool_count) as p:
            future_tasks = [p.submit(self.check_ip_alive, i) for i in hosts]
        result = [obj.result() for obj in future_tasks if obj.result()]

        return list(result)

    def get_server_from_nmap(self,ip):
        result = {}
        try:
            nm = nmap.PortScanner()
            res = nm.scan(ip,arguments='-Pn -sS -p 1-65535')
            try:
                r = res['scan'][ip]['tcp']
                if r:
                    for k, v in r.items():
                        result[k]=v.get('name')
                    for k,v in result.items():
                        if v == None or v=='unknown' or v == '':
                            result[k] = self.get_server_from_banner(ip,int(k))
            except:
                time.sleep(10)
                # 重试一次
                res = nm.scan(ip, arguments='-Pn -sS -p 1-65535')
                r = res['scan'][ip]['tcp']
                try:
                    if r:
                        for k, v in r.items():
                            result[k]=v.get('name')
                        for k,v in result.items():
                            if v == None or v=='unknown' or v == '':
                                result[k] = self.get_server_from_banner(ip,int(k))
                except Exception as e:
                    print('错误代码 [13] {} 扫描当前IP失败'.format(str(e)))
                    Error_Log.objects.create(url=ip + '|扫描当前IP失败', error='错误代码 [13] {} '.format(str(e)))
        except Exception as e :
            print('错误代码 [14] {} 扫描当前IP失败'.format(str(e)))
            Error_Log.objects.create(url=ip + '|扫描当前IP失败', error='错误代码 [14] {} '.format(str(e)))
        if result != {}:
            for k,v in result.items():
                if v == None or v == 'unknown' or v == '' or v == '获取失败':
                    result[k] = str(GetPortInfo(str(v)))
        return result

    def get_ip_address(self,ip):
        res = '获取失败'
        try:
            res = q.lookup(ip)
        except:
            pass
        return res



if __name__ == '__main__':
    ip = '118.24.11.235'
    # 端口
    IP_Res = Get_Ip_Info(ip)
    servers = IP_Res.get_server_from_nmap(ip)
    # 服务与端口  字典类型
    open_port = servers.keys()
    check_alive_url = []
    for port in open_port:
        check_alive_url.append('http://{}:{}'.format(ip,port))
        check_alive_url.append('https://{}:{}'.format(ip,port))
    alive_url = Get_Alive_Url(check_alive_url)
    # 该IP上存活WEB，类型为列表，内容为多个字典
    host_type = IP_Res.get_host_type(ip)
    # windows/linux
    area = IP_Res.get_ip_address(ip)
    # 返回地址

