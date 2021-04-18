# 通过 IMAP 收取邮件

import imaplib
import email
from email.header import decode_header
import webbrowser
import os

imap_ssh_host = 'smtp.partner.outlook.cn'
imap_ssh_port = 993
username = '19zyzhang@stu.edu.cn'
password = 'zz2001..'
imap = imaplib.IMAP4_SSL(imap_ssh_host, imap_ssh_port)

imap.login(username, password)
imap.select('INBOX')

data = server.uid('search', None, '(UNSEEN)')

status, data = imap.search(None, 'ALL')
for num in data[0].split():
    status, data = imap.fetch(num, '(RFC822)')
    email_msg = data[0][1]
    print(email_msg)
