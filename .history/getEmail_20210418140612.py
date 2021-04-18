# 通过 IMAP 收取邮件

import imaplib
import email
from email.header import decode_header
import webbrowser
import os


def clean(text):
    # 创建没有空格和特殊字符的文件夹，用来存放邮件
    return "".join(c if c.isalnum() else "_" for c in text)


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
    status, response = imap.uid('SEARCH', None, '(UNSEEN'))
    unseen_msg_nums=response[0].split()  # 统计未读邮件数量
    unseen_msg={}  # 存储所有未读邮件信息的字典
    i=1

    for e_id in unseen_msg_nums:
        # 通过uid匹配邮件
        res, msg=imap.uid('FETCH', e_id, '(UID BODY[TEXT])')

        for response in msg:
            mail={}

            if isinstance(response, tuple):
                # 将邮件类型(bytes)转换为对象(object)
                msg=email.message_from_bytes(response[1])

                # 解码邮件主题
                subject, encoding=decode_header(msg['Subject'])[0]
                if encoding is None:
                    content_type=msg.get('Content-Type', '').lower()
                    pos=content_type.find('charset=')
                    if pos >= 0:
                        encoding=content_type[pos + 8:].strip()
                    if encoding == None:
                        encoding='utf-8'
                    if isinstance(subject, bytes):
                        # 解码为字符串
                        subject=subject.decode(encoding)

                    # 解码发件人
                    From, encoding=decode_header(msg.get('From'))[0]
                    if isinstance(From, bytes):
                        From=From.decode(encoding)

                    mail['From']=From
                    mail['Subject']=subject

                    if msg.is_multipart():
                        for part in msg.walk():
                            content_type=part.get_content_type()
                            content_disposition=str(
                                part.get('Content-Disposition'))

                            # 获取邮件内容
                            try:
                                body=part.get_payload(decode = True).decode()
                            except:
                                pass

                            if content_type == 'text/plain' and 'attachment' not in content_disposition:
                                # 如果邮件内容只有文本信息，则打印出来
                                print(body)
                                mail['Body']='一段文字,' + body
                            elif 'attachment' in content_disposition:
                                mail['Body']='一个附件,请及时查收'
                                # 下载并保存附件
                                filename=part.get_filename()
                                if filename:
                                    folder_name=clean(subject)
                                    if not os.path.isdir(folder_name):
                                        # 创建存放该附件的文件夹
                                        os.mkdir(folder_name)

                                    filepath=os.path.join(
                                        folder_name, filename)

                                    # 下载附件并保存
                                    open(filepath, 'wb').write(
                                        part.get_payload(decode=True))

                    else:
                        content_type=msg.get_content_type()

                        body=msg.get_payload(decode = True).decode()

                        if content_type == 'text/plain':
                            print(body)
                            mail['Body']='一段文字,' + body
                        if content_type == 'text/html':
                            folder_name=clean(subject)
                            mail['Body']='一个html页面，请及时查收'
                        if not os.path.isdir(folder_name):
                            os.mkdir(folder_name)

                            filename='index.html'
                            filepath=os.path.join(folder_name, filename)

                            open(filepath, 'w').write(body)
                            # 打开默认浏览器
                            webbrowser.open(filepath)

                print('=' * 100)
                unseen_msg['email' + str(i)]=email
            i += 1

    # 关闭当前选择的邮箱。删除的邮件将可从邮箱中删除。相当于以前的logout()函数
    imap.logout()


getEmail()
