# 将IMAP获取的邮件内容发送到gTTS合成
# -*- coding: utf-8 -*-

import getEmail
from gtts import gTTS

unseen_msg = getEmail.getEmail()

words = '您现在共有' + str(unseen_msg['nums']) + '封未读邮件,'

i = 1

if unseen_msg['nums'] > 0:
    for e in unseen_msg.keys():
        if isinstance(unseen_msg[e], dict):
            words += unseen_msg[e]['From'] + '给你给来了第' + str(i) + '封主题为' + \
                unseen_msg[e]['Subject'] + '的邮件,'

            if 'Contant' in unseen_msg[e]:
                words += '内容为,' + unseen_msg[e]['Content']

            if 'Attachment' in unseen_msg[e]:
                words += '还有一个附件,' + unseen_msg[e]['Attachment'] + '
        i += 1

tts = gTTS(words,lang='zh-TW')
tts.save('email.mp3')
