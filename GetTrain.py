#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import urllib.request, urllib.error
import sys
import json
from datetime import datetime
import pdb

def getTrainDelay(target=[u'湘南新宿ライン',u'東海道線',u'横須賀線',u'京浜東北線']):
    retList = []
    retText = ""
    retval = []
    try:
      #resp = urllib.request.urlopen('https://rti-giken.jp/fhc/api/train_tetsudo/delay.json').read()
      resp = urllib.request.urlopen('https://tetsudo.rti-giken.jp/free/delay.json').read()
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

    print('**************************')
    print(getTrainDelay())
    print('**************************')

