# 通过 IMAP 收取邮件

import imaplib
import email
from email.header import decode_header
from email.parser import BytesParser
from email.utils import parseaddr
import os

imap_ssh_host = 'smtp.partner.outlook.cn'
imap_ssh_port = 993
username = '19zyzhang@stu.edu.cn'
password = 'zz2001..'
imap = imaplib.IMAP4_SSL(imap_ssh_host, imap_ssh_port)

imap.login(username, password)
imap.select('INBOX')


def decode_str(s):
    try:
        subject = email.header.decode_header(s)
    except:
        # print('Header decode error')
        return None

    sub_bytes = subject[0][0]
    sub_charset = subject[0][1]

    if sub_charset == None:
        subject = sub_bytes
    elif sub_charset == 'unknown-8bit':
        subject = str(sub_bytes, 'tuf8')
    else:
        subject = str(sub_bytes, sub_charset)

    return subject
# data = imap.uid('search', None, '(UNSEEN)')


def clean(text):
    # 创建没有空格和特殊字符的a文件夹，用来存放邮件
    return "".join(c if c.isalnum() else "_" for c in text)


status, data = imap.search(None, '(UNSEEN)')
email_list = list(reversed(data[0].split()))

for uid in email_list:
    status, content = imap.fetch(uid, '(RFC822)')
    msg = BytesParser().parsebytes(content[0][1])
    sub = msg.get('Subject')
    From = msg.get('From')
    To = msg.get('To')

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
                print(body)
            elif "attachment" in content_disposition:
                # 下载附件
                filename = part.get_filename()
                if filename:
                    folder_name = clean(sub)
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
            print(body)

            filename = "index.html"
            filepath = os.path.join(folder_name, filename)

            open(filepath, "w").write(body)
            # 打开默认浏览器
            webbrowser.open(filepath)

    print("=" * 100)

    print('sub', decode_str(sub))
    print('From', decode_str(From))
    print('To', decode_str(To))
