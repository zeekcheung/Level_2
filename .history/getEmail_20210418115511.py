# 通过 IMAP 收取邮件

username =


def getEmail():
    mail_type = input('邮箱类型：')
    username = input('邮箱地址：')
    password = input('邮箱密码：')

    if mail_type == 'gmail':
        imap_server = 'imap.gmail.com'


port = 993
