#encoding:utf-8
import urllib.request, sys
import json
from datetime import datetime
import pdb
def getWether(citycode= '140010'):
    retval = {}
    forecasts = {}
    #citycode = '130010' #東京
    request = urllib.request.Request('http://weather.livedoor.com/forecast/webservice/json/v1?city=%s'%citycode)
    resp = urllib.request.urlopen(request).read().decode()
    
    # 読み込んだJSONデータをディクショナリ型に変換
    resp = json.loads(resp)
    
    retval['title']=resp['title']
    retval['message']=resp['description']['text']
    retday = '今日'
    #15時以降は、明日の天気を表示する
    if int(datetime.now().strftime('%H')) >= 15: retday = '明日'
    retval['day']=retday
    for forecast in resp['forecasts']:
        if forecast['dateLabel']==retday:
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

def getTrainDelay(target=['湘南新宿ライン','東海道線','横須賀線','京浜東北線']):
    retval=''
    request = urllib.request.Request('https://rti-giken.jp/fhc/api/train_tetsudo/delay.json')
    delays = urllib.request.urlopen(request).read().decode()
    
    delays = json.loads(delays)

    infoCount = 0
    for delay in delays:
        if delay['name'] in target:
            retval+=delay['name'] + ', '
            infoCount += 1
    if infoCount == 0: 
        #retval='現在関連する電車の遅延などは無いようです。'
        retval=None
    else:
        retval = retval[:-2]+'の運転が遅延しているようです。'
    return retval

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