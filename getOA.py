# 获取最新的OA通知,并发送到邮箱中
import datetime
import requests
from bs4 import BeautifulSoup

from sendEmail import sendEmail

# 设置邮箱信息
mail_type = input('邮箱类型')
from_addr = input('发件邮箱')
password = input('邮箱密码')
to_addr = input('收件邮箱')

link = ''
index = requests.get(link)
soup = BeautifulSoup(index.content, 'html.parser')
# print(type(soup))
# print(soup.text)

accept = ['书院总院', '校团委', '敬一书院', '党政办公室', '党委组织部']  # 筛选发布通知的单位
today = datetime.date.today()  # 当日日期
oneDay = datetime.timedelta(days=1)
yesterday = str(today - oneDay)  # 前一天日期
data_block = soup.select('.datalight')  # 最新页面中的所有通知所在的元素

for d in data_block:
	# 筛选出最新邮件 筛选出发布通知的单位
	date = d.contents[-2].string
	if (date == today or date == yesterday) and d.contents[3].string in accept:
		# 获取每条通知标题、发布单位、链接
		title = d.contents[1].contents[0]['title']  # 标题
		organization = d.contents[3].string  # 发布单位
		subject = organization + title
		link = 'http://oa.stu.edu.cn' + d.contents[1].contents[0]['href']  # 链接
		# print(link)

		# 获取每条通知的页面
		index = requests.get(link)
		html = BeautifulSoup(index.content, 'html.parser')
		print(soup)

		# 发送邮件
		sendEmail(mail_type, from_addr, password, to_addr, subject, html)
