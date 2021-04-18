# 通过 SMTP 发送邮件

from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib


# 解析邮箱地址
def format_adds(s):
    name, addr = parseaddr(s)
