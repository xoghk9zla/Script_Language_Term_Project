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


local_code = {'수원시':'41110', '성남시':'41130', '의정부시':'41150', '안양시':'41170', '부천시':'41190', '광명시':'41210', '평택시':'41220', '동두천시':'41250', '안산시':'41270',
              '고양시':'41280', '과천시':'41290', '구리시':'41310', '남양주시':'41360', '오산시':'41370', '시흥시':'41390', '군포시':'41410', '의왕시':'41430', '하남시':'41450',
              '용인시':'41460', '파주시':'41480', '이천시':'41500', '안성시':'41550', '김포시':'41570', '화성시':'41590', '광주시':'41610', '양주시':'41630', '포천시':'41650',
              '여주시':'41670', '연천군':'41800', '가평군':'41820', '양평군':'41830'}


def getLocationData(loc_param):
    res_list = []
    url = baseurl + '&SIGUN_CD=' + local_code[loc_param]
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
