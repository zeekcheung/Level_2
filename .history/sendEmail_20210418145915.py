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

if mail_type == 'gmail':            # gmail
    smtp_server = 'smtp.gmail.com'
    #port = 465
    sender = from_addr[0:-10]

elif mail_type == 'outlook':        # outlook
    smtp_server = 'smtp.partner.outlook.cn'
    #port = 587
    sender = from_addr[0:-11]

else:
    print('不支持', mail_type, '邮箱')

if to_addr[-9:-4] == 'gmail':
    receiver = to_addr[0:-10]
else:
    receiver = to_addr[0:-11]

# 文本邮件信息
subject = input('邮件主题：')
content = input('邮件内容：')
msg = MIMEText(content, 'plain', 'utf-8')
msg['From'] = format_adds(sender + '<%s>' % from_addr)
print(msg['From'])
msg['To'] = format_adds(receiver + '<%s>' % to_addr)
print(msg['To'])
msg['Subject'] = Header(subject, 'utf-8').encode()

# 连接SMTP服务器,发送邮件
server = smtplib.SMTP_SSL(smtp_server, 465)
server.set_debuglevel(1)  # 打印与SMTP服务器交互的信息
server.login(from_addr, password)
server.sendmail(from_addr, to_addr, msg.as_string())

# 关闭连接
server.quit()
