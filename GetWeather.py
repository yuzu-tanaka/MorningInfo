#!/usr/bin/env python
isDebug = True #False

import urllib.request
from bs4 import BeautifulSoup
import requests
import pdb
from time import sleep
from datetime import datetime as dt

class getWeather():
    def __init__(self):
        # 抽出対象のRSSとURL(RSSは横浜、URLは鎌倉)
        self.rssurl = "https://rss-weather.yahoo.co.jp/rss/days/4610.xml"
        self.tenki = []
        self.detail = []
        self.lastUpdate = None
        if isDebug: print('最初の日時',self.lastUpdate)

    ## Parser : 天気情報WebページのHTMLタグから天気情報を抽出してパースするメソッド ##########################
    def update(self):
        try:
            with urllib.request.urlopen(self.rssurl) as res:
                #pdb.set_trace()
                sleep(1)
                xml = res.read()
                #if isDebug: print(xml)
        except:
            self.tenki = ['---','---']
            self.detail = ['---','---']
            self.lastUpdate = None

        else:
            soup = BeautifulSoup(xml, "html.parser")
            self.tenki = []
            self.detail = []
            self.lastUpdate = None
            
            for item in soup.find_all("item"):
                title = item.find("title").string
                description = item.find("description").string
                if title.find("[ PR ]") == -1:
                    self.tenki.append(title)
                    self.detail.append(description)
                    self.lastUpdate = dt.now()

    def getLastUpdate(self):
        return self.lastUpdate
## メイン処理 ###################################################################################
if __name__ == '__main__':
    WT = getWeather()
    WT.update() # 天気予報サイトのHTMLタグから天気情報を抽出
    print(WT.getLastUpdate())
    print("今日の天気",WT.detail[0])
    print("明日の天気",WT.detail[1])


