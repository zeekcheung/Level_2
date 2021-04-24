# 获取最新的OA通知,并发送到邮箱中
import datetime
import requests
from bs4 import BeautifulSoup

from sendEmail import sendEmail

# 设置邮箱信息
mail_type = 'outlook'
from_addr = '19zyzhang@stu.edu.cn'
password = 'zz2001..'
to_addr = '19zyzhang@stu.edu.cn'

index = requests.get('http://oa.stu.edu.cn/login/Login.jsp?logintype=1')
soup = BeautifulSoup(index.text, 'html.parser')
# print(type(soup))
# print(soup.text)

accept = ['书院总院', '校团委', '敬一书院', '党政办公室', '党委组织部', '教务处','基建处']  # 筛选发布通知的单位
today = datetime.date.today()  # 当日日期
oneDay = datetime.timedelta(days=1)
yesterday = today - oneDay  # 前一天日期
data_block = soup.select('.datalight')  # 最新页面中的所有通知所在的元素
data_block = data_block[0:-1]

for d in data_block:
    # 筛选出最新邮件 筛选出发布通知的单位
    date = d.contents[-2].string
    union = d.contents[3].string
    if (date == str(today) or date == str(yesterday)) and union in accept:
        # 获取每条通知标题、发布单位、链接
        title = d.contents[1].contents[0]['title']  # 标题
        organization = d.contents[3].string  # 发布单位
        subject = organization + title
        link = 'http://oa.stu.edu.cn' + d.contents[1].contents[0]['href']  # 链接
        # print(link)

        # 获取每条通知的页面
        index = requests.get(link)
        html = BeautifulSoup(index.text, 'html.parser')
        print(soup)

        # 发送邮件
        sendEmail(mail_type, from_addr, password, to_addr, subject, html)
