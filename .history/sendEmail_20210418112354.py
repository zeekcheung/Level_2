# 通过 SMTP 发送邮件

from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib


# 格式化邮箱地址
def format_adds(s):
    name, addr = parseaddr(s)
    # 如果name含有中文，则将其编码进行格式化
    return formataddr((Header(name, 'utf-8').encode(), addr))


# 邮箱信息
mail_type = input('邮箱类型：')
from_addr = input('邮箱地址：')
password = input('邮件密码：')
to_addr = input('收件人地址：')

# 文本邮件信息
subject = input('邮件主题：')
content = input('邮件内容：')
msg = MIMEText(content, 'plain', 'utf-8')
msg['From'] = format_adds(from_addr)
msg['To'] = format_adds(to_addr)
msg['Subject'] = Header(subject, 'utf-8').encode()

# 设置SMTP服务器
if mail_type == 'gmail':            # gmail
    smtp_server = 'smtp.gmail.com'
elif mail_type == 'outlook':        # outlook
    smtp_server = 'smtp.partner.outlook.cn'
else:
    print('不支持', mail_type, '邮箱')
