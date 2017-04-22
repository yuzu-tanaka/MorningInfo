#encoding:utf-8
isRaspi = False
# Flask などの必要なライブラリをインポートする
from flask import Flask, render_template, request, redirect, url_for
import numpy as np
from getJSON import *

if isRaspi == True:
    #焦電センサーの結果を18ピンでもらう
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18, GPIO.IN)

# 自身の名称を app という名前でインスタンス化する
app = Flask(__name__)

# index にアクセスしたときの処理
@app.route('/')
def index():
    title = "天気と電車"
    if isRaspi == True:
        retGPIO = GPIO.input(18)
    else:
        retGPIO = 1
    if 1==retGPIO:
        print('GPIO==1')
        respW = getWether('140010')
        respT = getTrainDelay()

    day = respW['day']
    message = respW['message']
    telop = respW['telop']
    icon = '/static/wetherIcons/'+ respW['icon'] + '.png'
    tempeMax = respW['max']
    tempeMin = respW['min']


    # index.html をレンダリングする
    return render_template('index.html',\
	 message=message,telop=telop,icon=icon,\
	 tempeMax=tempeMax,tempeMin=tempeMin, \
	 train=respT, day=day, title=title)

if __name__ == '__main__':
    app.debug = True # デバッグモード有効化
    app.run(host='0.0.0.0') # どこからでもアクセス可能に