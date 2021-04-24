# 通过 SMTP 发送邮件

from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib


# 格式化邮箱地址
def format_adds(s):
    name, addr = parseaddr(s)
    # 如果name含有中文，则将其编码进行格式化
    return formataddr((Header(name, 'utf-8').encode(), addr))


# 发送邮件
def sendEmail(mail_type, from_addr, password, to_addr, subject, content):
    # 设置SMTP服务器及发件人名
    sender = ''
    smtp_server = ''
    if mail_type == 'gmail':  # gmail
        sender = from_addr[0:-10]
        # gmail采用SSL加密方式
        smtp_server = 'smtp.gmail.com'

    elif mail_type == 'outlook':  # outlook
        sender = from_addr[0:-11]
        # outlook采用 STARTTLS 加密方式
        smtp_server = 'smtp.partner.outlook.cn'

    else:
        print('不支持', mail_type, '邮箱')

    port = 587
    server = smtplib.SMTP(smtp_server, port)
    server.ehlo()
    server.starttls()

    # 收件人名
    if to_addr[-9:-4] == 'gmail':
        receiver = to_addr[0:-10]
    else:
        receiver = to_addr[0:-11]

    if isinstance(content, str):
        msg = MIMEText(content, 'plain', 'utf-8')
    else:
        msg = MIMEText(content, 'html', 'utf-8')
    msg['From'] = format_adds(sender + '<%s>' % from_addr)
    print(msg['From'])
    msg['To'] = format_adds(receiver + '<%s>' % to_addr)
    print(msg['To'])
    msg['Subject'] = Header(subject, 'utf-8').encode()

    # 连接SMTP服务器,发送邮件
    server.set_debuglevel(1)  # 打印与SMTP服务器交互的信息
    server.login(from_addr, password)
    server.sendmail(from_addr, to_addr, msg.as_string())

    # 关闭连接
    server.quit()


# 只在该模块内运行输入邮箱邮件信息
if __name__ == '__main__':
    # 输入邮箱信息
    mail_type = input('邮箱类型：')
    from_addr = input('邮箱地址：')
    password = input('邮件密码：')
    to_addr = input('收件人地址：')
    # 文本邮件信息
    subject = input('邮件主题：')
    content = input('邮件内容：')
    sendEmail(mail_type, from_addr, password, to_addr, subject, content)
else:
    pass
