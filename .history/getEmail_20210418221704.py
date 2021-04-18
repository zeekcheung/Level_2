# 通过 IMAP 收取邮件

import imaplib
import email
from email.header import decode_header
from email.parser import BytesParser
from email.utils import parseaddr
import os


# 解码
def decode_str(s):
    try:
        s = email.header.decode_header(s)
    except:
        # print('Header decode error')
        return None

    s_bytes = s[0][0]
    s_charset = s[0][1]

    if s_charset == None:
        s = s_bytes
    elif s_charset == 'unknown-8bit':
        s = str(s_bytes, 'utf8')
    else:
        s = str(s_bytes, s_charset)

    return s


def clean(text):
    # 创建没有空格和特殊字符的a文件夹，用来存放邮件
    return "".join(c if c.isalnum() else "_" for c in text)


def getEmail():
    # 邮箱信息
    # mail_type = input('邮箱类型：')
    # username = input('邮箱地址：')
    # password = input('邮箱密码：')
    mail_type = 'outlook'
    username = '19zyzhang@stu.edu.cn'
    password = 'zz2001..'

    # 设置 IMAP 服务器
    if mail_type == 'gmail':        # gmail
        imap_server = 'imap.gmail.com'
    elif mail_type == 'outlook':    # outlook
        imap_server = 'partner.outlook.cn'

    # 连接 IMAP 服务器
    imap = imaplib.IMAP4_SSL(imap_server)
    imap.login(username, password)

    # 选择一个邮箱：收件箱
    imap.select('INBOX')

    status, data = imap.search(None, '(UNSEEN)')
    unseen_msg_nums = len(data[0].split())
    unseen_msg = {}
    unseen_msg['nums'] = unseen_msg_nums
    i = 1

    if unseen_msg_nums > 0:
        email_list = list(reversed(data[0].split()))

        for uid in email_list:
            status, content = imap.fetch(uid, '(RFC822)')
            msg = BytesParser().parsebytes(content[0][1])
            Subject = msg.get('Subject')
            From = msg.get('From')
            To = msg.get('To')
            mail = {}
            mail['Subject'] = Subject
            mail['From'] = From
            mail['To'] = To

            for part in msg.walk():
                fileName = part.get_filename
                fileName = decode_str(fileName)
                if fileName != None:
                    print('=' * 100)
                    print(fileName)
                    mail['File'] = fileName

            unseen_msg['email' + str(i)] = mail
            i += 1

            print('Subject：', decode_str(Subject))
            print('From：', decode_str(From))
            print('To：', decode_str(To))

    return unseen_msg
