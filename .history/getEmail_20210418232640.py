# 通过 IMAP 收取邮件
# -*- coding: utf-8 -*-

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
        email_list = list(data[0].split())

        for uid in email_list:
            status, content = imap.fetch(uid, '(RFC822)')
            msg = BytesParser().parsebytes(content[0][1])
            Subject = decode_str(msg.get('Subject'))
            From = decode_str(msg.get('From'))
            mail = {}
            mail['Subject'] = Subject
            mail['From'] = From

            if msg.is_multipart():
                for part in msg.walk():
                    content_type = part.get_content_type()
                    content_disposition = str(part.get("Content-Disposition"))

                    # 获取邮件内容
                    try:
                        body = part.get_payload(decode=True).decode()
                    except:
                        pass

                    if content_type == "text/plain" and "attachment" not in content_disposition:
                        # 如果邮件内容只有文本信息，则打印出来
                        mail['Content'] = body
                    elif "attachment" in content_disposition:
                        # 下载附件
                        filename = decode_str(part.get_filename())

                        if filename:
                            mail['Attachment'] = filename
                            folder_name = decode_str(filename)
                            if not os.path.isdir(folder_name):
                                # 创建存放该邮件的文件夹
                                os.mkdir(folder_name)

                            filepath = os.path.join(folder_name, filename)

                            # 下载附件并保存
                            open(filepath, "wb").write(
                                part.get_payload(decode=True))

            else:
                content_type = msg.get_content_type()

                body = msg.get_payload(decode=True).decode()

                if content_type == "text/plain":
                    mail['Content'] = body

                if content_type == "text/html":
                    folder_name = decode_str(Subject)
                    if not os.path.isdir(folder_name):
                        os.mkdir(folder_name)

                    filename = "index.html"
                    mail['Attachment'] = filename
                    filepath = os.path.join(folder_name, filename)

                    open(filepath, "w").write(msg.get_payload(decode=True))

            unseen_msg['email' + str(i)] = mail
            i += 1

            print('Subject：', Subject)
            print('From：', From)

    return unseen_msg
