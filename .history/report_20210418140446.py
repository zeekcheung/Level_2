# 将POP3获取的邮件内容发送到百度语音合成

import getEmail
from gtts import gTTS

getEmail.print_msg('this is a msg')


words = '您的' + getEmail()

gtts = gTTS()
