﻿import requests
import json
from pprint import pprint
from time import sleep
"""
Парсинг СМС собщений с сайта www.onlinesim.ru
"""

headers = {
    'Host': 'onlinesim.ru',
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
}

gl_ls_msg=[]

def AddMsg(msg):
    global gl_ls_msg
    if len(gl_ls_msg)==20: gl_ls_msg.pop(0)
    if gl_ls_msg.count(msg)==0:
        gl_ls_msg.append(msg)
        return msg

def GetMsg(number):
    global headers
    while 1==1:
        r=requests.get(f'https://www.onlinesim.ru/api/getFreeMessageList?page=1&phone={number}&lang=ru', headers=headers)
        dic=json.loads(r.text)
        ls_msg=dic['messages']['data']
        for i, dc in enumerate(ls_msg):
            #print(f'{i+1}.', dc['created_at'], ' -- ',dc['text'])
            s=AddMsg(f"{dc['created_at']} -- {dc['text']}")
            if s!= None: print(s)
        sleep(5)

def ListPhone():
    global headers
    r=requests.get('https://www.onlinesim.ru/api/getFreePhoneList?country=7&lang=ru', headers=headers)
    dic=json.loads(r.text)
    #pprint(dic)
    for i, dic_2 in enumerate(dic['numbers']):
        print(f'{i+1}. {dic_2["full_number"]}, {dic_2["country_text"]}, {dic_2["data_humans"]}' )
    n=int(input('Выберите порядковый номер телефона. '))
    if n>len(dic['numbers']):
        print('Неверный порядковый номер.')
        return
    print('****************************')
    print(f'Выбран номер: {dic["numbers"][n-1]["full_number"]}')
    print('****************************')
    return dic["numbers"][n-1]["number"]


if __name__=='__main__':
    number=ListPhone()
    if number!=None: GetMsg(number)
