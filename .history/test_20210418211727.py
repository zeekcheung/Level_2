# 通过 IMAP 收取邮件

import imaplib
import email
from email.header import decode_header
from email.parser import BytesParser
from email.utils import parseaddr


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


status, data = imap.search(None, '(UNSEEN)')
email_list = list(reversed(data[0].split()))

for uid in email_list:
    status, content = imap.fetch(uid, '(RFC822)')
    msg = BytesParser().parsebytes(content[0][1])
    sub = msg.get('Subject')
    From = msg.get('From')
    To = msg.get('To')
    for part in msg.walk():
        fileName = part.get_filename
        fileName = decode_str(fileName)
        if fileName != None:
            print('=' * 100)
            print(fileName)

    print('sub', decode_str(sub))
    print('From', decode_str(From))
    print('To', decode_str(To))
