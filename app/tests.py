# coding:utf-8
import random
import socket
import django
import os
import sys
pathname = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,pathname)
sys.path.insert(0,os.path.abspath(os.path.join(pathname,'..')))
os.environ.setdefault("DJANGO_SETTINGS_MODULE","LangSrcCurise.settings")
django.setup()
from app.models import Other_Url,IP,URL,Show_Data,Error_Log,Cpu_Min,Domains,Setting,Content

BA = Domains.objects.filter(curise='yes')
ALL_DOMAINS = [x.get('url') for x in BA.values()]
'''获取所有监控域名列表'''
print(ALL_DOMAINS)

