#!/usr/bin/env python3
# -*- coding: utf-8 -*-
isDebug = True
#import urllib.request, urllib.error
import requests
from bs4 import BeautifulSoup
import sys
import json
from datetime import datetime as dt
import pdb

class train:
    def __init__(self):
        self.dicUrls={}
        self.dicUrls['東海道線'] = 'https://transit.yahoo.co.jp/diainfo/27/0'
        self.dicUrls['京浜東北線'] = 'https://transit.yahoo.co.jp/diainfo/22/0'
        self.dicUrls['湘南新宿ライン'] = 'https://transit.yahoo.co.jp/diainfo/25/0'
        self.dicUrls['横須賀線'] = 'https://transit.yahoo.co.jp/diainfo/29/0'
        self.lastUpdate = None
        self.trainStatus =[]


    def isTrouble(self, url):
        trouble_info = None
        try:
            res = requests.get(url)
            res.raise_for_status()
        except requests.exceptions.RequestException as e:
            print("Error:{}".format(e))
            return 9
        else:
            Soup = BeautifulSoup(res.text, 'html.parser')
            if isDebug: print(Soup,'\n\n\n')
            trouble_info = Soup.find('dd', class_='trouble')
            if trouble_info != None:
                return 1
            else:
                return 0

    def updateTrainDelay(self, targets=[u'湘南新宿ライン',u'東海道線',u'横須賀線',u'京浜東北線']):
        retList = []
        retText = ""
        retval = []
        infoCount = 0
        #if isDebug: pdb.set_trace()
        for line in targets:
            ret = self.isTrouble(self.dicUrls[line])
            if ret == 1:
                retText += line + ', '
                retList.append(line)
                infoCount += 1
            elif ret == 9:
                retList.append('-')
        if infoCount == 0: 
            retText='現在関連する電車の遅延などは無いようです。' if isDebug else None
        else:
            retText = retText[:-2]+'の運転が遅延しているようです。'
        self.lastUpdate = dt.now()
        #return [retList,retText]
        self.trainStatus = [retList,retText]

    def getLastUpdate(self):
        return self.lastUpdate

if __name__ == '__main__':
    TR=train()
    print('**************************')
    print('LastUpdate: ', TR.getLastUpdate())
    TR.updateTrainDelay()
    print(TR.trainStatus)
    print('**************************')

