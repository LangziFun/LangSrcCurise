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
#anner = {b'http': [b'^HTTP/.*\nServer: Apache/2', b'HTTP', b'http/1.1', b'http/1.0'], b'ssh': [b'^SSH-.*openssh', b'^ssh-', b'connection refused by remote host.'], b'netbios': [b'\xc2\x83\x00\x00\x01\xc2\x8f', b'^y\x08.*browse', b'^y\x08.\x00\x00\x00\x00', b'^\x05\x00\r\x03', b'^\x82\x00\x00\x00', b'\x83\x00\x00\x01\x8f'], b'backdoor-fxsvc': [b'^500 Not Loged in'], b'backdoor-shell': [b'^sh[$#]'], b'bachdoor-shell': [b'[a-z]*sh: .* command not found'], b'backdoor-cmdshell': [b'^Microsoft Windows .* Copyright .*>'], b'db2': [b'.*SQLDB2RA', b'.*sqldb2ra'], b'db2jds': [b'^N\x00', b'^n\x00'], b'dell-openmanage': [b'^N\x00\r'], b'finger': [b'finger: GET: ', b'^\r\n\tline\t  user', b'line\t user', b'login name: ', b'login.*name.*tty.*idle', b'^no one logged on', b'^\r\nwelcome', b'^finger:', b'^must provide username', b'finger: get: '], b'ftp': [b'^220 .* UserGate', b'^220.*\n331', b'^220.*\n530', b'^220.*ftp', b'^220 .* microsoft .* ftp', b'^220 inactivity timer', b'^220 .* usergate', b'^220.*filezilla server', b'^220-', b'^220.*?ftp', b'^220.*?filezilla'], b'http-iis': [b'^<h1>Bad Request .Invalid URL.</h1>'], b'http-jserv': [b'^HTTP/.*Cookie.*JServSessionId'], b'http-tomcat': [b'.*Servlet-Engine'], b'http-weblogic': [b'^HTTP/.*Cookie.*WebLogicSession'], b'http-vnc': [b'^HTTP/.*RealVNC/'], b'ldap': [b'^0E', b'^0\x0c\x02\x01\x01a', b'^02\x02\x01', b'^03\x02\x01', b'^08\x02\x01', b'^0\x84', b'^0e'], b'smb': [b'^\x00\x00\x00.\xc3\xbfSMBr\x00\x00\x00\x00.*', b'^\x00\x00\x00.\xffsmbr\x00\x00\x00\x00.*', b'^\x83\x00\x00\x01\x8f'], b'msrdp': [b'^\x03\x00\x00\x0b\x06\xc3\x90\x00\x004\x12\x00'], b'msrdp-proxy': [b'^nmproxy: Procotol byte is not 8\n$'], b'msrpc': [b'\x05\x00\r\x03\x10\x00\x00\x00\x18\x00\x00\x00....\x04\x00\x01\x05\x00\x00\x00\x00$', b'^\x05\x00\r\x03\x10\x00\x00\x00\x18\x00\x00\x00\x00\x00', b'\x05\x00\r\x03\x10\x00\x00\x00\x18\x00\x00\x00....\x04\x00\x01\x05\x00\x00\x00\x00$'], b'mssql': [b';MSSQLSERVER;', b'^\x05n\x00', b'^\x04\x01', b';mssqlserver;', b'mssqlserver'], b'telnet': [b'^\xc3\xbf\xc3\xbe', b'telnet', b'^\xff[\xfa-\xff]', b'^\r\n%connection closed by remote host!\x00$'], b'mysql': [b"whost '", b'mysql_native_password', b'^\x19\x00\x00\x00\n', b'^,\x00\x00\x00\n', b"hhost '", b"khost '", b'mysqladmin', b"whost '", b'^[.*]\x00\x00\x00\n.*?\x00', b'this mysql server', b'mariadb server', b'\x00\x00\x00\xffj\x04host'], b'mysql-blocked': [b'^\\(\x00\x00'], b'mysql-secured': [b'this MySQL'], b'mongodb': [b'^.*version.....([\\.\\d]+)', b'mongodb'], b'nagiosd': [b'Sorry, you \\(.*are not among the allowed hosts...', b'sorry, you \\(.*are not among the allowed hosts...'], b'nessus': [b'< NTP 1.2 >\nUser:', b'< ntp 1.2 >\nuser:'], b'oracle-tns-listener': [b'\\(ADDRESS=\\(PROTOCOL=', b'\\(error_stack=\\(error=\\(code=', b'\\(address=\\(protocol='], b'oracle-dbsnmp': [b'^\x00\x0c\x00\x00\x04\x00\x00\x00\x00', b'^\x00\x0c\x00\x00\x04\x00\x00\x00\x00'], b'oracle-https': [b'^220- ora', b'^220- ora'], b'oracle-rmi': [b'^N\x00\t'], b'postgres': [b'^EFATAL'], b'rlogin': [b'^\x01Permission denied.\n', b'login: ', b'rlogind: ', b'^\x01permission denied.\n'], b'rpc-nfs': [b'^\x02\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x00', b'^\x02\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x00'], b'rpc': [b'^\xc2\x80\x00\x00', b'\x01\x86\xa0', b'\x03\x9beb\x00\x00\x00\x01', b'^\x80\x00\x00'], b'rsync': [b'^@RSYNCD:.*', b'^@rsyncd:', b'@rsyncd:'], b'smux': [b'^A\x01\x02\x00', b'^a\x01\x02\x00'], b'snmp-public': [b'public\xc2\xa2', b'public\xa2'], b'snmp': [b'A\x01\x02', b'a\x01\x02'], b'socks': [b'^\x05[\x00-\x08]\x00', b'^\x05[\x00-\x08]\x00'], b'ssl': [b'^\x16\x03\x00..\x02...\x03\x00', b'^..\x04\x00.\x00\x02', b'^\x16\x03\x01..\x02...\x03\x01', b'^\x16\x03\x00..\x02...\x03\x00', b'ssl.*get_client_hello', b'^-err .*tls_start_servertls', b'^\x16\x03\x00\x00j\x02\x00\x00f\x03\x00', b'^\x16\x03\x00..\x02\x00\x00f\x03\x00', b'^\x15\x03\x00\x00\x02\x02\\.*', b'^\x16\x03\x01..\x02...\x03\x01', b'^\x16\x03\x00..\x02...\x03\x00'], b'sybase': [b'^\x04\x01\x00', b'^\x04\x01\x00'], b'tftp': [b'^\x00[\x03\x05]\x00', b'^\x00[\x03\x05]\x00'], b'uucp': [b'^login: password: ', b'^login: password: '], b'vnc': [b'^RFB.*', b'^rfb'], b'webmin': [b'^0\\.0\\.0\\.0:.*:[0-9]', b'.*miniserv', b'^0\\.0\\.0\\.0:.*:[0-9]'], b'websphere-javaw': [b'^\x15\x00\x00\x00\x02\x02\n', b'^\x15\x00\x00\x00\x02\x02\n'], b'xmpp': [b"^\\<\\?xml version='1.0'\\?\\>"], b'backdoor': [b'^500 not loged in', b'get: command', b'sh: get:', b'^bash[$#]', b'^sh[$#]', b'^microsoft windows'], b'bachdoor': [b'*sh: .* command not found'], b'rdp': [b'^\x00\x01\x00.*?\r\n\r\n$', b'^\x03\x00\x00\x0b', b'^\x03\x00\x00\x11', b'^\x03\x00\x00\x0b\x06\xd0\x00\x00\x12.\x00$', b'^\x03\x00\x00\x17\x08\x02\x00\x00z~\x00\x0b\x05\x05@\x06\x00\x08\x91j\x00\x02x$', b'^\x03\x00\x00\x11\x08\x02..}\x08\x03\x00\x00\xdf\x14\x01\x01$', b'^\x03\x00\x00\x0b\x06\xd0\x00\x00\x03.\x00$', b'^\x03\x00\x00\x0b\x06\xd0\x00\x00\x00\x00\x00', b'^\x03\x00\x00\x0e\t\xd0\x00\x00\x00[\x02\xa1]\x00\xc0\x01\n$', b'^\x03\x00\x00\x0b\x06\xd0\x00\x004\x12\x00'], b'rdp-proxy': [b'^nmproxy: procotol byte is not 8\n$'], b'rmi': [b'\x00\x00\x00vinva', b'^n\x00\t'], b'postgresql': [b'invalid packet length', b'^efatal'], b'imap': [b'^\\* ok.*?imap'], b'pop': [b'^\\+ok.*?'], b'smtp': [b'^220.*?smtp', b'^554 smtp'], b'rtsp': [b'^rtsp/'], b'sip': [b'^sip/'], b'nntp': [b'^200 nntp'], b'sccp': [b'^\x01\x00\x00\x00$'], b'squid': [b'x-squid-error'], b'vmware': [b'vmware'], b'iscsi': [b'\x00\x02\x0b\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'], b'redis': [b'^-err unknown command', b'^-err wrong number of arguments', b'^-denied redis is running'], b'memcache': [b'^error\r\n'], b'websocket': [b'server: websocket'], b'https': [b'instead use the https scheme to accesshttps', b'http request to an https server', b'location: https'], b'svn': [b'^\\( success \\( 2 2 \\( \\) \\( edit-pipeline svndiff1'], b'dubbo': [b'^unsupported command'], b'elasticsearch': [b'cluster_name.*elasticsearch'], b'rabbitmq': [b'^amqp\x00\x00\t\x01'], b'zookeeper': [b'^zookeeper version: ']}

# 2020-01-29 更新
Banner = {
    b'http': [b'^HTTP/.*\nServer: Apach', b'^HTTP/.*\nServer: nginx', b'HTTP.*?text/html', b'http.*?</html>'],
    b'ssh': [b'^SSH-.*openssh', b'^ssh-', b'connection refused by remote host.'],
    b'netbios': [b'\xc2\x83\x00\x00\x01\xc2\x8f', b'^y\x08.*browse', b'^y\x08.\x00\x00\x00\x00', b'^\x05\x00\r\x03',
                 b'^\x82\x00\x00\x00', b'\x83\x00\x00\x01\x8f'], b'backdoor-fxsvc': [b'^500 Not Loged in'],
    b'backdoor-shell': [b'^sh[$#]'], b'bachdoor-shell': [b'[a-z]*sh: .* command not found'],
    b'backdoor-cmdshell': [b'^Microsoft Windows .* Copyright .*>'], b'db2': [b'.*SQLDB2RA', b'.*sqldb2ra'],
    b'db2jds': [b'^N\x00', b'^n\x00'], b'dell-openmanage': [b'^N\x00\r'],
    b'finger': [b'finger: GET: ', b'^\r\n\tline\t  user', b'line\t user', b'login name: ', b'login.*name.*tty.*idle',
                b'^no one logged on', b'^\r\nwelcome', b'^finger:', b'^must provide username', b'finger: get: '],
    b'ftp': [b'^220 .* UserGate', b'^220.*\n331', b'^220.*\n530', b'^220.*ftp', b'^220 .* microsoft .* ftp',
             b'^220 inactivity timer', b'^220 .* usergate', b'^220.*filezilla server', b'^220-', b'^220.*?ftp',
             b'^220.*?filezilla'], b'http-iis': [b'^<h1>Bad Request .Invalid URL.</h1>'],
    b'http-jserv': [b'^HTTP/.*Cookie.*JServSessionId'], b'http-tomcat': [b'.*Servlet-Engine'],
    b'http-weblogic': [b'^HTTP/.*Cookie.*WebLogicSession'], b'http-vnc': [b'^HTTP/.*RealVNC/'],
    b'ldap': [b'^0E', b'^0\x0c\x02\x01\x01a', b'^02\x02\x01', b'^03\x02\x01', b'^08\x02\x01', b'^0\x84', b'^0e'],
    b'smb': [b'^\x00\x00\x00.\xc3\xbfSMBr\x00\x00\x00\x00.*', b'^\x00\x00\x00.\xffsmbr\x00\x00\x00\x00.*',
             b'^\x83\x00\x00\x01\x8f'], b'msrdp': [b'^\x03\x00\x00\x0b\x06\xc3\x90\x00\x004\x12\x00'],
    b'msrdp-proxy': [b'^nmproxy: Procotol byte is not 8\n$'],
    b'msrpc': [b'\x05\x00\r\x03\x10\x00\x00\x00\x18\x00\x00\x00....\x04\x00\x01\x05\x00\x00\x00\x00$',
               b'^\x05\x00\r\x03\x10\x00\x00\x00\x18\x00\x00\x00\x00\x00',
               b'\x05\x00\r\x03\x10\x00\x00\x00\x18\x00\x00\x00....\x04\x00\x01\x05\x00\x00\x00\x00$'],
    b'mssql': [b';MSSQLSERVER;', b'^\x05n\x00', b'^\x04\x01', b';mssqlserver;', b'mssqlserver'],
    b'telnet': [b'^\xc3\xbf\xc3\xbe', b'telnet', b'^\xff[\xfa-\xff]', b'^\r\n%connection closed by remote host!\x00$'],
    b'mysql': [b"whost '", b'mysql_native_password', b'^\x19\x00\x00\x00\n', b'^,\x00\x00\x00\n', b"hhost '",
               b"khost '", b'mysqladmin', b"whost '", b'^[.*]\x00\x00\x00\n.*?\x00', b'this mysql server',
               b'mariadb server', b'\x00\x00\x00\xffj\x04host'], b'mysql-blocked': [b'^\\(\x00\x00'],
    b'mysql-secured': [b'this MySQL'], b'mongodb': [b'^.*version.....([\\.\\d]+)', b'mongodb'],
    b'nagiosd': [b'Sorry, you \\(.*are not among the allowed hosts...',
                 b'sorry, you \\(.*are not among the allowed hosts...'],
    b'nessus': [b'< NTP 1.2 >\nUser:', b'< ntp 1.2 >\nuser:'],
    b'oracle-tns-listener': [b'\\(ADDRESS=\\(PROTOCOL=', b'\\(error_stack=\\(error=\\(code=',
                             b'\\(address=\\(protocol='],
    b'oracle-dbsnmp': [b'^\x00\x0c\x00\x00\x04\x00\x00\x00\x00', b'^\x00\x0c\x00\x00\x04\x00\x00\x00\x00'],
    b'oracle-https': [b'^220- ora', b'^220- ora'], b'oracle-rmi': [b'^N\x00\t'], b'postgres': [b'^EFATAL'],
    b'rlogin': [b'^\x01Permission denied.\n', b'login: ', b'rlogind: ', b'^\x01permission denied.\n'],
    b'rpc-nfs': [b'^\x02\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x00',
                 b'^\x02\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x00'],
    b'rpc': [b'^\xc2\x80\x00\x00', b'\x01\x86\xa0', b'\x03\x9beb\x00\x00\x00\x01', b'^\x80\x00\x00'],
    b'rsync': [b'^@RSYNCD:.*', b'^@rsyncd:', b'@rsyncd:'], b'smux': [b'^A\x01\x02\x00', b'^a\x01\x02\x00'],
    b'snmp-public': [b'public\xc2\xa2', b'public\xa2'], b'snmp': [b'A\x01\x02', b'a\x01\x02'],
    b'socks': [b'^\x05[\x00-\x08]\x00', b'^\x05[\x00-\x08]\x00'],
    b'ssl': [b'^\x16\x03\x00..\x02...\x03\x00', b'^..\x04\x00.\x00\x02', b'^\x16\x03\x01..\x02...\x03\x01',
             b'^\x16\x03\x00..\x02...\x03\x00', b'ssl.*get_client_hello', b'^-err .*tls_start_servertls',
             b'^\x16\x03\x00\x00j\x02\x00\x00f\x03\x00', b'^\x16\x03\x00..\x02\x00\x00f\x03\x00',
             b'^\x15\x03\x00\x00\x02\x02\\.*', b'^\x16\x03\x01..\x02...\x03\x01', b'^\x16\x03\x00..\x02...\x03\x00'],
    b'sybase': [b'^\x04\x01\x00', b'^\x04\x01\x00'], b'tftp': [b'^\x00[\x03\x05]\x00', b'^\x00[\x03\x05]\x00'],
    b'uucp': [b'^login: password: ', b'^login: password: '], b'vnc': [b'^RFB.*', b'^rfb'],
    b'webmin': [b'^0\\.0\\.0\\.0:.*:[0-9]', b'.*miniserv', b'^0\\.0\\.0\\.0:.*:[0-9]'],
    b'websphere-javaw': [b'^\x15\x00\x00\x00\x02\x02\n', b'^\x15\x00\x00\x00\x02\x02\n'],
    b'xmpp': [b"^\\<\\?xml version='1.0'\\?\\>"],
    b'backdoor': [b'^500 not loged in', b'get: command', b'sh: get:', b'^bash[$#]', b'^sh[$#]', b'^microsoft windows'],
    b'bachdoor': [b'*sh: .* command not found'],
    b'rdp': [b'^\x00\x01\x00.*?\r\n\r\n$', b'^\x03\x00\x00\x0b', b'^\x03\x00\x00\x11',
             b'^\x03\x00\x00\x0b\x06\xd0\x00\x00\x12.\x00$',
             b'^\x03\x00\x00\x17\x08\x02\x00\x00z~\x00\x0b\x05\x05@\x06\x00\x08\x91j\x00\x02x$',
             b'^\x03\x00\x00\x11\x08\x02..}\x08\x03\x00\x00\xdf\x14\x01\x01$',
             b'^\x03\x00\x00\x0b\x06\xd0\x00\x00\x03.\x00$', b'^\x03\x00\x00\x0b\x06\xd0\x00\x00\x00\x00\x00',
             b'^\x03\x00\x00\x0e\t\xd0\x00\x00\x00[\x02\xa1]\x00\xc0\x01\n$',
             b'^\x03\x00\x00\x0b\x06\xd0\x00\x004\x12\x00'], b'rdp-proxy': [b'^nmproxy: procotol byte is not 8\n$'],
    b'rmi': [b'\x00\x00\x00vinva', b'^n\x00\t'], b'postgresql': [b'invalid packet length', b'^efatal'],
    b'imap': [b'^\\* ok.*?imap'], b'pop': [b'^\\+ok.*?'], b'smtp': [b'^220.*?smtp', b'^554 smtp'], b'rtsp': [b'^rtsp/'],
    b'sip': [b'^sip/'], b'nntp': [b'^200 nntp'], b'sccp': [b'^\x01\x00\x00\x00$'], b'squid': [b'x-squid-error'],
    b'vmware': [b'vmware'], b'iscsi': [b'\x00\x02\x0b\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'],
    b'redis': [b'^-err unknown command', b'^-err wrong number of arguments', b'^-denied redis is running'],
    b'memcache': [b'^error\r\n'], b'websocket': [b'server: websocket'],
    b'https': [b'instead use the https scheme to accesshttps', b'http request to an https server', b'location: https'],
    b'svn': [b'^\\( success \\( 2 2 \\( \\) \\( edit-pipeline svndiff1'], b'dubbo': [b'^unsupported command'],
    b'elasticsearch': [b'cluster_name.*elasticsearch'], b'rabbitmq': [b'^amqp\x00\x00\t\x01'],
    b'zookeeper': [b'^zookeeper version: ']}

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
        if title == '':
            return title+'标题为空'
        else:
            return title

def Requests(url):
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
    url1 = 'http://'+url
    url2 = 'https://'+url
    title = '获取失败'
    title1 = '获取失败'
    title2 = '获取失败'
    content1 = b'666666666'
    content2 = b'666666666'
    try:
        r = requests.get(url='http://'+url,headers=headers,verify=False,timeout=5)
        if b'Unauthorized' in r.content and b'MAC Address' in r.content and b'IP Address' in r.content:
            return None
        if b'text/html' in r.content or b'<title>' in r.content or b'</html>' in r.content:
            content1 = r.content
            if int(r.status_code) in Alive_Status:
                u = urlparse(str(r.url))
                title1 = get_title(r.content)
                url1 = u.scheme + '://' + u.netloc
        else:
            try:
                s = socket.socket()
                s.settimeout(1)
                s.connect((url.split(':')[0], int(url.split(':')[1])))
                s.send(b'langzi\n\n')
                rec = s.recv(1024)
                s.close()
                if b'Unauthorized' in rec and b'MAC Address' in rec and b'IP Address' in rec:
                    return None
                if b'HTTP' in rec:
                    u = urlparse(str(r.url))
                    title1 = get_title(rec)+'--通过TCP连接端口方式获取信息'
                    url1 = u.scheme + '://' + u.netloc
            except Exception as e:
                pass
            finally:
                s.close()
    except Exception as e:
        try:
            s = socket.socket()
            s.settimeout(1)
            s.connect((url.split(':')[0], int(url.split(':')[1])))
            s.send(b'langzi\n\n')
            rec = s.recv(1024)
            s.close()
            if b'Unauthorized' in rec and b'MAC Address' in rec and b'IP Address' in rec:
                return None
            if b'HTTP' in rec:
                u = urlparse(str('http://'+url))
                title1 = get_title(rec)+'--通过TCP连接端口方式获取信息'
                url1 = u.scheme + '://' + u.netloc
        except Exception as e:
            pass
        finally:
            s.close()
    try:
        r = requests.get(url='https://'+url,headers=headers,verify=False,timeout=5)
        if b'Unauthorized' in r.content and b'MAC Address' in r.content and b'IP Address' in r.content:
            return None
        if b'text/html' in r.content or b'<title>' in r.content or b'</html>' in r.content:
            content2 = r.content
            u = urlparse(str(r.url))
            title2 = get_title(r.content)
            url2 = u.scheme + '://' + u.netloc
        else:
            try:
                s = socket.socket()
                s.settimeout(1)
                s.connect((url.split(':')[0], int(url.split(':')[1])))
                s.send(b'langzi\n\n')
                rec = s.recv(1024)
                s.close()
                if b'Unauthorized' in rec and b'MAC Address' in rec and b'IP Address' in rec:
                    return None
                if b'HTTP' in rec:
                    u = urlparse(str(r.url))
                    title2 = get_title(rec) +'--通过TCP连接端口方式获取信息'
                    url2 = u.scheme + '://' + u.netloc
            except Exception as e:
                pass
            finally:
                s.close()
    except Exception as e:
        pass
    if b'66666' not in content1 and b'sent to HTTPS port' not in content1 and 'sent to HTTPS port' not in title1:
        return [{url1: title1}]
    if b'66666' not in content2 and b'sent to HTTPS port' not in content2 and 'sent to HTTPS port' not in title2:
        return [{url2: title2}]
    if title1 != '获取失败' and title2 == '获取失败':
        return [{url1: title1}]
    if title2 != '获取失败' and title1 == '获取失败':
        return [{url2: title2}]
    if b'66666' not in content1:
        return [{url1:title1}]
    if b'66666' not in content2:
        return [{url2:title2}]
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
    try:
        result = [y for x in result  for y in x]
        return result
    except:
        return []

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
            s.settimeout(0.7)
            s.connect((ip,int(port)))
            s.send(b'langzi\r\n')
            SocketRecv = (s.recv(1024))
            s.close()
            for k,v in Banner.items():
                for b in v:
                    banner = re.search(b,SocketRecv,re.I|re.S)
                    if banner:
                        return k.decode()
            return '获取失败'
        except Exception as e:
            # Log('向端口发起连接异常:{}'.format(str(e)))
            return '获取失败'
        finally:
            s.close()
    def get_alive_host(self):
        # 获取C段全部存活主机，返回数据为列表
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


    def CheckPortOpen(self,ip,port):
        # 该函数用来对nmap扫描端口进行复检，巧妙之处在于socket连接识别完banner，剩下无法识别连
        # 使用本地指纹库识别之前进行二次复检，节省许多不必要复检的端口任务数
        try:
            s = socket.socket()
            s.settimeout(0.5)
            r =s.connect_ex((ip,int(port)))
            if r == 0:
                return True
            else:
                return False
        except:
            return False
        finally:
            s.close()

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
            # res = nm.scan(ip, arguments='-Pn -sS -p 1-65535')
            # 扫全端口不得猴年马月了，有想法扫全端口自己修改吧~
            res = nm.scan(ip, arguments='-Pn -sS -p 6667,11234,1433,12401,898,2144,21571,1050,5904,4242,7070,1098,5190,12174,714,9593,259,10616,1334,5038,2717,5987,6129,11001,1723,3800,32764,8880,1070,99,1461,1862,3546,873,5633,1220,3945,32776,38080,771,3269,8180,5800,1128,27352,5054,366,3780,2288,1053,26000,26214,3390,446,2003,5353,5355,443,49155,10617,5250,3404,15200,50001,563,6502,30000,8290,1352,5214,8834,2035,3005,7770,1071,2161,1022,68,1130,8080,8600,49157,254,1037,5033,12265,27715,12221,44818,57294,14238,27960,9418,9004,100,1082,900,7741,65389,9,22006,1055,5922,8087,666,18040,3817,20034,20256,32913,8222,14442,545,123,2439,20171,5500,10002,5030,1719,6002,52822,48899,49175,9875,6839,13003,10215,60443,5960,1151,3200,4322,1259,89,800,8500,5802,4800,18980,1443,9040,2103,2323,5910,20,6565,9090,1034,5225,8890,5961,1417,32782,7435,23,9390,3372,26256,34443,1580,8014,52311,54345,1030,5959,1078,3077,6100,31337,497,144,11000,2260,5004,5998,37777,6792,7103,3268,90,5550,8082,32769,3995,523,902,25,3057,4433,6692,5554,5999,8042,1201,10004,1783,1062,9502,5080,8888,4111,135,7999,2126,49161,1717,2001,5950,10080,5859,8051,1041,125,4662,1198,8701,1947,8303,1114,2608,280,5002,9814,23943,48080,5814,1087,34205,10162,52673,16993,1801,4899,8021,808,3052,5815,1743,8812,1024,1117,1277,16001,7627,5351,1271,6101,6580,981,5521,32780,1720,8030,65535,2043,2522,41523,2888,45230,9944,27888,6660,222,2045,2170,9102,1216,1604,49,136,3037,55554,32772,1900,4126,1099,1233,1840,5061,2222,8649,6699,9084,1234,1,1067,417,6005,445,402,5986,50502,6006,8193,1106,4443,9011,616,2710,25735,502,5560,691,1010,3017,54045,5226,7777,541,5911,32781,9300,20010,10050,23472,10778,5718,7801,667,16080,2601,726,4001,1089,52302,31001,5440,32783,1186,2375,9999,50002,631,20005,41524,3310,2399,21,3527,2000,57797,5102,3703,1174,5280,8022,20111,1137,1103,6405,49156,554,3465,2013,8686,2702,47002,33,1503,1166,9812,27019,1122,19,1091,17988,1213,3851,8161,1687,5988,7100,7579,1088,9009,1187,9081,8050,28222,5200,524,25000,1169,9050,5051,3551,1090,10629,555,40007,8503,8443,50006,10203,4224,7787,6262,3986,5101,5405,10628,13579,8011,8085,2800,16016,7210,623,1244,1158,5858,31099,4321,55552,2004,3371,6789,119,7080,5877,44501,9900,1111,34571,10180,5909,1079,2701,50300,1084,5678,5298,5269,30718,11211,9991,1864,32777,5905,6080,20031,1310,700,384,49160,10003,7071,5985,25025,67,3324,648,1100,3998,7496,56738,3809,2725,69,50504,13,9503,5989,1007,8400,1423,3351,84,655,60020,901,110,6779,3784,5679,1068,44176,50636,6666,1581,4672,3814,14330,8101,1059,7625,998,5221,2207,4659,5000,2910,3905,8081,9010,5666,5730,1042,65000,9111,5862,8291,10621,2557,162,2500,8889,6901,2492,55600,1494,55555,6161,32,4592,46823,2135,5414,111,1021,1805,5915,2533,43,7937,27356,1112,3920,20222,1029,2009,15000,24800,1061,50070,34573,1527,8444,2394,2301,4,3006,3918,211,7426,7921,5099,912,1914,23502,5631,8091,8654,1102,1066,9290,5925,143,50030,2105,5222,6379,6112,1328,514,6004,1971,161,11110,9251,1110,3460,5566,4002,6000,5520,525,406,3702,20101,7106,1092,6547,19801,9495,1183,27353,587,9415,2718,3001,1812,4005,5227,82,5901,5963,2404,7,9594,2041,30951,1688,1984,8383,1046,10202,12397,9666,783,106,40911,3,3900,992,5100,8402,2046,1145,37,1755,2005,7144,6059,2381,11333,44443,4444,9043,146,617,50800,6504,8901,3370,9815,3369,8010,16000,25672,9810,3389,59777,1935,1309,61532,88,139,3827,8023,3011,7676,8093,50000,1026,65129,5093,61900,7414,1556,1998,7878,18881,4445,23791,687,22,1524,3007,1782,8001,27355,13364,32785,9809,5060,1500,2366,9152,5952,6881,9256,3301,5120,1863,26,5555,1049,9500,64680,49165,42,1038,4129,10025,24444,9917,306,1054,47001,4449,2869,9001,3690,83,548,3869,2379,2106,3071,5902,5357,7911,8300,9110,1031,42510,2199,2100,7800,2990,8083,8095,5431,9618,8999,5908,20828,1999,2121,1027,2480,4125,62078,15004,2809,138,1126,13500,13722,7004,15002,19842,2010,9091,3050,1023,2810,256,1086,27000,7700,9788,1072,6025,3128,28784,8007,3030,7547,711,4998,8899,3632,6156,49400,6,81,49999,3217,6668,3211,22939,4446,3300,5801,32022,340,1700,3322,4848,1149,255,4045,7879,24,3031,4000,1287,2920,7007,2607,5466,9101,30,56737,49153,464,2181,407,7510,53413,416,1521,1121,444,6007,7001,9071,7272,1048,13838,1533,8089,1435,85,199,3828,6988,19350,2022,2525,5433,6050,4279,49163,8008,921,2947,6689,105,4004,911,6566,1035,2002,7003,11099,15003,14000,5811,19283,50003,9080,1164,1002,41025,9711,27018,910,2196,903,7019,49176,6060,6106,6346,9535,3628,520,1875,3790,2065,311,13782,33000,4567,8642,9391,62514,1434,51103,40193,16992,1217,212,9876,1471,1077,63331,2811,9103,264,9811,5822,53,9124,1052,9898,57772,1101,1530,2605,8192,1582,9813,2008,668,880,1236,12000,3333,20221,1248,1063,4070,16018,4006,3766,1147,1131,3659,3889,4003,749,3325,8009,987,64623,32778,1883,5400,5903,7890,2401,15001,1064,2038,1839,3260,8200,25734,2048,7580,16102,2604,1124,2191,32770,3221,6646,3003,7025,6905,2875,1247,80,1119,6510,10082,7938,50389,13783,8000,5009,1218,8902,109,1721,9220,2190,1083,7443,801,49154,2909,19315,1000,2382,14441,1036,8980,4679,1455,16012,41080,1047,389,722,9575,10008,1583,2119,5850,1040,17,1075,179,593,1185,2638,5087,8333,10009,55056,49152,5040,646,8002,1414,8100,1322,11111,44334,787,70,7512,45100,2160,8090,9003,3580,15742,1028,10243,2030,6070,8994,38292,6503,55553,1113,5920,6669,50050,8099,9855,163,2200,6389,8084,3367,8205,9200,5050,10000,79,10566,5247,425,7021,999,15660,8903,1032,2111,33899,10051,1105,1094,1199,5906,33354,1001,1060,1154,3261,1192,8031,2967,1108,2602,49158,6009,500,27017,27015,1039,9595,10626,543,1658,1051,1080,4950,993,1069,3888,32771,843,4343,6001,13456,4786,19810,17200,6123,1501,20000,720,4550,5001,8800,52869,515,2598,8194,1972,1057,9878,32779,12203,9005,1081,10098,5962,8254,17877,6082,10333,5580,1065,512,1600,8088,9100,1033,2021,1761,1104,1296,6567,1093,32768,1301,58080,9998,5632,2067,1097,481,9002,7200,19101,1241,3000,1129,1811,9000,3871,9099,5810,10012,54328,11460,55055,1123,137,8787,513,683,1085,2049,990,3283,3737,6788,7181,7402,1175,10010,28201,1974,1152,1163,32775,1096,8873,32773,5510,8045,1074,3323,6661,8181,1009,777,1044,35500,1148,5180,50503,113,8651,1095,2107,11967,8883,2998,3476,1594,2033,1300,9968,995,1045,2006,1076,8445,19300,51493,2068,5900,87,10099,49167,17185,1641,9877,46824,19780,44442,2362,3500,13013,3181,3689,6371,2040,831,7902,2251,12345,9910,1141,7920,2007,3826,3971,32784,427,8292,3914,52848,41511,1011,22222,26122,8652,3306,689,1025,2034,1073,5907,10443,30015,1666,3517,10001,34572,636,705,3880,2968,6372,1165,5168,50500,1311,1718,301,2047,6969,2380,1211,7778,1043,7000,4900,3168,3801,50004,50501,2179,625,8086,1056,765,9207,3493,465,1132,3878,18988,1440,2152,5498,540,10024,6542,2099,2393,9485,23423,2020,9990,1107,3013,7201,888,3299,1058,31038,5544,6996,1138,5003,7002,8020,6543,1272,5432,49159,5984,6066,37718,32774,458,18101,6003,50013,16113,8028,3273,2042,11006,2383,4750,9943,544,5825')
            try:
                r = res['scan'][ip]['tcp']
                if r:
                    for k, v in r.items():
                        if v.get('state') == 'open':
                            result[k]=v.get('name')
                    if len(result)>200:
                        return {'WAF拦截':'扫描返回开放端口总数:{}'.format(len(result))}
                    for k,v in result.items():
                        banne = self.get_server_from_banner(ip,int(k))
                        if v == banne:
                            pass
                        else:
                            if banne != '获取失败':
                                result[k] = banne
            except:
                time.sleep(10)
                # 重试一次
                # res = nm.scan(ip, arguments='-Pn -sS -p 1-65535')
                # 扫全端口不得猴年马月了，有想法扫全端口自己修改吧~
                res = nm.scan(ip, arguments='-Pn -sS -p 6667,11234,1433,12401,898,2144,21571,1050,5904,4242,7070,1098,5190,12174,714,9593,259,10616,1334,5038,2717,5987,6129,11001,1723,3800,32764,8880,1070,99,1461,1862,3546,873,5633,1220,3945,32776,38080,771,3269,8180,5800,1128,27352,5054,366,3780,2288,1053,26000,26214,3390,446,2003,5353,5355,443,49155,10617,5250,3404,15200,50001,563,6502,30000,8290,1352,5214,8834,2035,3005,7770,1071,2161,1022,68,1130,8080,8600,49157,254,1037,5033,12265,27715,12221,44818,57294,14238,27960,9418,9004,100,1082,900,7741,65389,9,22006,1055,5922,8087,666,18040,3817,20034,20256,32913,8222,14442,545,123,2439,20171,5500,10002,5030,1719,6002,52822,48899,49175,9875,6839,13003,10215,60443,5960,1151,3200,4322,1259,89,800,8500,5802,4800,18980,1443,9040,2103,2323,5910,20,6565,9090,1034,5225,8890,5961,1417,32782,7435,23,9390,3372,26256,34443,1580,8014,52311,54345,1030,5959,1078,3077,6100,31337,497,144,11000,2260,5004,5998,37777,6792,7103,3268,90,5550,8082,32769,3995,523,902,25,3057,4433,6692,5554,5999,8042,1201,10004,1783,1062,9502,5080,8888,4111,135,7999,2126,49161,1717,2001,5950,10080,5859,8051,1041,125,4662,1198,8701,1947,8303,1114,2608,280,5002,9814,23943,48080,5814,1087,34205,10162,52673,16993,1801,4899,8021,808,3052,5815,1743,8812,1024,1117,1277,16001,7627,5351,1271,6101,6580,981,5521,32780,1720,8030,65535,2043,2522,41523,2888,45230,9944,27888,6660,222,2045,2170,9102,1216,1604,49,136,3037,55554,32772,1900,4126,1099,1233,1840,5061,2222,8649,6699,9084,1234,1,1067,417,6005,445,402,5986,50502,6006,8193,1106,4443,9011,616,2710,25735,502,5560,691,1010,3017,54045,5226,7777,541,5911,32781,9300,20010,10050,23472,10778,5718,7801,667,16080,2601,726,4001,1089,52302,31001,5440,32783,1186,2375,9999,50002,631,20005,41524,3310,2399,21,3527,2000,57797,5102,3703,1174,5280,8022,20111,1137,1103,6405,49156,554,3465,2013,8686,2702,47002,33,1503,1166,9812,27019,1122,19,1091,17988,1213,3851,8161,1687,5988,7100,7579,1088,9009,1187,9081,8050,28222,5200,524,25000,1169,9050,5051,3551,1090,10629,555,40007,8503,8443,50006,10203,4224,7787,6262,3986,5101,5405,10628,13579,8011,8085,2800,16016,7210,623,1244,1158,5858,31099,4321,55552,2004,3371,6789,119,7080,5877,44501,9900,1111,34571,10180,5909,1079,2701,50300,1084,5678,5298,5269,30718,11211,9991,1864,32777,5905,6080,20031,1310,700,384,49160,10003,7071,5985,25025,67,3324,648,1100,3998,7496,56738,3809,2725,69,50504,13,9503,5989,1007,8400,1423,3351,84,655,60020,901,110,6779,3784,5679,1068,44176,50636,6666,1581,4672,3814,14330,8101,1059,7625,998,5221,2207,4659,5000,2910,3905,8081,9010,5666,5730,1042,65000,9111,5862,8291,10621,2557,162,2500,8889,6901,2492,55600,1494,55555,6161,32,4592,46823,2135,5414,111,1021,1805,5915,2533,43,7937,27356,1112,3920,20222,1029,2009,15000,24800,1061,50070,34573,1527,8444,2394,2301,4,3006,3918,211,7426,7921,5099,912,1914,23502,5631,8091,8654,1102,1066,9290,5925,143,50030,2105,5222,6379,6112,1328,514,6004,1971,161,11110,9251,1110,3460,5566,4002,6000,5520,525,406,3702,20101,7106,1092,6547,19801,9495,1183,27353,587,9415,2718,3001,1812,4005,5227,82,5901,5963,2404,7,9594,2041,30951,1688,1984,8383,1046,10202,12397,9666,783,106,40911,3,3900,992,5100,8402,2046,1145,37,1755,2005,7144,6059,2381,11333,44443,4444,9043,146,617,50800,6504,8901,3370,9815,3369,8010,16000,25672,9810,3389,59777,1935,1309,61532,88,139,3827,8023,3011,7676,8093,50000,1026,65129,5093,61900,7414,1556,1998,7878,18881,4445,23791,687,22,1524,3007,1782,8001,27355,13364,32785,9809,5060,1500,2366,9152,5952,6881,9256,3301,5120,1863,26,5555,1049,9500,64680,49165,42,1038,4129,10025,24444,9917,306,1054,47001,4449,2869,9001,3690,83,548,3869,2379,2106,3071,5902,5357,7911,8300,9110,1031,42510,2199,2100,7800,2990,8083,8095,5431,9618,8999,5908,20828,1999,2121,1027,2480,4125,62078,15004,2809,138,1126,13500,13722,7004,15002,19842,2010,9091,3050,1023,2810,256,1086,27000,7700,9788,1072,6025,3128,28784,8007,3030,7547,711,4998,8899,3632,6156,49400,6,81,49999,3217,6668,3211,22939,4446,3300,5801,32022,340,1700,3322,4848,1149,255,4045,7879,24,3031,4000,1287,2920,7007,2607,5466,9101,30,56737,49153,464,2181,407,7510,53413,416,1521,1121,444,6007,7001,9071,7272,1048,13838,1533,8089,1435,85,199,3828,6988,19350,2022,2525,5433,6050,4279,49163,8008,921,2947,6689,105,4004,911,6566,1035,2002,7003,11099,15003,14000,5811,19283,50003,9080,1164,1002,41025,9711,27018,910,2196,903,7019,49176,6060,6106,6346,9535,3628,520,1875,3790,2065,311,13782,33000,4567,8642,9391,62514,1434,51103,40193,16992,1217,212,9876,1471,1077,63331,2811,9103,264,9811,5822,53,9124,1052,9898,57772,1101,1530,2605,8192,1582,9813,2008,668,880,1236,12000,3333,20221,1248,1063,4070,16018,4006,3766,1147,1131,3659,3889,4003,749,3325,8009,987,64623,32778,1883,5400,5903,7890,2401,15001,1064,2038,1839,3260,8200,25734,2048,7580,16102,2604,1124,2191,32770,3221,6646,3003,7025,6905,2875,1247,80,1119,6510,10082,7938,50389,13783,8000,5009,1218,8902,109,1721,9220,2190,1083,7443,801,49154,2909,19315,1000,2382,14441,1036,8980,4679,1455,16012,41080,1047,389,722,9575,10008,1583,2119,5850,1040,17,1075,179,593,1185,2638,5087,8333,10009,55056,49152,5040,646,8002,1414,8100,1322,11111,44334,787,70,7512,45100,2160,8090,9003,3580,15742,1028,10243,2030,6070,8994,38292,6503,55553,1113,5920,6669,50050,8099,9855,163,2200,6389,8084,3367,8205,9200,5050,10000,79,10566,5247,425,7021,999,15660,8903,1032,2111,33899,10051,1105,1094,1199,5906,33354,1001,1060,1154,3261,1192,8031,2967,1108,2602,49158,6009,500,27017,27015,1039,9595,10626,543,1658,1051,1080,4950,993,1069,3888,32771,843,4343,6001,13456,4786,19810,17200,6123,1501,20000,720,4550,5001,8800,52869,515,2598,8194,1972,1057,9878,32779,12203,9005,1081,10098,5962,8254,17877,6082,10333,5580,1065,512,1600,8088,9100,1033,2021,1761,1104,1296,6567,1093,32768,1301,58080,9998,5632,2067,1097,481,9002,7200,19101,1241,3000,1129,1811,9000,3871,9099,5810,10012,54328,11460,55055,1123,137,8787,513,683,1085,2049,990,3283,3737,6788,7181,7402,1175,10010,28201,1974,1152,1163,32775,1096,8873,32773,5510,8045,1074,3323,6661,8181,1009,777,1044,35500,1148,5180,50503,113,8651,1095,2107,11967,8883,2998,3476,1594,2033,1300,9968,995,1045,2006,1076,8445,19300,51493,2068,5900,87,10099,49167,17185,1641,9877,46824,19780,44442,2362,3500,13013,3181,3689,6371,2040,831,7902,2251,12345,9910,1141,7920,2007,3826,3971,32784,427,8292,3914,52848,41511,1011,22222,26122,8652,3306,689,1025,2034,1073,5907,10443,30015,1666,3517,10001,34572,636,705,3880,2968,6372,1165,5168,50500,1311,1718,301,2047,6969,2380,1211,7778,1043,7000,4900,3168,3801,50004,50501,2179,625,8086,1056,765,9207,3493,465,1132,3878,18988,1440,2152,5498,540,10024,6542,2099,2393,9485,23423,2020,9990,1107,3013,7201,888,3299,1058,31038,5544,6996,1138,5003,7002,8020,6543,1272,5432,49159,5984,6066,37718,32774,458,18101,6003,50013,16113,8028,3273,2042,11006,2383,4750,9943,544,5825')
                r = res['scan'][ip]['tcp']
                try:
                    if r:
                        for k, v in r.items():
                            if v.get('state') == 'open':
                                result[k] = v.get('name')
                        if len(result) > 200:
                            return {'WAF拦截': '扫描返回开放端口总数:{}'.format(len(result))}
                        for k,v in result.items():
                            banne = self.get_server_from_banner(ip, int(k))
                            if v == banne:
                                pass
                            else:
                                if banne != '获取失败':
                                    result[k] = banne
                except Exception as e:
                    print('错误代码 [13] {} 扫描当前IP失败'.format(str(e)))
                    Error_Log.objects.create(url=ip + '|扫描当前IP失败', error='错误代码 [13] {} '.format(str(e)))
        except Exception as e :
            print('错误代码 [14] {} 扫描当前IP失败'.format(str(e)))
            Error_Log.objects.create(url=ip + '|扫描当前IP失败', error='错误代码 [14] {} '.format(str(e)))
        if result != {}:
            for k in list(result.keys()):
                if result[k] == None or result[k] == 'unknown' or result[k] == '' or result[k] == '获取失败':
                    chk = self.CheckPortOpen(ip,k)
                    if chk == True:
                        result[k] = str(GetPortInfo(str(k)))
                    else:
                        del result[k]

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
        check_alive_url.append('{}:{}'.format(ip,port))
    alive_url = Get_Alive_Url(check_alive_url)
    # 该IP上存活WEB，类型为列表，内容为多个字典
    host_type = IP_Res.get_host_type(ip)
    # windows/linux
    area = IP_Res.get_ip_address(ip)
    # 返回地址

