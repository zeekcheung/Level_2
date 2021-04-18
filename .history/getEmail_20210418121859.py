# 通过 IMAP 收取邮件

import imaplib


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
        res, msg = imap.uid('FETCH', e_id, '(UID BODY[TEXT])')

    # 关闭连接
    imap.logout()
