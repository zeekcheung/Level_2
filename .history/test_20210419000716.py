unseen_msg = {}

unseen_msg['nums'] = 3

email1 = {
    'Subject': 'ELC4',
    'From': '李贞',
    'Attachment': 'file'
}

email2 = {
    'Subject': 'SMTP',
    'From': 'clementchueng',
    'Content': 'zzz'
}

unseen_msg['email1'] = email1
unseen_msg['email2'] = email2

words = '您现在共有' + str(unseen_msg['nums']) + '封未读邮件,'

if unseen_msg['nums'] > 0:
    for e in unseen_msg.keys():
        if isinstance(unseen_msg[e], dict):
            words += unseen_msg[e]['From'] + '给你给来了一封主题为' + \
                unseen_msg[e]['Subject'] + '的邮件,'

            if 'Contant' in unseen_msg[e]:
                words += '内容为,' + unseen_msg[e]['Content']

            if 'Attachment' in unseen_msg[e]:
                words += '还有一个附件,' + unseen_msg[e]['Attachment']

tts = gTTS(words)
tts.save('email.mp3')
