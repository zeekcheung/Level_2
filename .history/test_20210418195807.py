# 通过 IMAP 收取邮件

import imaplib
import email
from email.header import decode_header
import webbrowser
import os

imap_ssh_host = 'imap.gmail.com'
imap_ssh_port = 993
username = 'clementchueng@gmail.com'
password = 'zz2001..'
server = imaplib.IMAP4_SSL(imap_ssh_host, imap_ssh_port)

server.login(username, password)
server.select('INBOX')

data = server.uid('search', None, '(UNSEEN)')

print(data)
