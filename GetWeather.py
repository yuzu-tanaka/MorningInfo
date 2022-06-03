#!/usr/bin/env python
isDebug = True
#import urllib.request
#from bs4 import BeautifulSoup
import requests
import pdb
from time import sleep
from datetime import datetime as dt

class getWeather():
    def __init__(self):
        # 抽出対象のRSSとURL(RSSは横浜、URLは鎌倉)
        self.rssurl = "https://weather.tsukumijima.net/api/forecast/city/140010"
        self.tenki = []
        self.detail = []
        self.temperatureMin = []
        self.temperatureMax = []
        self.chanceOfRain = []
        self.lastUpdate = None
        if isDebug: print('最初の日時',self.lastUpdate)
    ## 最大の降水確率を返す
    def getMaxChanceOfRain(self,dicChance):
        retVal = 0
        for i in dicChance:
            tempVal = dicChance[i][:-1]
            if tempVal != '--':
                retVal = int(tempVal) if int(tempVal) >= retVal else retVal
        return retVal
            
    ## Parser : 天気情報WebページのHTMLタグから天気情報を抽出してパースするメソッド ##########################
    def update(self):
        try:
            res = requests.get(self.rssurl)
            res.raise_for_status()
        except requests.exceptions.RequestException as e:
            self.tenki = ['---','---']
            self.detail = ['---','---']
            self.lastUpdate = None
            print("Error:{}".format(e))

        else:
            jsonWeather = res.json()
            self.tenki = []
            self.detail = []
            self.lastUpdate = dt.now()
            self.tenki.append(jsonWeather["forecasts"][0]["dateLabel"])
            self.tenki.append(jsonWeather["forecasts"][1]["dateLabel"])
            self.detail.append(jsonWeather["forecasts"][0]["telop"])
            self.detail.append(jsonWeather["forecasts"][1]["telop"])
            # 気温
            ret = jsonWeather["forecasts"][0]["temperature"]["min"]["celsius"]
            if ret == 'null':
                ret = None
            self.temperatureMin.append(ret)
            ret = jsonWeather["forecasts"][1]["temperature"]["min"]["celsius"]
            if ret == 'null':
                ret = None
            self.temperatureMin.append(ret)
            ret = jsonWeather["forecasts"][0]["temperature"]["max"]["celsius"]
            if ret == 'null':
                ret = None
            self.temperatureMax.append(ret)
            ret = jsonWeather["forecasts"][1]["temperature"]["max"]["celsius"]
            if ret == 'null':
                ret = None
            self.temperatureMax.append(ret)
            # 降水確率（時間ごとで最大を取る）
            chanceOfRain = jsonWeather["forecasts"][0]["chanceOfRain"]
            self.chanceOfRain.append(self.getMaxChanceOfRain(chanceOfRain))
            chanceOfRain = jsonWeather["forecasts"][1]["chanceOfRain"]
            self.chanceOfRain.append(self.getMaxChanceOfRain(chanceOfRain))

    def getLastUpdate(self):
        return self.lastUpdate
## メイン処理 ###################################################################################
if __name__ == '__main__':

    WT = getWeather()
    WT.update() # 天気予報サイトのHTMLタグから天気情報を抽出
    print("LastUpdate:",WT.getLastUpdate())
    print("今日の天気",WT.detail[0])
    print("今日の最低気温",WT.temperatureMin[0])
    print("今日の最高気温",WT.temperatureMax[0])
    print("今日の降水確率",WT.chanceOfRain[0])
    print("明日の天気",WT.detail[1])
    print("明日の最低気温",WT.temperatureMin[1])
    print("明日の最高気温",WT.temperatureMax[1])
    print("明日の降水確率",WT.chanceOfRain[1])


