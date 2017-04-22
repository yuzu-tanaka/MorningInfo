#encoding:utf-8
import urllib2, sys
import json
import pdb
def getWether(citycode= '140010'):
    retval = {}
    forecasts = {}
    #citycode = '130010' #東京
    resp = urllib2.urlopen('http://weather.livedoor.com/forecast/webservice/json/v1?city=%s'%citycode).read()
    pdb.set_trace()
    # 読み込んだJSONデータをディクショナリ型に変換
    resp = json.loads(resp)
    return resp

def getTrainDelay():
    delays = urllib2.urlopen('https://rti-giken.jp/fhc/api/train_tetsudo/delay.json').read()
    
    delays = json.loads(delays)
    return delays

if __name__ == '__main__':

    resp = getWether('130010')
    
    print('**************************')
    print(resp['title'])
    print('**************************')
    print(resp['description']['text'])
    
    for forecast in resp['forecasts']:
        print('**************************')
        print(forecast['dateLabel']+'('+forecast['date']+')')
        print(forecast['telop'])
        print(forecast['image']['url'])
        if None != forecast['temperature']['max']:
            print(forecast['temperature']['max']['celsius'])
        if None != forecast['temperature']['min']:
            print(forecast['temperature']['min']['celsius'])
    print('**************************')
    
    print('**************************')
    delays = getTrainDelay()
    infoCount = 0
    for delay in delays:
        if delay['name'] in ['湘南新宿ライン','東海道線','横須賀線','京浜東北線']:
            print(delay['name'] + 'が遅れてます')
            infoCount += 1
    if infoCount == 0: print('Delay info is none.')