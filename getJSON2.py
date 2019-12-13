#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import urllib.request, urllib.error
import sys
import json
from datetime import datetime
import pdb
def getWether(citycode= '140010'):
    retval = {'title':'-','message':'-','day':'-','telop':'-','icon':'-','max':'-','min':'-'}
    forecasts = {}
    try:
      #citycode = '130010' #東京
      resp = urllib.request.urlopen('http://weather.livedoor.com/forecast/webservice/json/v1?city=%s'%citycode).read()
      #pdb.set_trace()
    except:
      resp = ''
    if resp != '':
      # 読み込んだJSONデータをディクショナリ型に変換
      #resp = json.loads(resp)
      #cont = json.loads(resp.read().decode('utf8'))
      cont = json.loads(resp.decode('utf8'))
      
      retval['title']=cont['title']
      retval['message']=cont['description']['text']
      retday = ('今日',0)
      #15時以降は、明日の天気を表示する
      if int(datetime.now().strftime('%H')) >= 15: retday = ('明日',1) 
      retval['day']=retday[0]
      forecast = cont['forecasts'][retday[1]]

      retval['telop']=forecast['telop']
      #livedoorのIconファイル名からIcon番号を作成
      rettmp = forecast['image']['url'].split('/')
      rettmp = rettmp[-1].split('.')[0]
      retval['icon']=rettmp
    
      if None != forecast['temperature']['max']:
        retval['max']=forecast['temperature']['max']['celsius']
      else:
        retval['max']=None
      if None != forecast['temperature']['min']:
        retval['min']=forecast['temperature']['min']['celsius']
      else:
        retval['min']=None

    return retval

def getTrainDelay(target=[u'湘南新宿ライン',u'東海道線',u'横須賀線',u'京浜東北線']):
    retList = []
    retText = ""
    retval = []
    try:
      resp = urllib.request.urlopen('https://rti-giken.jp/fhc/api/train_tetsudo/delay.json').read()
    except:
        resp =  ''

    if resp != '':
      #delays = json.loads(delays)
      delays = json.loads(resp.decode('utf8'))

      infoCount = 0
      for delay in delays:
          if delay['name'] in target:
              retText+=delay['name'] + ', '
              retList.append(delay['name'])
              infoCount += 1
      if infoCount == 0: 
          #retText='現在関連する電車の遅延などは無いようです。'
          retText=None
      else:
          retText = retText[:-2]+'の運転が遅延しているようです。'
    return [retList,retText]


if __name__ == '__main__':

    resp = getWether('140010')
    
    print('**************************')
    print(resp['title'])
    print('**************************')
    print(resp['message'])
    print('**************************')
    print(resp['day'])
    print(resp['telop'])
    print(resp['icon'])
    print(resp['max'])
    print(resp['min'])
    
    print('**************************')
    print(getTrainDelay())
    print('**************************')

#~ if __name__ == '__main__':

    #~ resp = getWether('130010')
    
    #~ print('**************************')
    #~ print(resp['title'])
    #~ print('**************************')
    #~ print(resp['description']['text'])
    
    #~ for forecast in resp['forecasts']:
        #~ print('**************************')
        #~ print(forecast['dateLabel']+'('+forecast['date']+')')
        #~ print(forecast['telop'])
        #~ print(forecast['image']['url'])
        #~ if None != forecast['temperature']['max']:
            #~ print(forecast['temperature']['max']['celsius'])
        #~ if None != forecast['temperature']['min']:
            #~ print(forecast['temperature']['min']['celsius'])
    #~ print('**************************')
    
    #~ print('**************************')
    #~ delays = getTrainDelay()
    #~ infoCount = 0
    #~ for delay in delays:
        #~ if delay['name'] in ['湘南新宿ライン','東海道線','横須賀線','京浜東北線']:
            #~ print(delay['name'] + 'が遅れてます')
            #~ infoCount += 1
    #~ if infoCount == 0: print('Delay info is none.')
