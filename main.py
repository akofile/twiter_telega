import requests
from twitter_scraper import get_tweets
import time

def send_telegram(text: str, channel):
    token = "1210743698:AAEFbjFZ30VgbdpB7MaHQ_4CwUa1DAQIYig"
    url = "https://api.telegram.org/bot"
    channel_id = channel
    url += token
    method = url + "/sendMessage"

    r = requests.post(method, data={
         "chat_id": channel_id,
         "text": text
          })
    print(r)


channel_twitter={}
f = open('Channel_Twitter.txt', 'r')
kk = f.read().split('\n')
f.closed
for k in kk:
    channel_twitter[k.split(':')[0]]=k.split(':')[1]
last_msg={}
f = open('last_msg.txt', 'r', encoding='utf-8')
kk = f.read().split('\n')
f.closed
if kk!=['']:
    for k in kk:
        try:
            last_msg[k.split(':')[0]]=k.split(':')[1]
        except Exception:
            continue

while 1:
    time.sleep(3)
    for ct in channel_twitter:
        buf1=get_tweets(channel_twitter[ct], pages=1).__next__()
        buf=buf1['text']
        if buf.find('…')>0:
            buf=buf.replace('…','')
        if ct in last_msg.keys():
            if last_msg[ct]!= buf[:len(last_msg[ct])]:
                if buf1['isRetweet']:
                    send_telegram('RT: @'+buf1['username']+': '+buf, '@' + ct)
                    last_msg[ct] = buf
                else:
                    send_telegram(buf,'@'+ ct)
                    last_msg[ct]=buf
        else:
            if buf1['isRetweet']:
                send_telegram('RT: @' + buf1['username'] + ': ' + buf, '@' + ct)
                last_msg[ct] = buf
            else:
                send_telegram(buf, '@' + ct)
                last_msg[ct] = buf

    f = open('last_msg.txt', 'w', encoding='utf-8')
    for lm in last_msg:
        f.writelines(lm+':'+last_msg[lm])