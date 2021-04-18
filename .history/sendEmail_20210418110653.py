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
