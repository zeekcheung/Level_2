# 通过 IMAP 收取邮件

import imaplib
import email
from email.header import decode_header
import webbrowser
import os


def getEmail():
    # 邮箱信息
    mail_type = input('邮箱类型：')
    username = input('邮箱地址：')
    password = input('邮箱密码：')

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

    # 获取所有未读邮件
    status, response = imap.uid('SEARCH', None, '(UNSEEN')
    unseen_msg_nums = response[0].split()  # 统计未读邮件数量

    for e_id in unseen_msg_nums:
        # 通过uid匹配邮件
        res, msg = imap.uid('FETCH', e_id, '(UID BODY[TEXT])')

        for response in msg:
            if isinstance(response, tuple):
                # 将邮件类型(bytes)转换为对象(object)
                msg = email.message_from_bytes(response[1])

                # 解码邮件主题
                subject, encoding = decode_header(msg['Subject'])[0]
                if encoding is None:
                    content_type = msg.get('Content-Type', '').lower()
                    pos = content_type.find('charset=')
                    if pos >= 0:
                        encoding = content_type[pos + 8:].strip()
                    if encoding == None:
                        encoding = 'utf-8'
                    if isinstance(subject, bytes):
                        # 解码为字符串
                        subject = subject.decode(encoding)

    # 关闭连接
    imap.logout()
