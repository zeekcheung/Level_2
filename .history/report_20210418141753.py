# 将POP3获取的邮件内容发送到百度语音合成

import getEmail
from gtts import gTTS

unseen_msg = getEmail.getEmail()

words = '您现在共有' + unseen_msg['nums'] + '封未读邮件'

for e in unseen_msg.keys():
    words += unseen_msg[e]['From'] + '给你给来了一封主题为' + \
        unseen_msg['Subject'] + '的邮件,内容为' + unseen_msg['Body']

tts = gTTS(words)
tts.save('email.mpe')
