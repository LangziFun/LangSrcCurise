# -*- coding:utf-8 -*-
import schedule,time
import smtplib,configparser
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import xlsxwriter
import django
import os
import sys
import datetime
pathname = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,pathname)
sys.path.insert(0,os.path.abspath(os.path.join(pathname,'..')))
os.environ.setdefault("DJANGO_SETTINGS_MODULE","LangSrcCurise.settings")
django.setup()
from app.models import Other_Url,IP,URL,Show_Data,Error_Log,Cpu_Min,Domains,Setting,Content,BLACKURL
from core.main import Except_Log,close_old_connections


# 尝试获取当天获取的子域名获取数量，来源表为--》域名资产表
from django.utils import timezone
from datetime import timedelta

close_old_connections()
BA = Domains.objects.all()
ALL_DOMAINS = [x.get('url') for x in BA.values()]

cfg = configparser.ConfigParser()
cfg.read('config.ini')
email_host = cfg.get("Email", "host")
email_username = cfg.get("Email", "username")
email_password = cfg.get("Email", "password")
email_receivers = cfg.get("Email","receivers").replace('，',',').replace('|',',')
email_port = int(cfg.get("Email","port"))
try:
    email_receivers = [email_receivers] if ',' not in email_receivers else email_receivers.split(',')
except Exception as e:
    print('序列化收件人信息失败:{}'.format(str(e)))

def MakeInfoResult():
    close_old_connections()
    '''
    2020-01-22
    1. 获取当天得到的子域名数据，按照表格输入
    2. 自动生成两个报告，该报告使用字符串格式输出，用作直接在邮箱显示。第二个报告内容较多，不适合在邮箱直接展示，应该生成excel文档
    3. 发送邮箱的内容为：-->
            24小时内新捕获资产的个数
            一个excel文档，内容为24小时内捕获资产的详情

    +------------------+------------------+----------------------------------+
    |     监控域名     | 当日新增捕获数量 |           报告发送时间           |
    +------------------+------------------+----------------------------------+
    |  sangfor.com.cn  |        4         | 2020-01-21 08:00:01.143213+00:00 |
    |     xin.com      |        36        | 2020-01-21 08:00:01.143213+00:00 |
    |   cainiao.com    |        8         | 2020-01-21 08:00:01.143213+00:00 |
    +------------------+------------------+----------------------------------+

    '''
    XlsxFileName = 'report/'+'-'.join(
        str(datetime.datetime.now()).replace(' ', '-').replace(':', '-').split('.')[0].split('-')) + 'LangSrcCuriseReport.xlsx'
    workbook = xlsxwriter.Workbook(XlsxFileName)
    now = timezone.now()
    start = now - timedelta(hours=23, minutes=59, seconds=59)
    a = '''
        <tr>
        <th>{}</th>
        <th>{}</th>
        </tr>
        '''
    CurrentDaySubdomain = URL.objects.filter(change_time__gt=start)
    # 查询当日24小时捕获的数据
    CurrentUrl = [c.url for c in CurrentDaySubdomain]
    # 捕获所有的网址
    CurrentIp = [c.ip for c in CurrentDaySubdomain]
    # 捕获所有的IP
    CurrentDomain = dict.fromkeys(ALL_DOMAINS,0)
    for domain in ALL_DOMAINS:
        for curl in CurrentUrl:
            if '.'+domain in curl:
                CurrentDomain[domain]+=1
    CurrentDomain = {x:y for x,y in CurrentDomain.items() if y!=0}

    i = datetime.datetime.now()
    timer = ('{}年{}月{}日'.format(i.year, i.month, i.day))
    daycou = len(CurrentUrl)
    allcou = len(list(URL.objects.all()))
    body = '''
        <h1>{}LangSrcCurise资产监控报告</h1>
        <hr>
        <h2>当日新捕获到 {} 个子域名,截至到目前共捕获有效子域名 {} 个</h2>
                <hr>
        <table border='1'>
                <tr>
        <th>监控域名</th>
        <th>当日捕获数量</th>
        </tr>
        '''.format(timer,daycou,allcou)


    worksheet = workbook.add_worksheet('当日捕获数据')
    headings = ['监控域名','当日新增捕获数量', '报告发送时间']  # 设置表头
    worksheet.write_row('A1', headings)
    bold = workbook.add_format({'bold': True})
    worksheet.set_column(0, 10, 20, bold)
    row = 1
    col = 0

    for x,y in CurrentDomain.items():
        worksheet.write_row(row, col, [x,y,str(start).split('.')[0]])
        row+=1
    body = body+''.join([a.format(x,y) for x,y in CurrentDomain.items()])+'</table>'

    CurrentDaySubdomain = Other_Url.objects.filter(url__in=CurrentUrl)
    # 查询当日24小时捕获的数据
    worksheet = workbook.add_worksheet('当日捕获资产数据详情')
    headings = ['捕获新资产网址','网址标题','网站容器','脚本语言','请求响应','IP地址','端口服务','操作系统','部署网站','IP归属地','捕获时间']  # 设置表头
    worksheet.write_row('A1', headings)
    bold = workbook.add_format({'bold': True})
    worksheet.set_column(0, 10, 20, bold)
    row = 1
    col = 0
    for cur in CurrentDaySubdomain:
        try:
            if cur.url in CurrentUrl:
                MidIpObj = IP.objects.filter(ip=cur.ip)
                if list(MidIpObj) == []:
                    worksheet.write_row(row, col,
                                        [cur.url, cur.title, cur.power, cur.server, cur.status, cur.ip, '暂无数据',
                                         '暂无数据', '暂无数据', '暂无数据', str(cur.change_time).split('.')[0]])

                else:
                    Mid = MidIpObj[0]
                    worksheet.write_row(row, col, [cur.url,cur.title,cur.power,cur.server,cur.status,cur.ip,Mid.servers,Mid.host_type,Mid.alive_urls,Mid.area,str(cur.change_time).split('.')[0]])
                row += 1
        except Exception as e:
            Except_Log(stat=107, url='生成Xlsx文档失败，失败原因为:{}', error=str(e))
    workbook.close()
    return (body,XlsxFileName)


def TestEmail(host,port,sender,pwd,receiver):
    body = '<h1>LangSrcCurise邮箱测试发送成功~</h1>'
    msg = MIMEMultipart()
    msg.attach(MIMEText(body, 'html'))
    msg['subject'] = 'LangSrcCurise邮箱可用性测试'
    msg['from'] = 'LangSrcCurise'
    msg['to'] = receiver
    try:
        s = smtplib.SMTP_SSL(host, port)
        s.login(sender, pwd)
        s.sendmail(sender, receiver, msg.as_string())
        print('[Test Email] 邮件发送成功~测试发送邮件成功~\n')
    except smtplib.SMTPException as e:
        print('[Test Email] 邮件发送失败，失败原因为:{}'.format(str(e)))
        Except_Log(stat=104, url='邮件发送失败，失败原因为:{}', error=str(e))
        time.sleep(5)


def SendEmail(body,xlsname,host,port,sender,pwd,receiver):
    xlsxpart = MIMEApplication(open(xlsname, 'rb').read())
    xlsxpart.add_header('Content-Disposition', 'attachment', filename=xlsname)
    msg = MIMEMultipart()
    msg.attach(MIMEText(body, 'html'))
    msg.attach(xlsxpart)
    i = datetime.datetime.now()
    msg['subject'] = '{}年{}月{}日资产监控报告'.format(i.year, i.month, i.day)
    msg['from'] = 'LangSrcCurise每日监控报表'
    msg['to'] = receiver
    try:
        s = smtplib.SMTP_SSL(host, port)
        s.login(sender, pwd)
        s.sendmail(sender, receiver, msg.as_string())
        print('[Send Email] 邮件发送成功！！')
    except smtplib.SMTPException as e:
        print('[Send Email] 邮件发送失败~~~失败原因:{}'.format(str(e)))
        Except_Log(stat=105, url='邮件发送失败~~~失败原因:', error=str(e))

def StartSendReport():
    try:
        a = MakeInfoResult()
        body,xlsname = a[0],a[1]
        for recev in email_receivers:
            try:
                SendEmail(body=body, xlsname=xlsname, host=email_host, port=email_port, sender=email_username, pwd=email_password, receiver=recev)
            except Exception as e:
                Except_Log(stat=107, url='尝试推送每日监控报表到邮箱失败~~~失败原因:', error=str(e))
                pass
    except Exception as e:
        Except_Log(stat=106, url='尝试发送邮箱失败~~~失败原因:', error=str(e))

def SendEmailReport():
    schedule.every().day.at("20:30").do(StartSendReport)
    # 上面代码意思为 每天的 20：30 自动发送报表
    # schedule.every(20).minutes.do(StartSendReport) 每20分钟发送一次
    while 1:
        schedule.run_pending()  # 运行所有可以运行的任务


