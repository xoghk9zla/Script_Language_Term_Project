#!/usr/bin/python
# coding=utf-8

import sys
import time
import telepot
from pprint import pprint
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
from datetime import datetime
import traceback


def getLocationData(loc_param):
    res_list = []
    url = baseurl + '&SIGUN_CD=' + loc_param
    res_body = urlopen(url).read()
    soup = BeautifulSoup(res_body, 'html.parser')
    items = soup.findAll('row')
    for item in items:
        item = re.sub('<.*?>', '\n', item.text)
        parsed = item.split('\n')
        print(parsed)
        try:
            row = parsed[3]+'\n'+parsed[5] + '\n' + parsed[16]+'\n'.strip()

        except IndexError:
            row = item.replace('|', ',')

        if row:
            res_list.append(row.strip())
    return res_list


def replyLocationData(user, loc_param):
    print(user, loc_param)
    res_list = getLocationData(loc_param)
    msg = ''
    for r in res_list:
        print(str(datetime.now()).split('.')[0], r)
        if len(r+msg)+1 > MAX_MSG_LENGTH:
            sendMessage(user, msg)
            msg = r+'\n'
        else:
            msg += r+'\n'
    if msg:
        sendMessage(user, msg)
    else:
        sendMessage(user, '데이터가 없습니다.')


def sendMessage(user, msg):
    try:
        bot.sendMessage(user, msg)
    except:
        traceback.print_exc(file=sys.stdout)


def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type != 'text':
        sendMessage(chat_id, '텍스트 이외의 메시지는 처리하지 못합니다.')
        return

    text = msg['text']
    args = text.split(' ')

    if text.startswith('지역명') and len(args) > 1:
        print('지역명: {0} 검색'.format(args[1]))
        replyLocationData(chat_id, args[1])
    else:
        sendMessage(chat_id, '모르는 명령어입니다.\n지역명 [지역코드] 형식으로 입력하세요.')

    pass


def Launcher():
    global MAX_MSG_LENGTH, baseurl, bot
    TOKEN = '598699953:AAFxTCJW_eul8_ST4BCH98z_qPuThKxs7YU'
    MAX_MSG_LENGTH = 300
    key = '716a00130e0e49a196f9433942b4c728'
    baseurl = 'https://openapi.gg.go.kr/GameSoftwaresDistribution?KEY=' + key

    bot = telepot.Bot(TOKEN)
    pprint(bot.getMe())
    bot.message_loop(handle)
    print("Listening...")
